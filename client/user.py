import couchdb
from workflow import Workflow
import datetime
import json
import time
import random

class User:
    def __init__(self, index: int, couchdb_url: str,db_name: str):
        """
        初始化 User 类的实例。
        
        :param index: int, 用户的索引
        :param couchdb_url: str, CouchDB 服务器的 URL
        :param db_name: str, CouchDB 数据库的名称
        """
        self.index = index
        self.db_name = db_name
        self.couch = couchdb.Server(couchdb_url)

        if self.db_name in self.couch:
            self.db = self.couch[self.db_name]
        else:
            self.db = self.couch.create(self.db_name)

    def trigger_workflow_request(self, workflow: Workflow, payload: dict):
        """
        向 CouchDB 写入工作流请求以触发工作流。
        
        :param workflow: Workflow, 工作流实例
        :param payload: dict, 请求的载荷数据
        """
        request = {
            "user_index": self.index,
            "workflow_name": workflow.workflow_name,
            "workflow_description": workflow.workflow_description,
            # "function_resources": workflow.function_resources,
            "payload": payload,
            "invoke_time": datetime.datetime.now().isoformat(),
            "status": "pending",
            "workflow_slo": workflow.slo
        }

        # print("+++++++++++++Hello test++++++++++++++++++++")
        return self.db.save(request)
        # print("+++++++++check point 2+++++++++++")
        # print(f"Triggered workflow request: {json.dumps(request, indent=2)}")

    def simulate_requests(self, workflows: list, payload_template: dict, min_requests: int, max_requests: int):
        """
        模拟持续发送多个工作流请求。
        
        :param workflows: list, 不同工作流实例的列表
        :param payload_template: dict, 请求的载荷数据模板
        :param min_requests: int, 每个工作流的最小请求数
        :param max_requests: int, 每个工作流的最大请求数
        """
        

        for workflow in workflows:
            num_requests = random.randint(min_requests, max_requests)
            for i in range(num_requests):
                payload = payload_template.copy()
                payload["data"] = f"{payload_template['data']} - request {i + 1}"

                if self.trigger_workflow_request(workflow, payload):
                    time.sleep(0.001) 
                 # 模拟一些间隔