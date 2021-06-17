#coding=utf-8 
# falcon
endpoint = "vcenter" # 上报给 open-falcon 的 endpoint
push_api = "http://127.0.0.1:6060/api/push" # 上报的 http api 接口
interval = 20  # 上报的 step 间隔

# vcenter
host = "192.168.16.167" # vcenter 的地址
user = "administrator@vsphere.local"  # vcenter 的用户名
pwd = "1qaz@WSX"  # vcenter 的密码
port = 443  # vcenter 的端口

# esxi
esxi_names = [] # 需要采集的 esxi ，留空则全部采集

# datastore
datastore_names = []  # 需要采集的 datastore ，留空则全部采集

# vm
vm_enable = True # 是否要采集虚拟机信息
# vm_names = [     # 需要采集的虚拟机，留空则全部采集
#             "vm1",
#             "vm2",
#             "vm3"
#            ]
vm_names = [     # 需要采集的虚拟机，留空则全部采集

           ]
