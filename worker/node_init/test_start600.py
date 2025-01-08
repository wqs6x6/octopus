
from threading import Thread

from node import Node

if __name__ == "__main__":
    schedule_profile = {
        'cpu_percent': 80,
        'memory_percent': 90,
        'disk_percent': 90,
        'num_processes': 10000
    }

    node = Node(
        index = 600,
        jtopic_index = 'node_600_topic',
        couchdb_url='http://admin:password@172.21.0.4:5984/',
        kafka_bootstrap_servers = '172.21.0.2:9092',
        schedule_profile = schedule_profile
    )
    Thread(target=node.start).start()
    Thread(target=node.monitor_and_run).start()

