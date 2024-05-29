from handyhelpers.aliyun.ECSManager import ECSManager
from handyhelpers.aliyun.RunECSInstanceSettings import RunECSInstanceSettings
from handyhelpers.aliyun.DNSService import DNSService
import time

ecs_manager = ECSManager(region_id='cn-hangzhou')
instances = ecs_manager.listInstances()
indentifier_name = 'host-name'

instance = next(
    (instance for instance in instances if instance.host_name == indentifier_name), 
    None)

if instance is None:
    instance = ecs_manager.runInstance(RunECSInstanceSettings(
        host_name=indentifier_name, 
        instance_type="ecs.u1-c1m2.large",
        image_id="aliyun_3_9_x64_20G_alibase_20231219.vhd",
        spot_strategy = "SpotAsPriceGo",
        password="your_pass"
        ))

time.sleep(20) # 公网IP分配需要时间

dns_service = DNSService()
dns_service.updateDNSRecordValue(
    domain_name="your.domain.net", 
    rr_name="subname", 
    new_value="127.0.0.1")