import unittest
import time
from workflow_execution import Workflow

RPS = 50

class TestWorkflowExecution(unittest.TestCase):
    def setUp(self):
        # Parse workflow configuration from YAML file
        self.RPS = RPS
        self.workflow = Workflow.from_yaml('Workflow.yaml')

    def test_multiple_requests(self):
        # Prepare multiple test data
        index_range = range(1, self.RPS + 1)  # e.g., 1 to 50
        test_payloads = []
        for index in index_range:
            test_payloads.append(
                {   
                    "request_id": f"request_{index}",
                    "metadata": {},
                    "data": {
                        "input": { 
                            "value": 30 + index
                        }
                    }
                })
        
        # Start worker threads
        start_time = time.perf_counter()
        threads = self.workflow.start_processing(num_workers=10)

        # Add multiple requests with unique request IDs
        # execution_times = {}  # Used to store execution time for each request
        for payload in test_payloads:
            request_id = payload.get('request_id') 
            print(f"Adding request: {request_id} with payload: {payload}")

            self.workflow.add_request(payload) 

        self.workflow.stop_processing(threads)
        print(f"Total time: {time.perf_counter() - start_time}")
    

if __name__ == '__main__':
    unittest.main() 