import base64
import json
import time
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from .ClientProvider import ClientProvider

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
        response = self._perform_request(client, request)
        return self._parse_invocation_result(response)

    def asyncRun(self, instance_id, cmd_content, timeout):
        client = ClientProvider.getClient(self.region_id)
        request = RunCommandRequest()
        request.set_accept_format('json')
        request.set_Type("RunShellScript")
        request.set_CommandContent(cmd_content)
        request.set_InstanceIds([instance_id])
        request.set_Username("root")
        request.set_Timeout(timeout)
        response = self._perform_request(client, request)
        return json.loads(response).get("InvokeId")

    def syncRun(self, instance_id, cmd_content, timeout):
        invoke_id = self.asyncRun(instance_id, cmd_content, timeout)
        while True:
            result = self.getInvocationResult(invoke_id)
            if result.invoke_record_status == "Finished":
                break
            time.sleep(3)
        return result

    def _perform_request(self, client, request):
        """Perform a request using provided client and request objects."""
        response = client.do_action_with_exception(request)
        return response

    def _parse_invocation_result(self, response):
        """Parse the command invocation result from the response."""
        data = json.loads(response.decode('utf-8'))
        invocation_result = data['Invocation']['InvocationResults']['InvocationResult'][0]
        output = base64.b64decode(invocation_result['Output']).decode('utf-8')
        return CommandInvocationResult(
            invocation_status=invocation_result['InvocationStatus'],
            invoke_record_status=invocation_result['InvokeRecordStatus'],
            output=output
        )