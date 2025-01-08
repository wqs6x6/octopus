from typing import Dict, Any
import couchdb
import datetime

class Workflow:
    def __init__(self, workflow_name: str, workflow_description: str, function_resources: Dict[str, Dict[str, Any]], slo, couchdb_url: str, db_name: str):
        """
        初始化 Workflow 类的实例。
        
        :param workflow_name: str, 工作流的名字
        :param workflow_description: str, 工作流的描述
        :param function_resources: dict, 每个函数的资源配置
        :param slo: dict, 服务级别目标
        :param couchdb_url: str, CouchDB 服务器的 URL
        :param db_name: str, CouchDB 数据库的名称
        """
        self.workflow_name = workflow_name
        self.workflow_description = workflow_description
        self.function_resources = function_resources
        self.slo = slo
        self.couchdb_url = couchdb_url
        self.db_name = db_name

        self.save_to_couchdb()

    def display_info(self):
        """
        显示工作流的详细信息。
        """
        print(f"Workflow Name: {self.workflow_name}")
        print(f"Workflow Description: {self.workflow_description}")
        print("Function Resources:")
        for function_name, resources in self.function_resources.items():
            print(f"  Function: {function_name}")
            for resource_type, resource_value in resources.items():
                print(f"    {resource_type}: {resource_value}")
        print("Service Level Objective:", self.slo)

    def save_to_couchdb(self):
        """
        将工作流信息保存到 CouchDB
        """
        couch = couchdb.Server(self.couchdb_url)
        if self.db_name in couch:
            db = couch[self.db_name]
        else:
            db = couch.create(self.db_name)

        workflow_doc = {
            "workflow_name": self.workflow_name,
            "workflow_description": self.workflow_description,
            "function_resources": self.function_resources,
            "slo": self.slo,
            "timestamp": datetime.datetime.now().isoformat()
        }
        db.save(workflow_doc)
        print(f"Workflow{self.workflow_name} saved to CouchDB in database '{self.db_name}'.")

