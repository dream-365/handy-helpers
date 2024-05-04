import base64
import json
import time
import math
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from .ClientProvider import ClientProvider

SECONDS_INTERVAL = 3
DEFAULT_PAGE_SIZE = 20

class CommandInvocationResult(object):
    def __init__(self, dropped, invocation_status, instance_id, exit_code, 
                 error_info, start_time, repeats, invoke_record_status, 
                 finished_time, username, container_id, container_name, 
                 output, command_id, error_code, invoke_id, tags, stop_time):
        self.dropped = dropped
        self.invocation_status = invocation_status
        self.instance_id = instance_id
        self.exit_code = exit_code
        self.error_info = error_info
        self.start_time = start_time
        self.repeats = repeats
        self.invoke_record_status = invoke_record_status
        self.finished_time = finished_time
        self.username = username
        self.container_id = container_id
        self.container_name = container_name
        self.output = output
        self.command_id = command_id
        self.error_code = error_code
        self.invoke_id = invoke_id
        self.tags = tags
        self.stop_time = stop_time

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
    
    def getInvocationResults(self, tags=None, invoke_record_status=None):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeInvocationResultsRequest()
        request.set_accept_format('json')
        converted_tags = [{"Key": k, "Value": v} for k, v in tags.items()] if tags is not None else []
        request.set_Tags(converted_tags)
        
        if invoke_record_status is not None:
            request.set_InvokeRecordStatus(invoke_record_status)

        # 初始化分页数和结果存储变量
        page_number = 1
        all_results = []

        while True:
            request.set_PageNumber(page_number)
            request.set_PageSize(DEFAULT_PAGE_SIZE)  # 或者根据API的实际上限进行设置

            api_response = self._perform_request(client, request)

            # 处理当前页的结果
            current_results = self._parse_invocation_results(api_response)
            all_results.extend(current_results) 

            # 更新分页信息
            total_count = api_response["Invocation"]["TotalCount"]
            page_size = api_response["Invocation"]["PageSize"]

            # 计算总页数
            total_pages = math.ceil(total_count / page_size)
            
            # 如果当前页是最后一页，则退出循环
            if page_number >= total_pages:
                break

            # 否则，继续获取下一页
            page_number += 1
        
        # 返回所有结果
        return all_results

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
        api_response = json.loads(response.decode('utf-8'))
        return api_response

    def _parse_invocation_results(self, api_response):
        """Parse the command invocation result from the response."""
        invocation_results = []
        for item in api_response["Invocation"]["InvocationResults"]["InvocationResult"]:
            tags_dict = {tag["TagKey"]: tag["TagValue"] for tag in item.get("Tags", {}).get("Tag", [])}
            decoded_output = base64.b64decode(item.get("Output")).decode('utf-8')
            result = CommandInvocationResult(
                dropped=item.get("Dropped"),
                invocation_status=item.get("InvocationStatus"),
                instance_id=item.get("InstanceId"),
                exit_code=item.get("ExitCode", 0),  # 考虑默认值
                error_info=item.get("ErrorInfo", ""),
                start_time=item.get("StartTime"),
                repeats=item.get("Repeats"),
                invoke_record_status=item.get("InvokeRecordStatus"),
                finished_time=item.get("FinishedTime", ""),
                username=item.get("Username"),
                container_id=item.get("ContainerId", ""),
                container_name=item.get("ContainerName", ""),
                output=decoded_output,
                command_id=item.get("CommandId"),
                error_code=item.get("ErrorCode", ""),
                invoke_id=item.get("InvokeId"),
                tags=tags_dict,
                stop_time=item.get("StopTime", "")
            )
                
            invocation_results.append(result)

        return invocation_results