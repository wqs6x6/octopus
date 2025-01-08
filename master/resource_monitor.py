import psutil
import subprocess
import time
import logging
import os

# 配置日志记录
logging.basicConfig(filename='./logs/resource_monitor.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 启动 test_start.py 脚本
process = subprocess.Popen(['python', 'test_start.py'])

# 获取启动的进程 ID
pid = process.pid

def get_docker_stats():
    try:
        result = subprocess.run(['docker', 'stats', '--no-stream'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            logging.error(f"Failed to get Docker stats: {result.stderr}")
            return ""
    except Exception as e:
        logging.error(f"Error getting Docker stats: {e}")
        return ""

try:
    # 定义监控的时间间隔（秒）
    interval = 5

    while True:
        # 获取进程信息
        proc = psutil.Process(pid)

        # 获取 CPU 和内存使用信息
        cpu_usage = proc.cpu_percent(interval=interval)
        memory_info = proc.memory_info()

        logging.info(f"CPU usage: {cpu_usage}%")
        logging.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        
        # 记录 Docker 容器状态
        docker_status = get_docker_stats()
        logging.info(f"Docker status:\n{docker_status}")

        # 暂停指定的时间间隔
        time.sleep(interval)

except psutil.NoSuchProcess:
    logging.error("Process terminated")

except KeyboardInterrupt:
    logging.warning("Monitoring interrupted")

finally:
    # 确保在脚本结束时清理进程
    process.terminate()
    process.wait()
    logging.info("Process terminated and monitoring stopped")
