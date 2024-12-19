import unittest
import time
from workflow_execution import Workflow



class TestWorkflowExecution(unittest.TestCase):
    def setUp(self):
        # Parse workflow configuration from YAML file
        self.workflow = Workflow.from_yaml('Workflow.yaml')

    def test_multiple_requests(self):
        # Prepare multiple test data
        test_payloads = [
            {   
                "request_id": "request_1",
                "metadata": {},
                "data": {
                    "input": {
                        "value": 5
                    }
                }
            },
            {
                "request_id": "request_2",
                "metadata": {},
                "data": {
                    "input": {
                        "value": 6
                    }
                }
            },
            {
                "request_id": "request_3",
                "metadata": {},
                "data": {
                    "input": {
                        "value": 7
                    }
                }
            }
        ]

        # Start worker threads
        start_time = time.perf_counter()
        threads = self.workflow.start_processing(num_workers=3)

        # Add multiple requests with unique request IDs
        for payload in test_payloads:
            request_id = payload.get('request_id')  # Extract request_id from payload
            print(f"Adding request: {request_id} with payload: {payload}")
            self.workflow.add_request(payload)  # Add the request

        # Stop processing
        self.workflow.stop_processing(threads)
        print(f"Total time: {time.perf_counter() - start_time}")
        

if __name__ == '__main__':
    unittest.main() 