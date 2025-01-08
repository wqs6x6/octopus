# Ocotopus: Decentralized Workflow-granular Scheduling for Serverless Workflow

## Description

Octopus(🐙), an efficient Serverless Workflow Management System.Octopus enables efficient workflow scheduling and execution across different levels of concurrency and cluster scales.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/wqs6x6/octopus.git
    ```

2. Install dependencies:
    ```bash
    docker-compose up -d    
    ```

## Usage

Run the following command to start the program:

First, *Worker* initialization.
```bash
./worker/workers-start.sh
```
Second, *Master* initialization.   
```bash
python3 ./master/start.py
```

Third, *Client* initialization.
```bash
python3 ./client/test_simulation_invocation.py
```

## License
This project is licensed under the [MIT License](LICENSE).


