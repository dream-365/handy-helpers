import json
from aliyunsdkcore.client import AcsClient

class ApiUtils:
    @staticmethod
    def perform_request(client:AcsClient, request):
        """Perform a request using provided client and request objects."""
        response = client.do_action_with_exception(request)
        api_response = json.loads(response.decode('utf-8'))
        return api_response