import os
import sys
import pandas as pd
import boto3   
import numpy as np 
import matplotlib.pyplot as plt

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps1000"
# RPS = 1000

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps500"
# RPS = 500

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps100"
# RPS = 100

EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps50"
RPS = 50

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps10"
# RPS = 10


def get_execution_by_name(state_machine_arn: str, execution_names: list) -> list:
    """
    根据状态机ARN和执行名称获取执行的详细信息
    :param state_machine_arn: 状态机的ARN
    :param execution_names: 执行的名称列表
    :return: 包含执行ARN和执行时间的字典列表
    """
    client = boto3.client('stepfunctions', region_name='ap-southeast-1')  # 请根据您的实际区域进行修改

    try:
        # 列出所有执行
        response = client.list_executions(
            stateMachineArn=state_machine_arn,
            statusFilter='SUCCEEDED'  # 修改为有效的状态值
        )
        print(response)
    except Exception as e:
        print(f"Error fetching executions: {e}")
        return []

    # 查找匹配的执行
    all_results = [
        {
            'ExecutionArn': execution['executionArn'],
            'ExecutionTime': (execution['stopDate'] - execution['startDate']).total_seconds() if execution['stopDate'] and execution['startDate'] else None
        }
        for execution in response['executions']
        if execution['name'] in execution_names
    ]

    return all_results  # 返回所有结果

def save_cdf_to_csv(execution_times: list, filename: str):
    """
    计算并保存执行时间的CDF到CSV文件
    :param execution_times: 执行时间列表
    :param filename: 输出CSV文件名
    """
    # 计算CDF
    sorted_times = np.sort(execution_times)
    cdf = np.arange(1, len(sorted_times) + 1) / len(sorted_times)

    # 创建DataFrame并保存为CSV
    cdf_df = pd.DataFrame({'ExecutionTime': sorted_times, 'CDF': cdf})
    cdf_df.to_csv(filename, index=False)

# 示例调用
if __name__ == "__main__":
    state_machine_arn = "arn:aws:states:ap-southeast-1:827866353472:stateMachine:test-End-to-end"
    index_range = range(1, RPS + 1)  # 例如，1 到 5
    execution_names = [f'{EXECUTION_NAME_TEMPLATE}-{index}' for index in index_range]  # 格式化 execution_name

    # print(execution_names)
    all_results = get_execution_by_name(state_machine_arn, execution_names)

    print(all_results)

    # 计算并保存CDF
    execution_times = [result['ExecutionTime'] for result in all_results if result['ExecutionTime'] is not None]
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # 创建输出文件夹（如果不存在）
    output_file = os.path.join(output_dir, f"{EXECUTION_NAME_TEMPLATE}.csv")
    save_cdf_to_csv(execution_times, output_file)
    