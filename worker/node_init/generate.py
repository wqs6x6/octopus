import re

def modify_code(index, jtopic_index, bootstrap_servers ,input_file, output_file):
    with open(input_file, 'r') as file:
        code = file.read()

    # Modify the index value
    code = re.sub(r'index\s*=\s*\d+', f'index = {index}', code)

    # Modify the jtopic_index value
    code = re.sub(r'jtopic_index\s*=\s*\'node_\d+_topic\'', f'jtopic_index = \'{jtopic_index}\'', code)

    code = re.sub(r"kafka_bootstrap_servers\s*=\s*'[^']*'", f"kafka_bootstrap_servers = '{bootstrap_servers}'", code)

    with open(output_file, 'w') as file:
        file.write(code)

if __name__ == "__main__":
    # Define the total number of scripts to generate
    total_scripts = 1024  # Change this value as needed
    # bootstrap_servers = '172.21.0.2:9092,172.21.0.5:9093'
    bootstrap_servers = '172.21.0.2:9092'
    input_file = 'start_script.py'

    for i in range(1, total_scripts + 1):
        index = i
        jtopic_index = f'node_{i}_topic'
        output_file = f'test_start{i}.py'
        modify_code(index, jtopic_index,bootstrap_servers, input_file, output_file)
        print(f'Generated {output_file}')
