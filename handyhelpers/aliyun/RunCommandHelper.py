import base64
import json
import time
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from .ClientProvider import ClientProvider

SECONDS_INTERVAL = 3

class CommandInvocationResult:
    """Represents the result of a command invocation."""
    def __init__(self, invocation_status, invoke_record_status, output):
        self.invocation_status = invocation_status
        self.invoke_record_status = invoke_record_status
        self.output = output

class RunCommandHelper:
    """Helper class to run commands on Alibaba Cloud ECS instances."""
    def __init__(self, region_id):
        """Initialize the RunCommandHelper class instance."""
        self.region_id = region_id

    def getInvocationResult(self, invocation_id):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeInvocationResultsRequest()
        request.set_accept_format('json')
        request.set_InvokeId(invocation_id)
        
        # 直接在方法调用中处理获取结果的逻辑
        results = self._parse_invocation_results(self._perform_request(client, request))
        
        # 使用 next(iter()) 来获取列表中的第一个元素，如果列表为空则返回 None
        return next(iter(results), None)
    
    def getInvocationResults(self, tags=None):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeInvocationResultsRequest()
        request.set_accept_format('json')
        converted_tags = [{"Key": k, "Value": v} for k, v in tags.items()] if tags is not None else []
        request.set_Tags(converted_tags)

        results = self._parse_invocation_results(self._perform_request(client, request))

        return results

    def asyncRun(self, instance_id, cmd_content, timeout, name=None, tags=None):
        client = ClientProvider.getClient(self.region_id)
        request = RunCommandRequest()
        request.set_accept_format('json')
        request.set_Type("RunShellScript")
        request.set_CommandContent(cmd_content)
        request.set_InstanceIds([instance_id])

        converted_tags = [{"Key": k, "Value": v} for k, v in tags.items()] if tags is not None else []
        request.set_Tags(converted_tags)

        request.set_Username("root")
        request.set_Timeout(timeout)

        if name is not None:
            request.set_Name(name)

        response = self._perform_request(client, request)
        return json.loads(response).get("InvokeId")

    def syncRun(self, instance_id, cmd_content, timeout, name=None, tags=None):
        invoke_id = self.asyncRun(instance_id=instance_id, 
                                  name=name, 
                                  cmd_content=cmd_content,
                                  tags=tags,
                                  timeout=timeout)
        while True:
            result = self.getInvocationResult(invoke_id)
            if result.invoke_record_status == "Finished":
                break
            time.sleep(SECONDS_INTERVAL)
        return result

    def _perform_request(self, client, request):
        """Perform a request using provided client and request objects."""
        response = client.do_action_with_exception(request)
        return response

    def _parse_invocation_results(self, response):
        """Parse the command invocation result from the response."""
        
        # 直接从 response 中解析出 invocation_results
        invocation_results = json.loads(response.decode('utf-8'))['Invocation']['InvocationResults']['InvocationResult']

        # 使用列表推导式生成结果列表
        return [CommandInvocationResult(
                    invocation_status=result['InvocationStatus'],
                    invoke_record_status=result['InvokeRecordStatus'],
                    output=base64.b64decode(result['Output']).decode('utf-8')
                ) for result in invocation_results]