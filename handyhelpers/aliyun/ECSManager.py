from .ECSInstance import ECSInstance
from .RunECSInstanceSettings import RunECSInstanceSettings
from .ClientProvider import ClientProvider
import time
import json
import os
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeVSwitchesRequest import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest

class ECSManager:
    def __init__(self, region_id):
        self.region_id = region_id

    def __getDefaultVswitchId(self):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeVSwitchesRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        data = json.loads(str(response, encoding='utf-8'))
    
        if len(data['VSwitches']['VSwitch']):
            return data['VSwitches']['VSwitch'][0]['VSwitchId']
        
        return None
    
    def __getDefaultSecurityGroupId(self):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeSecurityGroupsRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        data = json.loads(str(response, encoding='utf-8'))
    
        if len(data['SecurityGroups']['SecurityGroup']):
            return data['SecurityGroups']['SecurityGroup'][0]['SecurityGroupId']
        
        return None
    
    def _createDefaultRunECSInstanceSettings(self):
        settings = RunECSInstanceSettings()

        default_vswitch_id = self.__getDefaultVswitchId()
        default_security_group_id = self.__getDefaultSecurityGroupId()
        settings.set_security_group_id(default_security_group_id)
        settings.set_vswitch_id(default_vswitch_id)
        settings.set_host_name('demo-001')
        settings.set_image_id("aliyun_3_x64_20G_qboot_alibase_20230727.vhd")
        settings.set_password(os.environ.get("VM_PASS"))
        settings.set_instance_type("ecs.g6.large")
        settings.set_biz_tags([])
        settings.set_system_disk_size(80)
        settings.set_system_disk_category("cloud_essd")
        settings.set_system_disk_performance_level("PL0")
        settings.set_spot_strategy("NoSpot")

        return settings
    
    def __runInstance(self, settings):
        client = ClientProvider.getClient(self.region_id)
        run_instances_request = RunInstancesRequest()
        run_instances_request.set_accept_format('json')
        run_instances_request.set_ImageId(settings.image_id)
        run_instances_request.set_InstanceType(settings.instance_type)
        run_instances_request.set_SystemDiskCategory(settings.system_disk_category)
        run_instances_request.set_SystemDiskPerformanceLevel(settings.system_disk_performance_level)
        run_instances_request.set_SystemDiskSize(settings.system_disk_size)
        run_instances_request.set_SecurityGroupId(settings.security_group_id)
        run_instances_request.set_VSwitchId(settings.vswitch_id)
        run_instances_request.set_InstanceName(settings.host_name)
        run_instances_request.set_InternetMaxBandwidthOut(100)
        run_instances_request.set_HostName(settings.host_name)
        run_instances_request.set_Password(settings.password)
        run_instances_request.set_SpotStrategy(settings.spot_strategy)
        run_instances_request.set_Tags(settings.biz_tags)

        run_instances_response = client.do_action_with_exception(run_instances_request)
        run_instances_response_json = json.loads(str(run_instances_response, encoding='utf-8'))
        instance_id = run_instances_response_json['InstanceIdSets']['InstanceIdSet'][0]

        time.sleep(10) # wait for public ip addr assignment

        return self.describeInstanceAttribute(instance_id=instance_id)
    
    def getOrCreateInstance(self, settings:RunECSInstanceSettings):
        pass

    def runInstance(self, settings:RunECSInstanceSettings):
        defualt_settings = self._createDefaultRunECSInstanceSettings()
        settings.merge_from(defualt_settings)
        return self.__runInstance(settings)
    
    def describeInstanceAttribute(self, instance_id):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instance_id)
        run_instances_response = client.do_action_with_exception(request)
        data = json.loads(str(run_instances_response, encoding='utf-8'))

        return ECSInstance.from_json(data)