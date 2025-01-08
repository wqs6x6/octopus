
from workflow import Workflow
from user import User

couchdb_url = 'http://admin:password@172.21.0.4:5984/'



def user_simulation():
    # 定义多个工作流的资源配置
    #sequence
    function_resources_1 = {
        "function1": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function2": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function3": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function4": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function5": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function6": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function7": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function8": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },"function9": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function10": {
           "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        }
    }
    #switchw1l6-section1
    function_resources_2 = {
        "function1": {
            "cpu": "1 core",
            "memory": "0.125 GB",
            "disk": "1 GB"
        }
    }
    #switchw1l6-section2
    function_resources_3 = {
        "function1": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function2": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function3": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function4": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function5": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function6": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        }
    }

    # parallel_10
    function_resources_4 = {
        "function1": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function2": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function3": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function4": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function5": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function6": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function7": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function8": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },"function9": {
            "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        },
        "function10": {
           "cpu": "0.1 cores",
            "memory": "0.125 GB",
            "disk": "1 GB"
        }
    }

    slo_1 = {
        "response_time": "95% requests within 1000ms",
        "success_rate": "99.9% request success",
        "throughput": "500 requests per second",
        "error_rate": "error rate less than 0.01% per month",
        "priority" : 0.2
    }

    slo_2 = {
        "response_time": "90% requests within 1000ms",
        "success_rate": "99.5% request success",
        "throughput": "300 requests per second",
        "error_rate": "error rate less than 0.05% per month",
        "priority" : 0.4
    }
    slo_3 = {
        "response_time": "90% requests within 1000ms",
        "success_rate": "99.5% request success",
        "throughput": "300 requests per second",
        "error_rate": "error rate less than 0.05% per month",
        "priority" : 0.4
    }

    slo_4 = {
        "response_time": "90% requests within 1000ms",
        "success_rate": "99.5% request success",
        "throughput": "300 requests per second",
        "error_rate": "error rate less than 0.05% per month",
        "priority" : 0.4
    }

    # 创建多个 Workflow 实例
    workflow_1 = Workflow(
        workflow_name="Example Workflow 1",
        workflow_description="This is an example workflow 1.",
        function_resources=function_resources_1,
        slo=slo_1,
        couchdb_url=couchdb_url,
        db_name='workflow_info_db'
    )
    
    # workflow_2 = Workflow(
    #     workflow_name="Example Workflow 2",
    #     workflow_description="This is an example workflow 2.",
    #     function_resources=function_resources_2,
    #     slo=slo_2,
    #     couchdb_url=couchdb_url,
    #     db_name='workflow_info_db'
    # )

    # workflow_3 = Workflow(
    #     workflow_name="Example Workflow 3",
    #     workflow_description="This is an example workflow 3.",
    #     function_resources=function_resources_3,
    #     slo=slo_3,
    #     couchdb_url=couchdb_url,
    #     db_name='workflow_info_db'
    # )

    # workflow_4 = Workflow(
    #     workflow_name="Example Workflow 4",
    #     workflow_description="This is an example workflow 4.",
    #     function_resources=function_resources_4,
    #     slo=slo_4,
    #     couchdb_url=couchdb_url,
    #     db_name='workflow_info_db'
    # )


    # 创建 User 实例并触发工作流请求
    user = User(
        index=1,
        couchdb_url = couchdb_url,
        db_name='workflow_invocations_db',
    )
    payload_template = {"data": "example payload data"}
    
    # 模拟发送不同工作流的随机次数的请求
    print("+++++++++++++++++++++++++check point one+++++++++++++++++++")
    user.simulate_requests([workflow_1], payload_template, min_requests=1000, max_requests=1000)
    # user.simulate_requests([workflow_2], payload_template, min_requests=50, max_requests=50)
    # user.simulate_requests([workflow_3], payload_template, min_requests=10, max_requests=10)
    # user.simulate_requests([workflow_4], payload_template, min_requests=50, max_requests=50)

if __name__ == "__main__":
    user_simulation()