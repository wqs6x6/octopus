import boto3
import aiohttp
import asyncio
from functools import partial
import json


# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps1000"
# RPS = 1000

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps500"
# RPS = 500

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-3-rps100"
# RPS = 100

EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps50"
RPS = 50

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps10"
# RPS = 10


def start_step_function_execution(state_machine_arn, input_data, execution_name):
    """
    启动AWS Step Function的执行
    :param state_machine_arn: 状态机的ARN
    :param input_data: 输入数据，通常是JSON格式的字符串
    :param execution_name: 执行的名称
    :return: 执行ARN
    """
    # 创建Step Functions客户端，指定区域
    client = boto3.client('stepfunctions', region_name='ap-southeast-1')  # 请根据您的实际区域进行修改

    # 启动执行
    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=input_data,
        name=execution_name  # 添加执行名称
    )

    return response['executionArn']

async def start_step_function_execution_async(state_machine_arn, input_data, execution_name):
    """
    异步启动AWS Step Function的执行
    :param state_machine_arn: 状态机的ARN
    :param input_data: 输入数据，通常是JSON格式的字符串
    :param execution_name: 执行的名称
    :return: 执行ARN
    """
    loop = asyncio.get_event_loop()  # 添加这一行以获取事件循环
    async with aiohttp.ClientSession() as session:
        client = boto3.client('stepfunctions', region_name='ap-southeast-1')  # 请根据您的实际区域进行修改

        # 启动执行
        response = await loop.run_in_executor(None, partial(client.start_execution, 
            stateMachineArn=state_machine_arn,
            input=input_data,
            name=execution_name  # 添加执行名称
        ))

        return response['executionArn']

async def main_async(request_count: int = RPS) -> None:
    state_machine_arn = "arn:aws:states:ap-southeast-1:827866353472:stateMachine:test-End-to-end"
    tasks = []

    for i in range(1, request_count + 1):
        execution_name = f"{EXECUTION_NAME_TEMPLATE}-{i}"  # 设置执行名称
        input_data = f'{{"key1": "{30 + i}"}}'  # 设置输入数据，从30开始
        tasks.append(start_step_function_execution_async(state_machine_arn, input_data, execution_name))

    # 同时发送所有请求
    execution_arns = await asyncio.gather(*tasks)
    for arn in execution_arns:
        print(f"执行ARN: {arn}")

def get_execution_by_name(state_machine_arn: str, execution_names: list, input_payload: dict) -> list:
    """
    根据状态机ARN和执行名称获取执行的详细信息
    :param state_machine_arn: 状态机的ARN
    :param execution_names: 执行的名称列表
    :param input_payload: 输入有效负载
    :return: 包含执行ARN和执行时间的字典列表
    """
    client = boto3.client('stepfunctions', region_name='ap-southeast-1')  # 请根据您的实际区域进行修改

    try:
        # 启动执行
        for name in execution_names:
            print(name,name)
            response = client.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(input_payload)  # 将输入有效负载转换为JSON字符串
            )
            print(f"Started execution for {name}: {response['executionArn']}")
    except Exception as e:
        print(f"Error starting executions: {e}")
        return []

# 示例调用
if __name__ == "__main__":
    asyncio.run(main_async())
    state_machine_arn = input("请输入状态机ARN: ")  # 让用户输入状态机ARN
    input_payload = {"key": "value"}  # 这里定义您的输入有效负载
    index_range = range(1, RPS + 1)  # 例如，1 到 5
    execution_names = [f'{EXECUTION_NAME_TEMPLATE}-{index}' for index in index_range]  # 格式化 execution_name

    all_results = get_execution_by_name(state_machine_arn, execution_names, input_payload)

    print(all_results)
