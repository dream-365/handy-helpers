from .ClientProvider import ClientProvider
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
import json
import time
import base64

class CommandInvocationResult:
    def __init__(self, invocation_status, invoke_record_status, output):
        self.invocation_status = invocation_status
        self.invoke_record_status = invoke_record_status
        self.output = output

class RunCommandHelper:
    def __init__(self, region_id):
        self.region_id = region_id

    def asyncRun(self, instance_id, cmd_content, timeout):
        client = ClientProvider.getClient(self.region_id)
        request = RunCommandRequest()
        request.set_accept_format('json')
        request.set_Type("RunShellScript")
        request.set_CommandContent(cmd_content)
        request.set_InstanceIds([instance_id])
        request.set_Username("root")
        request.set_Timeout(timeout)

        response = client.do_action_with_exception(request)
        invoke_id = json.loads(response).get("InvokeId")

        return invoke_id

    def syncRun(self, instance_id, cmd_content, timeout):
        client = ClientProvider.getClient(self.region_id)
        invoke_id = self.asyncRun(instance_id, cmd_content, timeout)

        request = DescribeInvocationResultsRequest()
        request.set_accept_format('json')
        request.set_InvokeId(invoke_id)
        invoke_record_status = ''
        invocation_status = ''
        invocation_output = ''

        while invoke_record_status != "Finished":
            time.sleep(3)
            response = client.do_action_with_exception(request)
            data = json.loads(str(response, encoding='utf-8'))
            invocation_result = data['Invocation']['InvocationResults']['InvocationResult'][0]
            base64_output = invocation_result['Output']
            invocation_status = invocation_result['InvocationStatus']
            invoke_record_status = invocation_result['InvokeRecordStatus']
            decoded_bytes = base64.b64decode(base64_output)
            invocation_output = decoded_bytes.decode('utf-8')

        return CommandInvocationResult(invocation_status=invocation_status, 
                                       invoke_record_status=invoke_record_status, 
                                       output=invocation_output)