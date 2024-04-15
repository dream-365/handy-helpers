from handyhelpers.aliyun.ECSManager import ECSManager
from handyhelpers.aliyun.RunECSInstanceSettings import RunECSInstanceSettings
import handyhelpers.scripts.linux.alilinux3.docker as docker_scripts

ecs_manager = ECSManager(region_id='cn-hangzhou')

instance = ecs_manager.runInstance(RunECSInstanceSettings(
    host_name="tf-notebook-cpu", 
    instance_type="ecs.g7.xlarge",
    spot_strategy="SpotAsPriceGo"
    # image_id="aliyun_3_9_x64_20G_uefi_alibase_20231219.vhd"
    ))

# run command
instance.syncRun(docker_scripts.install_docker)

pipeline = [
    {"name": "task1", "scripts": "script..."},
    {"name": "task2", "scripts": "script..."},
]

result = instance.runPipeline(pipeline)


result.getOutput("task name")