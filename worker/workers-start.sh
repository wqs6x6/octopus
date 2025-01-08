#!/bin/bash

# 启动的 Python 程序数量
x=1024
# 保存所有进程 ID 的数组
pids=()

# 启动所有 Python 程序并将它们放入后台运行
for i in $(seq 1 $x)
do
    python node_init/test_start$i.py &
    # 获取最后一个后台进程的 PID 并保存到数组中
    pids+=($!)
done

# 等待所有后台进程启动完成
sleep 2

# 输出启动的进程信息
echo "Started ${#pids[@]} Python scripts in the background."
echo "PIDs: ${pids[@]}"

# 定义清理函数，用于终止所有进程并删除日志文件
cleanup() {
    echo "Stopping all Python scripts..."
    for pid in "${pids[@]}"; do
        kill $pid 2>/dev/null
    done
    echo "Deleting log files..."
    for i in $(seq 1 $x); do
        rm -f ./logs/Node_$i.log
    done
    echo "Cleanup complete."
}

# 在脚本结束时调用清理函数
trap cleanup EXIT

# 等待所有后台进程完成（此处仅为示例，实际应用中根据需求调整）
wait

echo "All Python scripts have been terminated."
