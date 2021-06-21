from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect

import atexit


from home_application.models import Esix, EsixVm


# vcenter
host = "192.168.16.167"  # vcenter 的地址
user = "administrator@vsphere.local"  # vcenter 的用户名
pwd = "1qaz@WSX"  # vcenter 的密码
port = 443  # vcenter 的端口

si = SmartConnectNoSSL(
    host=host,
    user=user,
    pwd=pwd,
    port=port)

atexit.register(Disconnect, si)

content = si.RetrieveContent()
# print(content)
container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)


def get_esxi():
    """
    获取esxi和esxiVm的数据
    """
    esxiDict = {}
    esxiVmDict = {}
    # 获取esxi
    esxiList = [esxi for esxi in container.view]
    # 用于存放esxi名
    esxi_li = []
    # 用于存放esxi下服务器名
    esxiVm_li = []
    for esxi in esxiList:
        # 获取esxi的名字
        esxiName = esxi.name
        esxi_li.append(esxi.name)
        # 获取esxi的cpu的处理器的数量
        numCpuPkgs = esxi.summary.hardware.numCpuPkgs
        # 获取esxi的cpu核数
        numCpuCores = esxi.summary.hardware.numCpuCores
        # 获取esxi的cpu的频率(最大值)
        cpuMhz = esxi.summary.hardware.cpuMhz
        # 获取esxi的cpu的使用情况
        cpuUsage = esxi.summary.quickStats.overallCpuUsage
        # 计算cpu的使用率
        cpuUsagePercent = '%.1f%%' % (cpuUsage / (numCpuCores * numCpuCores * cpuMhz) * 100)
        # 获取esxi内存的最大值(GB)
        maxMemory = int(esxi.summary.hardware.memorySize / 1024 / 1024 / 1024)
        # 获取esxi内存的使用情况
        memoryUsage = int(esxi.summary.quickStats.overallMemoryUsage / 1024 / 1024 / 1024)
        # 获取esxi的内存的使用率
        memoryUsagePercent = '%.1f%%' % (memoryUsage / maxMemory * 100)
        # 获取esxi磁盘的使用率
        total_capacity = 0
        free_capacity = 0
        for ds in esxi.datastore:
            # 磁盘的总容量，转换为GB
            total_capacity += int(ds.summary.capacity / 1024 / 1024 / 1024)
            # 磁盘的剩余容量，转换为GB
            free_capacity += int(ds.summary.freeSpace / 1024 / 1024 / 1024)
        storage_percent = '%.1f%%' % (100 * (total_capacity - free_capacity) / total_capacity)

        # 保存
        esxiDict[esxiName] = {}
        esxiDict[esxiName]['esxiName'] = esxiName
        esxiDict[esxiName]['numCpuPkgs'] = numCpuPkgs
        esxiDict[esxiName]['numCpuCores'] = numCpuCores
        esxiDict[esxiName]['cpuMhz'] = cpuMhz
        esxiDict[esxiName]['cpuUsagePercent'] = cpuUsagePercent
        esxiDict[esxiName]['maxMemory'] = maxMemory
        esxiDict[esxiName]['memoryUsage'] = memoryUsage
        esxiDict[esxiName]['memoryUsagePercent'] = memoryUsagePercent
        esxiDict[esxiName]['storage_percent'] = storage_percent

        # 获取esxi下的所有虚拟机
        esxiVmList = esxi.vm
        # 存储每一个esxi下的虚拟机
        each_esxiVm_li = []
        for esxiVm in esxiVmList:
            if esxiVm.runtime.powerState == 'poweredOn':
                # 获取名字
                esxiVmName = esxiVm.name
                each_esxiVm_li.append(esxiVm.name)
                # 获取cpu的核数
                numCpu = esxiVm.config.hardware.numCPU
                # 虚拟机cpu的使用情况MHZ
                vmCpuUsage = esxiVm.summary.quickStats.overallCpuUsage
                # 虚拟机cpu的demand
                vmCpuDemand = esxiVm.summary.quickStats.overallCpuDemand
                # 虚拟机cpu的最大值MHZ
                maxVmCpuUsage = esxiVm.runtime.maxCpuUsage
                # 虚拟机内存的最大值
                maxVmMemoryUsage = esxiVm.runtime.maxMemoryUsage
                # 虚拟机内存的使用情况
                vmMemoryUsage = esxiVm.summary.quickStats.guestMemoryUsage
                # 计算虚拟机cpu的使用率
                vmCpuUsagePercent = '%.1f%%' % (vmCpuUsage / maxVmCpuUsage * 100)
                # 获取虚拟机内存的使用率
                vmMemoryUsagePercent = '%.1f%%' % (vmMemoryUsage / maxVmMemoryUsage * 100)
                # 虚拟机磁盘的使用率
                total_capacity = 0
                free_capacity = 0
                for ds in esxiVm.datastore:
                    # 磁盘的总容量，转换为GB
                    total_capacity += int(ds.summary.capacity / 1024 / 1024 / 1024)
                    # 磁盘的剩余容量，转换为GB
                    free_capacity += int(ds.summary.freeSpace / 1024 / 1024 / 1024)
                storage_percent = '%.1f%%' % (100*(total_capacity - free_capacity)/total_capacity)

                # 保存
                esxiVmDict[esxiVmName] = {}
                esxiVmDict[esxiVmName]['esxiVmName'] = esxiVmName
                esxiVmDict[esxiVmName]['numCpu'] = numCpu
                esxiVmDict[esxiVmName]['vmCpuUsage'] = vmCpuUsage
                esxiVmDict[esxiVmName]['vmCpuDemand'] = vmCpuDemand
                esxiVmDict[esxiVmName]['maxVmCpuUsage'] = maxVmCpuUsage
                esxiVmDict[esxiVmName]['maxVmMemoryUsage'] = maxVmMemoryUsage
                esxiVmDict[esxiVmName]['vmMemoryUsage'] = vmMemoryUsage
                esxiVmDict[esxiVmName]['vmCpuUsagePercent'] = vmCpuUsagePercent
                esxiVmDict[esxiVmName]['vmMemoryUsagePercent'] = vmMemoryUsagePercent
                esxiVmDict[esxiVmName]['storage_percent'] = storage_percent
        # 存储将不同的esxi下的虚拟机归类
        esxiVm_li.append(each_esxiVm_li)

    return esxiDict, esxiVmDict, esxi_li, esxiVm_li


