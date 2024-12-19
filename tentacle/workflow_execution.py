import docker
import json
import tempfile
import os
from queue import Queue
from threading import Thread, Lock
import yaml
import time
from concurrent.futures import ThreadPoolExecutor
import csv  # Import csv module

class DockerTask:
    def __init__(self, task_info):
        self.name = task_info['name']
        self.image = task_info['image']
        self.client = docker.from_env()
        self.container = None
        self.shared_dir = tempfile.mkdtemp()
        self.lock = Lock()  # Create a lock for each task

    def execute(self, payload, request_id):
        with self.lock:  # Ensure only one thread can execute this code at a time
            # If the container does not exist, create a new container
            if self.container is None:
                self.container = self.client.containers.run(
                    self.image,
                    command="tail -f /dev/null",  # Keep the container running
                    detach=True,
                    remove=False,
                    volumes={self.shared_dir: {'bind': '/app/data', 'mode': 'rw'}}
                )

            # Generate a unique input and output file name
            input_file = os.path.join(self.shared_dir, f'input_{request_id}.json')
            output_file = os.path.join(self.shared_dir, f'output_{request_id}.json')

            # Ensure the shared directory exists
            if not os.path.exists(self.shared_dir):
                os.makedirs(self.shared_dir)
            # Write payload to input file
            with open(input_file, 'w') as f:
                json.dump(payload, f)

        # Print debug information
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")

        # Execute processing command in the container, ensuring the use of paths within the shared volume
        exec_result = self.container.exec_run(cmd=f"python /app/process.py /app/data/input_{request_id}.json /app/data/output_{request_id}.json", workdir="/app")

        # Read output result from the shared directory
        try:
            with open(output_file, 'r') as f:
                result = json.load(f)
            return result
        except FileNotFoundError:
            return {"error": f"Task {self.name} failed: {exec_result.output.decode()}"}

    def cleanup(self):
        with self.lock:  # Ensure only one thread can execute this code at a time
            if self.container:
                try:
                    if self.container.status == 'running':
                        self.container.stop()  # Try to stop the container
                    self.container.remove()  # Try to remove the container
                except docker.errors.NotFound:
                    print(f"Container {self.container.id} does not exist, cannot stop or remove.")
                except Exception as e:
                    print(f"Error cleaning up container: {e}")

            # Check if the shared directory exists
            if os.path.exists(self.shared_dir):
                for filename in os.listdir(self.shared_dir):
                    file_path = os.path.join(self.shared_dir, filename)
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"Error deleting file: {e}")  # Add error handling
                os.rmdir(self.shared_dir)
            else:
                print(f"Shared directory {self.shared_dir} does not exist, cannot clean up.")

class Workflow:
    def __init__(self, tasks):
        self.tasks = [DockerTask(task) for task in tasks]
        self.request_queue = Queue()  # Request queue
        self.results = Queue()  # Use Queue to store results
        self.lock = Lock()  # Create a lock to protect shared resources

    @classmethod
    def from_yaml(cls, yaml_file):
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
            return cls(config['tasks'])

    def process_request(self, payload):
        request_id = payload.get('request_id')
        results = {}
        
        # Record request start time
        request_start_time = time.perf_counter()

        # Use thread pool to process each task in parallel
        with ThreadPoolExecutor(max_workers=len(self.tasks)) as executor:
            futures = {}
            
            # Submit the first task
            first_task = self.tasks[0]
            futures[executor.submit(first_task.execute, payload, request_id)] = first_task

            # Submit subsequent tasks sequentially
            for i in range(1, len(self.tasks)):
                task = self.tasks[i]
                # Wait for the previous task to complete and get the result
                previous_result = futures.popitem()[0].result()  # Get the result of the previous task
                print(f"Previous result: {previous_result}")
                # Use the result of the previous task as input for the current task
                futures[executor.submit(task.execute, previous_result, request_id)] = task

            # Process results of all tasks
            for future in futures:
                try:
                    result = future.result()  # Get task result
                    results[futures[future].name] = result
                    print(f"Task {futures[future].name} processed request {request_id} with result: {result}")
                except Exception as e:
                    print(f"Task encountered an error: {e}")

        # Record request end time
        request_end_time = time.perf_counter()
        total_time = request_end_time - request_start_time  # Calculate total time
        print(f"Request {request_id} total processing time: {total_time:.6f} seconds")  # Print total time

        # Write request ID and execution time to CSV file
        self.save_request_time_to_csv(request_id, total_time)

        return results

    def save_request_time_to_csv(self, request_id, execution_time):
        csv_file = './output/rps50.csv'  # Specify CSV file name
        # Open CSV file in append mode
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request_id, execution_time])  # Write request ID and execution time

    def worker(self):
        while True:
            payload = self.request_queue.get()
            if payload is None:
                break
            try:
                result = self.process_request(payload)
                self.results.put(result)
            except Exception as e:
                print(f"Error processing request: {e}")
            finally:
                self.request_queue.task_done()

    def start_processing(self, num_workers=5):
        threads = []
        for _ in range(num_workers):
            thread = Thread(target=self.worker)
            thread.start()
            threads.append(thread)
        return threads

    def add_request(self, payload):
        self.request_queue.put(payload)  # Add request to the queue

    def stop_processing(self, threads):
        for _ in threads:
            self.request_queue.put(None)  # Add None to the queue to end worker threads
        for thread in threads:
            thread.join()  # Wait for all threads to complete

    def get_results(self):
        # Get all results
        return list(self.results.queue)





