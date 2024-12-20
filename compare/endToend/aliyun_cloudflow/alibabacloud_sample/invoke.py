# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
import asyncio  


from typing import List

from alibabacloud_fnf20190315.client import Client as fnf20190315Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_fnf20190315 import models as fnf_20190315_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

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
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=MY_ALIYUN_ACCESS_KEY_ID,
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=MY_ALIYUN_ACCESS_KEY_SECRET
        )
        # Endpoint 请参考 https://api.aliyun.com/product/fnf
        config.endpoint = f'cn-shenzhen.fnf.aliyuncs.com'
        return fnf20190315Client(config)

    # @staticmethod
    # def main(
    #     args: List[str],
    # ) -> None:
    #     client = Sample.create_client()
    #     start_execution_request = fnf_20190315_models.StartExecutionRequest(
    #         flow_name='test-end-to-end',
    #         execution_name='invocation-3',
    #         input='{"key1":20}'
    #     )
    #     runtime = util_models.RuntimeOptions()
    #     try:
    #         resp = client.start_execution_with_options(start_execution_request, runtime)
    #         ConsoleClient.log(UtilClient.to_jsonstring(resp))
    #     except Exception as error:
    #         # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
    #         # 错误 message
    #         print(error.message)
    #         # 诊断地址
    #         print(error.data.get("Recommend"))
    #         UtilClient.assert_as_string(error.message)

    @staticmethod
    async def send_execution(client, index: int) -> None:
        start_execution_request = fnf_20190315_models.StartExecutionRequest(
            flow_name='test-end-to-end',
            execution_name=f'{EXECUTION_NAME_TEMPLATE}-{index}',
            input=f'{{"key1":{30 + index}}}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = await client.start_execution_with_options_async(start_execution_request, runtime)
            # print(resp)  # 打印响应以便调试
            # 检查执行结果
            print("Response body:", resp.body)
            if resp and resp.body is not None:
                if resp.body.RequestId:
                    print(f"Execution {resp.body.RequestId} started successfully.")
                else:
                    print("Execution failed to start: 'RequestId' is empty in response body.")
            else:
                print("Execution failed to start: Invalid response structure.")
        except Exception as error:
            print(f"Error occurred: {str(error)}")
            print(error.data.get("Recommend") if hasattr(error, 'data') else "无诊断信息")

    @staticmethod
    async def main_async(
        args: List[str],
        request_count: int = RPS,
    ) -> None:
        client = Sample.create_client()
        tasks = [Sample.send_execution(client, i) for i in range(1, request_count + 1)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(Sample.main_async(sys.argv[1:]))
