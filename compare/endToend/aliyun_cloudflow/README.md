# 异步调用开始一个流程的执行完整工程示例

该项目为StartExecution的完整工程示例。

该示例**无法在线调试**，如需调试可下载到本地后替换 [AK](https://usercenter.console.aliyun.com/#/manage/ak) 以及参数后进行调试。

## 运行条件

- 下载并解压需要语言的代码;


- 在阿里云帐户中获取您的 [凭证](https://usercenter.console.aliyun.com/#/manage/ak) 并通过它替换下载后代码中的 ACCESS_KEY_ID 以及 ACCESS_KEY_SECRET;

- 执行对应语言的构建及运行语句

## 执行步骤

下载的代码包，在根据自己需要更改代码中的参数和 AK 以后，可以在**解压代码所在目录下**按如下的步骤执行：

- *Python 版本要求 Python3*
```sh
python3 setup.py install && python ./alibabacloud_sample/sample.py
```
## 使用的 API

-  StartExecution：开始一个流程的执行。 更多信息可参考：[文档](https://next.api.aliyun.com/document/fnf/2019-03-15/StartExecution)

## API 返回示例

*实际输出结构可能稍有不同，属于正常返回；下列输出值仅作为参考，以实际调用为准*


- JSON 格式 
```js
{
  "Status": "Succeeded",
  "StoppedTime": "2019-01-01T01:01:01.001Z",
  "RequestId": "testRequestId",
  "StartedTime": "2019-01-01T01:01:01.001Z",
  "FlowDefinition": "旧版：\n\"type: flow\\nversion: v1\\nname: my_flow_name\\nsteps:\\n  - type: pass\\n    name: mypass\"\n\n新版：\n\"Type: StateMachine\\nSpecVersion: v1\\nName: my_flow_name\\nStartAt: my_state\\nStates:\\n  - Type: Pass\\n    Name: my_state\\n    End: true\"",
  "Output": "{\"key\":\"value\"}",
  "FlowName": "my_flow_name",
  "Name": "my_exec_name",
  "Input": "{\"key\":\"value\"}"
}
```

