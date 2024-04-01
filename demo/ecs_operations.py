from handyhelpers.aliyun.ECSManager import ECSManager
from handyhelpers.aliyun.RunECSInstanceSettings import RunECSInstanceSettings
import time

ecs_manager = ECSManager(region_id='ap-southeast-1')
vm = ecs_manager.runInstance(RunECSInstanceSettings(host_name="demo"))
print(vm.public_ip_address[0])
reuslt = vm.syncRun("yum update -y")
print(reuslt.output)

vm.release()