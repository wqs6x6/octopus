import json
import time
import psutil
import couchdb
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from kafka.structs import TopicPartition
from threading import Thread

class Node:
    def __init__(self, index, jtopic_index, kafka_bootstrap_servers, couchdb_url, schedule_profile):
        self.index = index
        self.jtopic_index = jtopic_index
        self.schedule_profile = schedule_profile
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.couchdb_url = couchdb_url
        

        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumer = KafkaConsumer(
            'waiting_process_list',
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=f'node_{index}',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.topic_consumer = KafkaConsumer(
            jtopic_index,
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=f'node_{index}_topic',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        # Set up logging for the node
        self.logger = logging.getLogger(f'Node_{index}')
        handler = logging.FileHandler(f'./logs/Node_{index}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        self.logger.info(f'Node {index} initialized.')

    def get_system_status(self):
        """ 获取容器内部的系统状态 """
        status = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'num_processes': len(psutil.pids())
        }
        self.logger.info(f"System status: {status}")
        return status

    def can_pull_tasks(self):
        """ 判断是否可以拉取任务 """
        start_time = time.time()
        status = self.get_system_status()
        for key, value in self.schedule_profile.items():
            if status[key] > value:
                return False
        end_time = time.time()

        self.logger.info(f"Time cost of node self-checking: {end_time - start_time}")
        return True

    def match_task(self, tasks):
        """ 根据系统状态和任务要求计算匹配度 """
        status = self.get_system_status()
        couch = couchdb.Server(self.couchdb_url)
        db = couch['workflow_info_db']

        def get_workflow_info(workflow_name):
            """从 CouchDB 获取工作流信息"""
            result = list(db.find({'selector': {'workflow_name': workflow_name}}))
            if result:
                return result[0]
            return None

        def find_best_batch_indexes(batch_memory_requirements):
            """找到满足条件的 batch，并返回内存差值最小的 batch 的索引号列表，按匹配度从高到低排序"""
            free_memory = psutil.virtual_memory().available / (1024 ** 3)  # 以 GB 为单位
            
            eligible_batches = []

            for index, batch in enumerate(batch_memory_requirements):
                required_memory = batch['required_memory']
                required_memory_float = float(''.join(filter(lambda x: x.isdigit() or x == '.', required_memory)))

                if required_memory_float <= free_memory:
                    diff = free_memory - required_memory_float
                    eligible_batches.append((index, diff))

            # 按内存差值从小到大排序（即匹配度从高到低）
            eligible_batches.sort(key=lambda x: x[1])

            # 返回排序后的索引列表
            return [index for index, diff in eligible_batches]
        

        def calculate_max_memory_requirements(data):
            """计算每个 batch 的最大内存需求"""
            batch_memory_requirements = []
            for batch in data:
                max_memory = 0.0
                for task in batch:
                    workflow_name = task['workflow_name']
                    workflow_info = get_workflow_info(workflow_name)
                    if workflow_info:
                        function_resources = workflow_info.get('function_resources', {})
                        for resources in function_resources.values():
                            memory = resources.get('memory', '0 GB').split()
                            if len(memory) > 1 and memory[1].lower() == 'gb':
                                max_memory = max(max_memory, float(memory[0]))  # 更新最大内存值
                batch_memory_requirements.append({
                    'batch_id': batch[0]['invoke_time'],  # 使用第一个任务的 invoke_time 作为 batch_id
                    'required_memory': str(max_memory) + ' GB'  # 以 GB 为单位
                })
            return batch_memory_requirements
         # 解析输入数据
        for task in tasks:
            unique_id = task['unique_id']
            tasks = task['tasks']
            # 计算每个 batch 的内存需求
            batch_memory_requirements = calculate_max_memory_requirements(tasks)
            # 查找满足条件的最佳 batch 并返回索引号
            best_index = find_best_batch_indexes(batch_memory_requirements)
            # return {unique_id:best_index}
            return {'unique_id':task['unique_id'],'exception_task_index_list':best_index}
        
        else:
            return {"Error: Topic \'waiting_process_lis\' is empty!!"}

    def new_pull_tasks(self):
        """ 拉取任务 """
        tasks = []
        self.logger.info("Pulling task....")

        start_time = time.time()
        for message in self.consumer:
            tasks.append(message.value)
            end_time = time.time()
            if end_time - start_time >= 1:
                break
        return tasks


    def send_processing_result(self, result):
        """ 发送处理结果到 application_processing_result 主题 """
        try:
            self.logger.info("++++++++++++Just Test++++++++++++")
            # data_to_send = {
            #     "node_index":self.index,
            #     # "application_result":result
            #     result
            # }
            result['node_index'] = self.index
            
            self.producer.send('application_processing_result', result)
            self.producer.flush()
            self.logger.info(f"Sent 'application_processing_result' processing result: {result}")
        except KafkaError as e:
            self.logger.error(f"Failed to send message to Kafka: {e}")


    def run_workflow(self, task):
        """ 模拟运行工作流并生成结果 """
        # 模拟处理任务
        # time.sleep(2)  # 假设处理任务需要2秒

        # self.generate_response(task)
        print("Executing Tasks",task)


    def monitor_and_run(self):
        start_time = time.time()
        """ 持续监视 topic 并执行工作流 """
        for message in self.topic_consumer:
            task = message.value
            end_time = time.time()
            self.run_workflow(task)

            self.logger.info(f"Time cost of node monitoring: {end_time - start_time}")
            self.logger.info(f"Tasks that need to be executed: {task}")


    def display_node_info(self):
        """
        显示实例的具体内容。
        """
        self.logger.info("Node info:")
        self.logger.info(f"Index: {self.index}")
        self.logger.info(f"JTopic Index: {self.jtopic_index}")
        self.logger.info(f"Kafka Bootstrap Servers: {self.kafka_bootstrap_servers}")
        self.logger.info(f"Schedule Profile: {self.schedule_profile}")

    def start(self):
        """ 启动节点 """
        self.display_node_info()
        while True:
            
            if self.can_pull_tasks():
                self.logger.info("I can deal tasks")
                current_tasks = self.new_pull_tasks()

                
                if current_tasks:
                    start_time = time.time()
                    
                    # self.logger.info(f"Waiting process list: {current_tasks}")
                    exception_result = self.match_task(current_tasks)
                    self.logger.info(f"Exception index: {exception_result}")
                    self.send_processing_result(exception_result)
                    
                    end_time = time.time()
                    self.logger.info(f"Time cost of node: {end_time - start_time}")
                else:
                    continue

            else:
                self.logger.info("System resources are too high to pull tasks.")
            time.sleep(5)  # 每5秒检查一次

# # Example usage:
# if __name__ == "__main__":
#     node = Node(1, 'jtopic_index', 'localhost:9092', {'cpu_percent': 80, 'memory_percent': 80, 'disk_percent': 80})
#     node.start()
