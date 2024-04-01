class RunECSInstanceSettings:
    def __init__(self, image_id=None, instance_type=None, system_disk_size=None, system_disk_category=None, system_disk_performance_level=None,
                 security_group_id=None, vswitch_id=None, host_name=None, password=None, biz_tags=None, spot_strategy=None):
        self.image_id = image_id
        self.instance_type = instance_type
        self.system_disk_size = system_disk_size
        self.system_disk_category = system_disk_category
        self.system_disk_performance_level = system_disk_performance_level
        self.security_group_id = security_group_id
        self.vswitch_id = vswitch_id
        self.host_name = host_name
        self.password = password
        self.biz_tags = biz_tags
        self.spot_strategy = spot_strategy

    def set_image_id(self, image_id):
        self.image_id = image_id

    def set_instance_type(self, instance_type):
        self.instance_type = instance_type

    def set_system_disk_size(self, system_disk_size):
        self.system_disk_size = system_disk_size

    def set_system_disk_category(self, system_disk_category):
        self.system_disk_category = system_disk_category

    def set_system_disk_performance_level(self, system_disk_performance_level):
        self.system_disk_performance_level = system_disk_performance_level

    def set_security_group_id(self, security_group_id):
        self.security_group_id = security_group_id

    def set_vswitch_id(self, vswitch_id):
        self.vswitch_id = vswitch_id

    def set_host_name(self, host_name):
        self.host_name = host_name

    def set_password(self, password):
        self.password = password

    def set_biz_tags(self, biz_tags):
        self.biz_tags = biz_tags

    def set_spot_strategy(self, spot_strategy):
        self.spot_strategy = spot_strategy

    def merge_from(self, other):
        if isinstance(other, RunECSInstanceSettings):
            for attribute in vars(self):
                if getattr(self, attribute) is None:
                    setattr(self, attribute, getattr(other, attribute))