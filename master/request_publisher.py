import time
from threading import Thread
import re
import json
import uuid
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from kafka import TopicPartition
from datetime import datetime

class RequestPublisher:
    def __init__(self, kafka_bootstrap_servers, request_publisher_queue, waiting_process_list, application_processing_result):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.request_consumer = KafkaConsumer(
            request_publisher_queue,
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='request_publisher_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.result_consumer = KafkaConsumer(
            application_processing_result,
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='result_publisher_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.waiting_process_list = waiting_process_list

        # Setup logging
        self.logger = logging.getLogger(f'RequestPublisher')
        handler = logging.FileHandler(f'./logs/Octopus_{self.logger.name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def batch_processing_and_priority_sorting(self, tasks):
        classified_data = {}

        # Step 1: Classify tasks by workflow_name and parse relevant information
        for item in tasks[0]:
            workflow_name = item['workflow_name']
            invoke_time = item['invoke_time']
            payload = item['payload']

            # Extract response time from the response_time string
            response_time_str = item['workflow_slo']['response_time']
            match = re.search(r'\b(\d+)ms\b', response_time_str)
            response_time = int(match.group(1))

            # Initialize the list for the workflow_name if not already present
            if workflow_name not in classified_data:
                classified_data[workflow_name] = []

            # Append the parsed item to the corresponding workflow_name list
            classified_data[workflow_name].append({
                'workflow_name': workflow_name,
                'invoke_time': invoke_time,
                'response_time': response_time,
                'payload': payload,
                'priority': item['workflow_slo'].get('priority', 1)
            })

        merged_data = {}
        index = 1

        # Step 2: Process each workflow_name to merge tasks into units
        for workflow_name, items in classified_data.items():
            # Sort items by invoke_time
            items.sort(key=lambda x: datetime.fromisoformat(x['invoke_time']))

            merged_items = []
            current_unit = []

            for i in range(len(items)):
                if i == 0:
                    current_unit.append(items[i])
                else:
                    # Calculate the time difference between the first task in the unit and the current task
                    time_diff = datetime.fromisoformat(items[i]['invoke_time']) - datetime.fromisoformat(current_unit[0]['invoke_time'])
                    if time_diff.total_seconds() * 1000 <= current_unit[0]['response_time']:
                        current_unit.append(items[i])
                    else:
                        merged_items.append(current_unit)
                        current_unit = [items[i]]

            if current_unit:
                merged_items.append(current_unit)
            
            # Store the merged items under a unique unit name
            unit_name = 'unit' + str(index)
            merged_data[unit_name] = merged_items
            index += 1

        sum_units = []
        # Step 3: Calculate priority sum and unit length for sorting
        for units in merged_data.values():
            for unit in units:
                unit_priority_sum = sum(item['priority'] for item in unit)
                sum_units.append({'unit': unit, 'priority_sum': unit_priority_sum, 'length': len(unit)})

        # Step 4: Sort units by priority sum (descending) and unit length (descending)
        sorted_units = sorted(sum_units, key=lambda u: (-u['priority_sum'], -u['length']))
        result_units = [u['unit'] for u in sorted_units]

        return result_units

    def fetch_rpq_tasks(self):
        self.logger.info(f"Listening for messages on {self.request_consumer.subscription()}...")
        tasks = []
        start_time = time.time()
        for message in self.request_consumer:
            tasks.append(message.value)
            end_time = time.time()
            if end_time - start_time >= 5:
                break
        return tasks

    def send_to_waiting_process_list(self, tasks):
        try:
            self.producer.send(self.waiting_process_list, tasks)
            self.producer.flush()
            # self.logger.info(f"Sent to {self.waiting_process_list}: {tasks}")
            self.logger.info(f"Sent to {self.waiting_process_list} successfully")
        except KafkaError as e:
            self.logger.error(f"Failed to send message to Kafka: {e}")
    
    def monitoring_and_allocating_and_sending(self, data):
        task_allocation = {}
        unique_id = data['unique_id']
        number_task = data['number_task']
        tasks = list(range(number_task))

        task_allocation['unique_id'] = unique_id

        

        for message in self.result_consumer:
            message_value = message.value

            self.logger.info(f"Candidate result: {message_value}")

            if message_value['unique_id'] == unique_id:
                node_index = message_value['node_index']
                exception_task_index_list = message_value['exception_task_index_list']
                for index in exception_task_index_list:
                    if index in tasks:
                        task_allocation[f'node_index_{node_index}'] = index

                        affirm_node_topic = f'node_{node_index}_topic'
                        affirm_data = {'unique_id': unique_id, 'task_index': index}

                        self.producer.send(affirm_node_topic, affirm_data)
                        self.producer.flush()
                        self.logger.info(f"Sent {affirm_data} to {affirm_node_topic}")
                        tasks.remove(index)
                        break
            
            # Check if all tasks are processed
            if not tasks:
                self.logger.info("All tasks processed. Clearing remaining messages.")

                start_time = time.time()
                while time.time() - start_time < 30:
                    # Do something repeatedly
                    pass
            
                # Clear remaining messages
                partitions = self.result_consumer.assignment()
                for partition in partitions:
                    # Get the end offset for the partition
                    end_offset = self.result_consumer.end_offsets([partition])[partition]
                    # Seek to the end offset
                    self.result_consumer.seek(partition, end_offset)
                
                # Close the consumer
                # self.result_consumer.close()
                break

        self.logger.info(f"Task allocation result: {task_allocation}")
        return task_allocation


    # def monitoring_and_allocating_and_sending(self, data):
    #     task_allocation = {}
    #     unique_id = data['unique_id']
    #     number_task = data['number_task']
    #     tasks = list(range(number_task))

    #     task_allocation['unique_id'] = unique_id

    #     for message in self.result_consumer:
    #         message_value = message.value
            
    #         self.logger.info(f"Candidate result: {message_value}")

    #         if message_value['unique_id'] == unique_id:
    #             node_index = message_value['node_index']
    #             exception_task_index_list = message_value['exception_task_index_list']
    #             for index in exception_task_index_list:
    #                 if index in tasks:
    #                     task_allocation[f'node_index_{node_index}'] = index

    #                     affirm_node_topic = f'node_{node_index}_topic'
    #                     affirm_data = {'unique_id': unique_id, 'task_index': index}
                    
    #                     self.producer.send(affirm_node_topic, affirm_data)
    #                     self.producer.flush()
    #                     self.logger.info(f"Sent {affirm_data} to {affirm_node_topic}")
    #                     tasks.remove(index)
    #                     break
    #         if not tasks:
    #             self.logger.info("All tasks processed. Clearing remaining messages.")
    #             # Clear remaining messages
    #             partitions = self.result_consumer.assignment()
    #             for partition in partitions:
    #                 end_offset = self.result_consumer.end_offsets([partition])[partition]
    #                 self.result_consumer.seek(partition, end_offset)
    #             # self.result_consumer.close()
    #             break

    #     self.logger.info(f"Task allocation result: {task_allocation}")
    #     return task_allocation

    def new_start(self):
        while True:
            tasks = self.fetch_rpq_tasks()
            start_time = time.time()
            if tasks:
                # self.logger.info(f"Tasks from sender: {tasks}")
                # print("++++++++++++++++Check Point1++++++++++++++++++++++++++++++++++")
                processed_tasks = self.batch_processing_and_priority_sorting(tasks)
                # print("++++++++++++++++Check Point2++++++++++++++++++++++++++++++++++")
                unique_id = str(uuid.uuid4())
                data_to_send = {
                    'unique_id': unique_id,
                    'tasks': processed_tasks,
                    'number_task': len(processed_tasks)
                }
                sub_data_to_send = {
                    'unique_id': unique_id,
                    'number_task': len(processed_tasks)
                }
                
                self.send_to_waiting_process_list(data_to_send)
                
                self.logger.info("---------------------Check point--------------------")
                self.monitoring_and_allocating_and_sending(sub_data_to_send)


            end_time = time.time()
            self.logger.info(f"Time cost of request publisher: {end_time - start_time}")

# 使用示例
# publisher = RequestPublisher('localhost:9092', 'request_publisher_queue', 'waiting_process_list', 'application_processing_result')
# publisher.new_start()
