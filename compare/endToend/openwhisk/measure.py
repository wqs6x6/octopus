import subprocess
import csv
import time
import numpy as np

def execute_command_and_save_times(command_template, num_executions, csv_filename):
    times = []

    for i in range(num_executions):
        start_time = time.time()
        
        # 动态生成命令
        command = command_template.format(param_value=i+30)
        
        # 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 打印结果（可选）
        print(result.stdout)
        
        # 保存执行时间
        times.append(execution_time)
    
    # 计算执行时间的CDF
    sorted_times = np.sort(times)
    cdf = np.arange(1, num_executions + 1) / num_executions
    
    # 将执行时间和CDF写入 CSV 文件
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Execution Time (s)", "CDF"])
        for exec_time, cdf_value in zip(sorted_times, cdf):
            writer.writerow([exec_time, cdf_value])

# 使用示例
command_template = "wsk action invoke mySequence10 --result --param key1 {param_value} -i"
num_executions = 10
csv_filename = "execution_times_rps10_cdf.csv"
execute_command_and_save_times(command_template, num_executions, csv_filename)
