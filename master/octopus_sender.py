import couchdb
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time

class Sender:
    def __init__(self, couchdb_url, kafka_bootstrap_servers, workflow_invocations_db_name, invocation_state_db_name):
        
        self.couch = couchdb.Server(couchdb_url)
        self.producer = KafkaProducer(
            bootstrap_servers = kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        if workflow_invocations_db_name in self.couch:
            self.workflow_invocations_db = self.couch[workflow_invocations_db_name]
        else:
            self.workflow_invocations_db = self.couch.create(workflow_invocations_db_name)

        if invocation_state_db_name in self.couch:
            self.invocation_state_db = self.couch[invocation_state_db_name]
        else:
            self.invocation_state_db = self.couch.create(invocation_state_db_name)

        # Setup logging for each Sender instance
        self.logger = logging.getLogger(f'Sender')
        handler = logging.FileHandler(f'./logs/Octopus_Sender.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def fetch_and_process(self):
        while True:
            self.logger.info(f"Number of invocations: {len(self.workflow_invocations_db)}")
            cold_start_invocations_sum = []
            
            start_time = time.time()

            for doc_id in self.workflow_invocations_db:
                try:
                    doc = self.workflow_invocations_db[doc_id]
                    self.logger.debug(f"Invocation info: {doc}")

                    workflow_name = doc.get('Workflow_name')

                    # 检索 invocation_state_db 数据库
                    results = len(list(self.invocation_state_db.find({'selector': {'Workflow_name': workflow_name}})))
                    if results:
                        self.logger.info(f"检索结果: {results}")
                    else:
                        cold_start_invocations_sum.append(doc)

                    # 删除该内容
                    self.workflow_invocations_db.delete(doc)
                except Exception as e:
                    self.logger.error(f"Error processing document {doc_id}: {e}")

            if cold_start_invocations_sum:
                self.send_to_kafka('request_publisher_queue', cold_start_invocations_sum)
            
            end_time = time.time()
            self.logger.info(f"Time cost of Sender: {end_time-start_time}")
            
            time.sleep(18)  # 每5秒循环一次

    def send_to_kafka(self, topic, message):
        try:
            self.producer.send(topic, message)
            self.producer.flush()
            self.logger.info(f"Sent to {topic}: {message}")
        except KafkaError as e:
            self.logger.error(f"Failed to send message to Kafka: {e}")

