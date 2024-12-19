import sys
import json
import os
import time


def fib_recursive(n):
    """
    Calculate Fibonacci number using iterative method
    Args:
        n: Integer representing the position in Fibonacci sequence
    Returns:
        Fibonacci number at position n
    """
    n = n % 30
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

def process_payload(input_file, output_file):
    start_time = time.perf_counter()
    
    # Initialize default payload
    payload = {
        'data': {},
        'status': {},
        'metadata': {}
    }

    try:
        # Read input data
        print(f"Reading input file: {input_file}")  # Debug information
        with open(input_file, 'r') as f:
            payload = json.load(f)

        # Extract the value of x
        if 'output' in payload.get('data', {}):
            x = payload['data']['output']['value']  # Use the value of output if the output field exists
        else:
            x = payload.get('data', {}).get('input', {}).get('value', 0)  # Otherwise, use the value of input

        # Calculate Fibonacci number
        fib_result = fib_recursive(x)
        # Calculate execution time
        execution_time = time.perf_counter() - start_time

        # Update payload
        payload['data']['input'] = {
            "value": x
        }
        payload['data']['output'] = {
            "value": fib_result
        }
        payload['status'] = {
            "code": "success",
            "message": None,
            "error": None
        }
        payload['metadata']['execution_time'] = round(execution_time, 6)

        # Write processing result
        print(f"Writing output file: {output_file}")  # Debug information
        with open(output_file, 'w') as f:
            json.dump(payload, f)

    except Exception as e:
        # Handle errors
        execution_time = time.perf_counter() - start_time
        payload['status'] = {
            "code": "error",
            "message": str(e),
            "error": type(e).__name__
        }
        payload['metadata']['execution_time'] = round(execution_time, 6)

        # Write processing result
        print(f"Writing output file: {output_file} due to error")  # Debug information
        with open(output_file, 'w') as f:
            json.dump(payload, f)

if __name__ == "__main__":


    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_payload(input_file, output_file)