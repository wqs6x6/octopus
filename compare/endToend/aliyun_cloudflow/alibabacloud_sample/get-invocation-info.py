# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_fnf20190315.client import Client as fnf20190315Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_fnf20190315 import models as fnf_20190315_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import pandas as pd  # Import pandas library
from datetime import datetime
import json
import matplotlib.pyplot as plt  # Add this line
import numpy as np  # Add this line

MY_ALIYUN_ACCESS_KEY_ID = "********"
MY_ALIYUN_ACCESS_KEY_SECRET = "********"

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps1000"
# RPS = 1000

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps500"
# RPS = 500

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps100"
# RPS = 100

EXECUTION_NAME_TEMPLATE = "octopus-seq10-3-rps50"
RPS = 50

# EXECUTION_NAME_TEMPLATE = "octopus-seq10-2-rps10"
# RPS = 10

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> fnf20190315Client:
        """
        Initialize account Client using AK&SK
        @return: Client
        @throws Exception
        """
        # Leaking project code may lead to AccessKey leakage and threaten the security of all resources under the account. The following code example is for reference only.
        # It is recommended to use a more secure STS method. For more authentication access methods, please refer to: https://help.aliyun.com/document_detail/378659.html.
        config = open_api_models.Config(
            # Required, please ensure that the environment variable ALIBABA_CLOUD_ACCESS_KEY_ID is set in the code running environment.
            access_key_id=MY_ALIYUN_ACCESS_KEY_ID,
            # Required, please ensure that the environment variable ALIBABA_CLOUD_ACCESS_KEY_SECRET is set in the code running environment.
            access_key_secret=MY_ALIYUN_ACCESS_KEY_SECRET
        )
        # For endpoint, please refer to https://api.aliyun.com/product/fnf
        config.endpoint = f'cn-shenzhen.fnf.aliyuncs.com'
        return fnf20190315Client(config)

    @staticmethod
    def process_response(response):
        """
        Process API response, extract Request ID, StartedTime, and StoppedTime, and calculate execution time.
        Return result data.
        """

        response_dict = response.to_map()
        # print(response_dict,type(response_dict))
        RequestID = response_dict["body"]["RequestId"]
        # print(RequestID)
        started_time = response_dict['body']['StartedTime']
        stopped_time = response_dict['body']['StoppedTime']
        # print(started_time,stopped_time)

        started_time = datetime.fromisoformat(started_time.replace("Z", "+00:00"))
        stopped_time = datetime.fromisoformat(stopped_time.replace("Z", "+00:00"))
        execution_time = (stopped_time - started_time).total_seconds()
        # print(execution_time)
        # Create result data
        result_data = {
            "RequestID": RequestID,
            "ExecutionTime": execution_time
        }
        
        return result_data  # Return result data

    @staticmethod
    def ensure_output_dir():
        """
        Ensure the output directory exists, create it if it does not exist
        """
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    @staticmethod
    def get_output_path(filename: str) -> str:
        """
        Get the full path of the output file
        
        Args:
            filename: File name
        Returns:
            str: Full output path
        """
        return os.path.join(os.path.dirname(__file__), 'output', filename)

    @staticmethod
    def plot_cdf(df: pd.DataFrame, output_file: str = 'execution_time_cdf.png') -> None:
        """
        Plot the CDF distribution of execution time
        
        Args:
            df: DataFrame containing the ExecutionTime column
            output_file: Output image file name
        """
        # Ensure the output directory exists
        Sample.ensure_output_dir()
        
        # Calculate statistical metrics
        execution_times = df['ExecutionTime'].sort_values()
        stats = {
            'Mean': execution_times.mean(),
            'Median': execution_times.median(),
            'Min': execution_times.min(),
            'Max': execution_times.max(),
            '95th Percentile': execution_times.quantile(0.95),
            '99th Percentile': execution_times.quantile(0.99)
        }
        
        # Calculate CDF
        n = len(execution_times)
        cumulative_prob = np.arange(1, n + 1) / n
        
        # Save CDF data to CSV
        cdf_df = pd.DataFrame({
            'ExecutionTime': execution_times.values,
            'CumulativeProbability': cumulative_prob
        })
        cdf_df.to_csv(Sample.get_output_path(f"{EXECUTION_NAME_TEMPLATE}_cdf.csv"), index=False)
        
        # Create chart
        plt.figure(figsize=(12, 8))
        plt.plot(execution_times, cumulative_prob, 
                marker='.', 
                linestyle='-', 
                linewidth=2, 
                color='#1f77b4',
                label='CDF')
        
        # Set chart style
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xlabel('Execution Time (seconds)', fontsize=12)
        plt.ylabel('Cumulative Probability', fontsize=12)
        plt.title(f'Execution Time CDF Distribution ({EXECUTION_NAME_TEMPLATE})', fontsize=14, pad=20)
        
        # Add statistical information text box
        stats_text = '\n'.join([f'{k}: {v:.2f}s' for k, v in stats.items()])
        plt.text(0.02, 0.98, stats_text,
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', 
                         edgecolor='#666666',
                         alpha=0.8,
                         boxstyle='round,pad=0.5'),
                fontsize=10,
                verticalalignment='top')
        
        # Set axis range and ticks
        plt.xlim(left=0)
        plt.ylim(0, 1.05)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Print statistical information
        print("\nStatistical Information:")
        for k, v in stats.items():
            print(f"{k}: {v:.2f}s")

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        # Ensure the output directory exists
        Sample.ensure_output_dir()
        
        client = Sample.create_client()
        describe_execution_request_template = fnf_20190315_models.DescribeExecutionRequest(
            flow_name='test-end-to-end',
        )
        # Print detailed information of describe_execution_request
        runtime = util_models.RuntimeOptions()
        
        # Specify index range
        index_range = range(1, RPS+1)  # For example, 1 to 5

        all_results = []  # Used to store all results

        for index in index_range:
            execution_name = f'{EXECUTION_NAME_TEMPLATE}-{index}'  # Format execution_name
            describe_execution_request = describe_execution_request_template
            describe_execution_request.execution_name = execution_name
            
            print("DescribeExecutionRequest:", describe_execution_request.to_map())
            
            try:
                # Call API and get return value
                response = client.describe_execution_with_options(describe_execution_request, runtime)
                # Print detailed return information
                print("Execution Details for", execution_name, ":", response, type(response))

                # Call the function to process the response and get the result
                result_data = Sample.process_response(response)
                all_results.append(result_data)  # Add the result to the list

            except Exception as error:
                # Use str(error) to get error information
                print("Error:", str(error))
                # Diagnostic address
                if hasattr(error, 'data') and 'Recommend' in error.data:
                    print("Recommendation:", error.data.get("Recommend"))
                UtilClient.assert_as_string(str(error))

        # Write all results to CSV (modify save path)
        print(all_results)
        df = pd.DataFrame(all_results)
        df.to_csv(Sample.get_output_path(f"{EXECUTION_NAME_TEMPLATE}.csv"), index=False)
        
        # Call the plotting function (use full path)
        Sample.plot_cdf(df, Sample.get_output_path(f"{EXECUTION_NAME_TEMPLATE}.png"))

if __name__ == '__main__':
    Sample.main(sys.argv[1:])