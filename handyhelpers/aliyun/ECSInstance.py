from .RunCommandHelper import RunCommandHelper
from .ClientProvider import ClientProvider
from aliyunsdkecs.request.v20140526.DeleteInstancesRequest import DeleteInstancesRequest

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

    def syncRun(self, cmd_content, timeout=600):
        return RunCommandHelper(self.region_id).syncRun(self.instance_id, cmd_content, timeout=timeout)
    
    def asyncRun(self, cmd_content, timeout=600):
        return RunCommandHelper(self.region_id).asyncRun(self.instance_id, cmd_content, timeout=timeout)

    def attachNewDisk(self):
        pass

    def release(self):
        client = ClientProvider.getClient(self.region_id)
        delete_instance_request = DeleteInstancesRequest()
        delete_instance_request.set_accept_format('json')
        delete_instance_request.set_InstanceIds([self.instance_id])
        delete_instance_request.set_Force(True)

        client.do_action_with_exception(delete_instance_request)