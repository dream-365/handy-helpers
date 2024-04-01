from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
import os

class ClientProvider:
    @staticmethod
    def getClient(region_id):
        credentials = AccessKeyCredential(os.environ.get("ACCESS_KEY"), os.environ.get("ACCESS_SECRET"))
        return AcsClient(region_id=region_id, credential=credentials)