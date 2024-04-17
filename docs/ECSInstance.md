# ECSInstance 类文档

## 概述

`ECSInstance` 是一个用于管理阿里云ECS（弹性计算服务）实例的Python类。它提供了一组属性和方法，用于与ECS实例进行交互和操作。

### 属性

- `instance_id`：ECS实例的唯一标识符。
- `description`：ECS实例的描述。
- `memory`：分配给ECS实例的内存大小，以MiB（兆字节）为单位。
- `instance_charge_type`：ECS实例的计费类型。
- `cpu`：分配给ECS实例的CPU核心数量。
- `instance_network_type`：ECS实例的网络类型。
- `public_ip_address`：与ECS实例关联的公网IP地址列表。
- `inner_ip_address`：与ECS实例关联的内网IP地址列表。
- `enable_jumbo_frame`：一个布尔值，表示是否在ECS实例上启用了巨帧。
- `expired_time`：ECS实例的过期时间。
- `image_id`：ECS实例使用的镜像ID。
- `eip_address`：包含EIP（弹性IP）地址信息的字典。
- `instance_type`：ECS实例的类型。
- `vlan_id`：ECS实例的VLAN ID。
- `host_name`：ECS实例的主机名。
- `status`：ECS实例当前的状态。
- `io_optimized`：表示实例是否具有I/O优化。
- `request_id`：与ECS实例API调用关联的请求ID。
- `zone_id`：部署了ECS实例的区域ID。
- `cluster_id`：ECS实例所属的集群ID。
- `stopped_mode`：ECS实例的停止模式。
- `dedicated_host_attribute`：包含专有宿主机属性的字典。
- `security_group_ids`：与ECS实例关联的安全组ID列表。
- `vpc_attributes`：包含VPC（虚拟私有云）属性的字典。
- `operation_locks`：包含操作锁定细节的字典。
- `internet_charge_type`：网络使用的互联网计费类型。
- `instance_name`：ECS实例的名称。
- `internet_max_bandwidth_out`：实例最大出站互联网带宽，以Mbps计。
- `serial_number`：ECS实例的序列号。
- `internet_max_bandwidth_in`：实例最大入站互联网带宽，以Mbps计。
- `creation_time`：ECS实例的创建时间。
- `region_id`：部署了ECS实例的地域ID。
- `credit_specification`：ECS实例的信用规格。

### 方法

#### `from_json(data)`
静态方法，从JSON数据创建`ECSInstance`的实例。

参数：
- `data`：包含ECS实例信息的字典。

返回值：
- 一个`ECSInstance`的实例。

#### `syncRun(cmd_content, timeout=600)`
在ECS实例上同步运行命令。

参数：
- `cmd_content`：要运行的命令内容。
- `timeout`：命令执行的超时时间，以秒为单位。

返回值：
- 运行命令的结果。

#### `asyncRun(cmd_content, timeout=600)`
在ECS实例上异步运行命令。

参数：
- `cmd_content`：要运行的命令内容。
- `timeout`：命令执行的超时时间，以秒为单位。

返回值：
- 运行命令的结果。

#### `attachNewDisk()`
方法用于将新磁盘附加到ECS实例（未展示实现）。

#### `release()`
释放ECS实例，从阿里云ECS中删除它。

## 示例

以下示例展示了如何使用`ECSInstance`类：

### 从JSON数据创建ECSInstance对象

```python
instance_data = {
    "InstanceId": "i-1234567890abcdef",
    "Memory": 