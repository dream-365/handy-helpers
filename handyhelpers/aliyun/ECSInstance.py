from .RunCommandHelper import RunCommandHelper
from .ClientProvider import ClientProvider
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.DeleteInstancesRequest import DeleteInstancesRequest
from aliyunsdkecs.request.v20140526.CreateDiskRequest import CreateDiskRequest
from aliyunsdkecs.request.v20140526.AttachDiskRequest import AttachDiskRequest
from aliyunsdkecs.request.v20140526.RebootInstanceRequest import RebootInstanceRequest
import json

class ECSInstance:
    def __init__(self):
        self.instance_id = ""
        self.description = ""
        self.memory = 0
        self.instance_charge_type = ""
        self.cpu = 0
        self.instance_network_type = ""
        self.public_ip_address = []
        self.inner_ip_address = []
        self.enable_jumbo_frame = False
        self.expired_time = ""
        self.image_id = ""
        self.eip_address = {}
        self.instance_type = ""
        self.vlan_id = ""
        self.host_name = ""
        self.status = ""
        self.io_optimized = ""
        self.request_id = ""
        self.zone_id = ""
        self.cluster_id = ""
        self.stopped_mode = ""
        self.dedicated_host_attribute = {}
        self.security_group_ids = []
        self.vpc_attributes = {}
        self.operation_locks = {}
        self.internet_charge_type = ""
        self.instance_name = ""
        self.internet_max_bandwidth_out = 0
        self.serial_number = ""
        self.internet_max_bandwidth_in = 0
        self.creation_time = ""
        self.region_id = ""
        self.credit_specification = ""

    @staticmethod
    def from_json(data):
        instance = ECSInstance() 
        instance.description = data.get("Description", "")
        instance.memory = data.get("Memory", 0)
        instance.instance_charge_type = data.get("InstanceChargeType", "")
        instance.cpu = data.get("Cpu", 0)
        instance.instance_network_type = data.get("InstanceNetworkType", "")
        instance.public_ip_address = data.get("PublicIpAddress", {}).get("IpAddress", [])
        instance.inner_ip_address = data.get("InnerIpAddress", {}).get("IpAddress", [])
        instance.enable_jumbo_frame = data.get("EnableJumboFrame", False)
        instance.expired_time = data.get("ExpiredTime", "")
        instance.image_id = data.get("ImageId", "")
        instance.eip_address = data.get("EipAddress", {})
        instance.instance_type = data.get("InstanceType", "")
        instance.vlan_id = data.get("VlanId", "")
        instance.host_name = data.get("HostName", "")
        instance.status = data.get("Status", "")
        instance.io_optimized = data.get("IoOptimized", "")
        instance.request_id = data.get("RequestId", "")
        instance.zone_id = data.get("ZoneId", "")
        instance.cluster_id = data.get("ClusterId", "")
        instance.instance_id = data.get("InstanceId", "")
        instance.stopped_mode = data.get("StoppedMode", "")
        instance.dedicated_host_attribute = data.get("DedicatedHostAttribute", {})
        instance.security_group_ids = data.get("SecurityGroupIds", {}).get("SecurityGroupId", [])
        instance.vpc_attributes = data.get("VpcAttributes", {})
        instance.operation_locks = data.get("OperationLocks", {})
        instance.internet_charge_type = data.get("InternetChargeType", "")
        instance.instance_name = data.get("InstanceName", "")
        instance.internet_max_bandwidth_out = data.get("InternetMaxBandwidthOut", 0)
        instance.serial_number = data.get("SerialNumber", "")
        instance.internet_max_bandwidth_in = data.get("InternetMaxBandwidthIn", 0)
        instance.creation_time = data.get("CreationTime", "")
        instance.region_id = data.get("RegionId", "")
        instance.credit_specification = data.get("CreditSpecification", "")
        return instance
    
    def run(self, cmd_content, name=None, timeout=600, tags=None):
        return RunCommandHelper(self.region_id).run(
            instance_id=self.instance_id, 
            cmd_content=cmd_content, 
            name=name,
            tags=tags,
            timeout=timeout)
    
    def runAndWaitForCompletion(self, cmd_content, name=None, timeout=600, tags=None):
        return RunCommandHelper(self.region_id).runAndWaitForCompletion(
            instance_id=self.instance_id, 
            cmd_content=cmd_content, 
            name=name, 
            tags=tags,
            timeout=timeout)


    def attachNewDisk(self, disk_size, disk_category, performance_level=None, delete_with_instance=True):
        client = ClientProvider.getClient(self.region_id)
        # 创建一块新的云盘
        create_disk_request = CreateDiskRequest()
        create_disk_request.set_ZoneId(self.zone_id)  # 设置创建云盘的区域ID和可用区ID
        create_disk_request.set_Size(disk_size)  # 设置云盘大小，单位为GiB
        create_disk_request.set_DiskCategory(disk_category)  # 设置云盘类型，可选cloud | cloud_efficiency | cloud_ssd | cloud_essd | etc.

        if performance_level is not None:
            create_disk_request.set_PerformanceLevel(performance_level)

        # 发送请求并处理响应或异常
        try:
            create_disk_response = client.do_action_with_exception(create_disk_request)
            create_disk_response_decoded = json.loads(create_disk_response)
            # 解析云盘ID，用于后续挂载操作
            disk_id = create_disk_response_decoded['DiskId']
        except ServerException as e:
            print("Create Disk Failed:", e)
        except ClientException as e:
            print("Create Disk Failed:", e)

        # 将创建的云盘附加到ECS实例上
        attach_disk_request = AttachDiskRequest()
        attach_disk_request.set_InstanceId(self.instance_id)
        attach_disk_request.set_DiskId(disk_id)  # 使用之前创建云盘的云盘ID
        attach_disk_request.set_DeleteWithInstance(delete_with_instance)
        # 发送请求并处理响应或异常
        try:
            client.do_action_with_exception(attach_disk_request)
        except ServerException as e:
            print("Attach Disk Failed:", e)
        except ClientException as e:
            print("Attach Disk Failed:", e)
    
    def reboot(self, force_stop=False):
        client = ClientProvider.getClient(self.region_id)
        reboot_instance_request = RebootInstanceRequest()
        reboot_instance_request.set_InstanceId(self.instance_id)
        reboot_instance_request.set_ForceStop(force_stop)
        client.do_action_with_exception(reboot_instance_request)

        pass

    def release(self):
        client = ClientProvider.getClient(self.region_id)
        delete_instance_request = DeleteInstancesRequest()
        delete_instance_request.set_accept_format('json')
        delete_instance_request.set_InstanceIds([self.instance_id])
        delete_instance_request.set_Force(True)

        client.do_action_with_exception(delete_instance_request)