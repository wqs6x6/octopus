
import os
from threading import Thread
from request_publisher import RequestPublisher
from octopus_sender import Sender


def sender_start():
    sender = Sender(
        couchdb_url= os.environ.get('COUCHDB_URL'), 
        kafka_bootstrap_servers= os.environ.get('KAFKA_BOOTSTRAP_SERVERS'), 
        workflow_invocations_db_name='workflow_invocations_db',
        invocation_state_db_name='invocation_state_db'
    )
    sender.fetch_and_process()

def request_publisher_start():
    request_publisher = RequestPublisher(
        kafka_bootstrap_servers=os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
        request_publisher_queue='request_publisher_queue',
        waiting_process_list='waiting_process_list',
        application_processing_result='application_processing_result'
    )
    request_publisher.new_start()

if __name__ == "__main__":
    Thread(target=sender_start).start()
    Thread(target=request_publisher_start).start()
    