def save_esxi_data():
    """
    保存esxi的数据
    """
    esxiDict, esxiVmDict, esxi_li, esxiVm_li = get_esxi()
    # 存储esxi实例
    esxiInstance = []
    # 保存esxi
    for each_esxi in esxi_li:
        esxi = Esix()
        esxiInstance.append(esxi)
        esxi.name = esxiDict[each_esxi]['esxiName']
        esxi.numCpuPkgs = esxiDict[each_esxi]['numCpuPkgs']
        esxi.numCpuCores = esxiDict[each_esxi]['numCpuCores']
        esxi.cpuMhz = esxiDict[each_esxi]['cpuMhz']
        esxi.cpuUsagePercent = esxiDict[each_esxi]['cpuUsagePercent']
        esxi.maxMemory = esxiDict[each_esxi]['maxMemory']
        esxi.memoryUsage = esxiDict[each_esxi]['memoryUsage']
        esxi.memoryUsagePercent = esxiDict[each_esxi]['memoryUsagePercent']
        esxi.storage_percent = esxiDict[each_esxi]['storage_percent']
        esxi.save()

    # 保存esxi下的虚拟机
    for i, each_esxiVm_list in enumerate(esxiVm_li):
        for each_esxiVm in each_esxiVm_list:
            esxiVm = EsixVm()
            esxiVm.esixName = esxiInstance[i]
            esxiVm.vmName = esxiVmDict[each_esxiVm]['esxiVmName']
            esxiVm.maxVmCpuUsage = esxiVmDict[each_esxiVm]['maxVmCpuUsage']
            esxiVm.numCpu = esxiVmDict[each_esxiVm]['numCpu']
            esxiVm.storage_percent = esxiVmDict[each_esxiVm]['storage_percent']
            esxiVm.vmCpuDemand = esxiVmDict[each_esxiVm]['vmCpuDemand']
            esxiVm.vmCpuUsage = esxiVmDict[each_esxiVm]['vmCpuUsage']
            esxiVm.vmCpuUsagePercent = esxiVmDict[each_esxiVm]['vmCpuUsagePercent']
            esxiVm.vmMemoryUsage = esxiVmDict[each_esxiVm]['vmMemoryUsage']
            esxiVm.vmMemoryUsagePercent = esxiVmDict[each_esxiVm]['vmMemoryUsagePercent']
            esxiVm.save()


#
# from pprint import pprint
# pprint(esxiDict)
# pprint(esxiVmDict)























