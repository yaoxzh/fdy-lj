import atexit
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect
import sys
import copy
import requests
import config
from datetime import timedelta

data = {}
payload = []

def VmInfo(vm, content, vchtime, interval, perf_dict, tags):
    try:
        print('========================')
        print('虚拟机的名字：', vm.name)
        print('虚拟机总的cpu核数', vm.summary.config.numCpu)
        statInt = interval / 20
        summary = vm.summary
        stats = summary.quickStats
        # print(summary.runtime)
        print('虚拟机的快照', stats)
        # print(stats.overallCpuDemand)
        # print(stats.overallCpuDemand)

        uptime = stats.uptimeSeconds
        add_data("vm.uptime", uptime, "GAUGE", tags)
        cpuUsageMHZ = stats.overallCpuUsage
        cpuMaxUsageMHZ = summary.runtime.maxCpuUsage

        # print('虚拟机cpu总的使用情况和最大使用：', stats.overallCpuUsage, summary.runtime.maxCpuUsage)
        cpuUsage = 100 * (float(cpuUsageMHZ) / float(cpuMaxUsageMHZ))
        cpuUsage = round(cpuUsage, 1)
        add_data("vm.cpu.usage", cpuUsage, "GAUGE", tags)
        # data[vm.name]['maxCpuUsage'] = summary.runtime.maxCpuUsage
        # data[vm.name]['cpuUsage'] = round(cpuUsage, 1)
        print('cpu使用率:', cpuUsage)

        # 获取内存的使用情况
        memoryUsage = stats.guestMemoryUsage / 1024
        print('内存的使用情况：', round(memoryUsage, 1))
        add_data("vm.memory.usage", round(memoryUsage, 1), "GAUGE", tags)
        # data[vm.name]['memoryUsage'] = round(memoryUsage, 1)

        # 获取最大内存
        memoryCapacity = summary.runtime.maxMemoryUsage / 1024
        add_data("vm.memory.capacity", memoryCapacity, "GAUGE", tags)
        # print('最大内存：', memoryCapacity)
        # data[vm.name]['memoryCapacity'] = memoryCapacity

        # 剩余可用内存容量的百分比
        freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacity) * 100
        )
        # print('剩余可用内存百分比：', freeMemoryPercentage)
        add_data("vm.memory.freePercent", freeMemoryPercentage, "GAUGE", tags)
        # data[vm.name]['freeMemoryPercentage'] = freeMemoryPercentage

        # # 第一层
        # if not data.get(vm.name):
        #     data[vm.name] = {}
        #
        # # 第二层
        # if not data[vm.name].get('vm_data'):
        #     # data[vm.name]['cpuUsageMHZ'] = stats.overallCpuUsage
        #     data[vm.name]['vm_data'] = {}
        #
        # if not data[vm.name]['vm_data'].get(YMD):
        #     data[vm.name]['vm_data'][YMD] = {}
        #
        # # 第四层
        # if not data[vm.name]['vm_data'][YMD].get(struct_time.tm_hour):
        #     data[vm.name]['vm_data'][YMD][struct_time.tm_hour] = []
        #     data[vm.name]['vm_data'][YMD][struct_time.tm_hour].append((cpuUsageMHZ,
        #                                                                cpuMaxUsageMHZ,
        #                                                                cpuUsage,
        #                                                                memoryUsage,
        #                                                                memoryCapacity,
        #                                                                freeMemoryPercentage,
        #                                                                ts))
        # else:
        #     data[vm.name]['vm_data'][YMD][struct_time.tm_hour].append((cpuUsageMHZ,
        #                                                                cpuMaxUsageMHZ,
        #                                                                cpuUsage,
        #                                                                memoryUsage,
        #                                                                memoryCapacity,
        #                                                                freeMemoryPercentage,
        #                                                                ts))

        # 获取磁盘读的速度
        statDatastoreRead = BuildQuery(content, vchtime, (perf_id(perf_dict, 'datastore.read.average')), "*", vm,
                                       interval)
        # print(statDatastoreRead)
        # print(statDatastoreRead[0].value[0])
        DatastoreRead = (float(sum(statDatastoreRead[0].value[0].value) * 1024) / statInt)
        # print(DatastoreRead)
        add_data("vm.datastore.io.read_bytes", DatastoreRead, "GAUGE", tags)

        # 获取磁盘写的速度
        statDatastoreWrite = BuildQuery(content, vchtime, (perf_id(perf_dict, 'datastore.write.average')), "*", vm,
                                        interval)
        DatastoreWrite = (float(sum(statDatastoreWrite[0].value[0].value) * 1024) / statInt)
        # print(DatastoreWrite)
        add_data("vm.datastore.io.write_bytes", DatastoreWrite, "GAUGE", tags)

        # 获取硬盘读的速度
        statDatastoreIoRead = BuildQuery(content, vchtime, (perf_id(perf_dict, 'datastore.numberReadAveraged.average')),
                                         "*", vm, interval)
        DatastoreIoRead = (float(sum(statDatastoreIoRead[0].value[0].value)) / statInt)
        # print(DatastoreIoRead)
        add_data("vm.datastore.io.read_numbers", DatastoreIoRead, "GAUGE", tags)

        # 获取硬盘写的速度
        statDatastoreIoWrite = BuildQuery(content, vchtime,
                                          (perf_id(perf_dict, 'datastore.numberWriteAveraged.average')), "*", vm,
                                          interval)
        DatastoreIoWrite = (float(sum(statDatastoreIoWrite[0].value[0].value)) / statInt)
        # print(DatastoreIoWrite)
        add_data("vm.datastore.io.write_numbers", DatastoreIoWrite, "GAUGE", tags)

        ######
        statDatastoreLatRead = BuildQuery(content, vchtime, (perf_id(perf_dict, 'datastore.totalReadLatency.average')),
                                          "*", vm, interval)
        DatastoreLatRead = (float(sum(statDatastoreLatRead[0].value[0].value)) / statInt)
        add_data("vm.datastore.io.read_latency", DatastoreLatRead, "GAUGE", tags)
        # print(DatastoreLatRead)

        #######
        statDatastoreLatWrite = BuildQuery(content, vchtime,
                                           (perf_id(perf_dict, 'datastore.totalWriteLatency.average')), "*", vm,
                                           interval)
        DatastoreLatWrite = (float(sum(statDatastoreLatWrite[0].value[0].value)) / statInt)
        add_data("vm.datastore.io.write_latency", DatastoreLatWrite, "GAUGE", tags)
        # print(DatastoreLatWrite)

        #######
        statNetworkTx = BuildQuery(content, vchtime, (perf_id(perf_dict, 'net.transmitted.average')), "", vm, interval)
        if statNetworkTx != False:
            networkTx = (float(sum(statNetworkTx[0].value[0].value) * 8 * 1024) / statInt)
            # print(networkTx)
            add_data("vm.net.if.out", networkTx, "GAUGE", tags)
        statNetworkRx = BuildQuery(content, vchtime, (perf_id(perf_dict, 'net.received.average')), "", vm, interval)
        if statNetworkRx != False:
            networkRx = (float(sum(statNetworkRx[0].value[0].value) * 8 * 1024) / statInt)
            # print(networkRx)
            add_data("vm.net.if.in", networkRx, "GAUGE", tags)

    except Exception as error:
        print("Unable to access information for host: ", vm.name)
        print(error)
        pass


def HostInformation(host, datacenter_name, computeResource_name, content, perf_dict, vchtime, interval):
    try:
        statInt = interval / 20
        summary = host.summary
        # print(summary)
        stats = summary.quickStats
        # print(stats)
        hardware = host.hardware
        # print(hardware)
        # print(type(str(datacenter_name)))
        # print(str(datacenter_name))
        tags = "datacenter=" + datacenter_name + ",cluster_name=" + computeResource_name + ",host=" + host.name

        uptime = stats.uptime
        # print(uptime)
        add_data("esxi.uptime", uptime, "GAUGE", tags)

        cpuUsage = 100 * 1000 * 1000 * float(stats.overallCpuUsage) / float(
            hardware.cpuInfo.numCpuCores * hardware.cpuInfo.hz)
        # print(cpuUsage)
        add_data("esxi.cpu.usage", cpuUsage, "GAUGE", tags)

        memoryCapacity = hardware.memorySize
        add_data("esxi.memory.capacity", memoryCapacity, "GAUGE", tags)

        memoryUsage = stats.overallMemoryUsage * 1024 * 1024
        add_data("esxi.memory.usage", memoryUsage, "GAUGE", tags)

        freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacity) * 100
        )
        add_data("esxi.memory.freePercent", freeMemoryPercentage, "GAUGE", tags)

        statNetworkTx = BuildQuery(content, vchtime, (perf_id(perf_dict, 'net.transmitted.average')), "", host,
                                   interval)
        networkTx = (float(sum(statNetworkTx[0].value[0].value) * 8 * 1024) / statInt)
        add_data("esxi.net.if.out", networkTx, "GAUGE", tags)

        statNetworkRx = BuildQuery(content, vchtime, (perf_id(perf_dict, 'net.received.average')), "", host, interval)
        networkRx = (float(sum(statNetworkRx[0].value[0].value) * 8 * 1024) / statInt)
        add_data("esxi.net.if.in", networkRx, "GAUGE", tags)

        add_data("esxi.alive", 1, "GAUGE", tags)

    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        pass


def perf_id(perf_dict, counter_name):
    counter_key = perf_dict[counter_name]
    return counter_key


def ComputeResourceInformation(computeResource, datacenter_name, content, perf_dict, vchtime, interval):
    try:
        hostList = computeResource.host  # 获取主机
        print(hostList)
        computeResource_name = computeResource.name  # 获取主机的名称
        print(computeResource_name)
        for host in hostList:
            print(host.name)
            if (host.name in config.esxi_names) or (len(config.esxi_names) == 0):
                HostInformation(host, datacenter_name, computeResource_name, content, perf_dict, vchtime, interval)
    except Exception as error:
        print("Unable to access information for compute resource: ",
              computeResource.name)
        print(error)
        pass


def DatastoreInformation(datastore, datacenter_name):  # vim.Datastore:datastore-10' datastore1
    try:
        summary = datastore.summary
        # print(summary)
        name = summary.name
        TYPE = summary.type
        # print(type(str(datacenter_name)), type(name), type(TYPE))
        tags = "datacenter=" + datacenter_name + ",datastore=" + name + ",type=" + TYPE
        capacity = summary.capacity

        add_data("datastore.capacity", capacity, "GAUGE", tags)  # datastore的存储能力

        freeSpace = summary.freeSpace
        add_data("datastore.free", freeSpace, "GAUGE", tags)  # datastore的剩余空间

        freeSpacePercentage = (float(freeSpace) / capacity) * 100
        add_data("datastore.freePercent", freeSpacePercentage, "GAUGE", tags)  # datastore剩余空间的百分比

    except Exception as error:
        print("Una9ble to access summary for datastore: ", datastore.name)
        print(error)
        pass


# 用来存储vcenter数据的汇总信息
def add_data(metric, value, counterType, tags):  # "vcenter.alive", 0, "GAUGE", ""
    data = {"endpoint": config.endpoint, "metric": metric, "step": config.interval, "value": value,
            "counterType": counterType, "tags": tags}
    payload.append(copy.copy(data))


def run(host, user, pwd, port, interval):
    try:
        # 链接vcenter
        si = SmartConnectNoSSL(host=host, user=user, pwd=pwd, port=port)
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()
        # print(content)
        # print('======================================')
        # vchtime = si.CurrentTime()
        from datetime import datetime
        vchtime = datetime.now()
        # print(si)
        # print(vchtime, type(vchtime))
        # from datetime import datetime
        # print(datetime.now())

        perf_dict = {}  # 存储虚拟机信息相关的参数
        perfList = content.perfManager.perfCounter  # vcenter上所有可以演示的东西
        # print(perfList)
        for counter in perfList:
            counter_full = "{}.{}.{}".format(counter.groupInfo.key, counter.nameInfo.key, counter.rollupType)
            # print(counter_full, counter.key)  # 虚拟机的信息相关的参数
            perf_dict[counter_full] = counter.key

        # from pprint import pprint
        # pprint(perf_dict)

        for datacenter in content.rootFolder.childEntity:
            datacenter_name = datacenter.name.encode("utf8")
            datacenter_name = datacenter_name.decode('utf-8')
            # print(datacenter_name, type(datacenter_name))
            datastores = datacenter.datastore
            # print(datastores)
            for ds in datastores:
                # print(ds, ds.name)
                if (ds.name in config.datastore_names) or (len(config.datastore_names) == 0):
                    DatastoreInformation(ds, datacenter_name)  # 存储数据中心的信息

            if hasattr(datacenter.hostFolder, 'childEntity'):
                hostFolder = datacenter.hostFolder
                # print(hostFolder)
                computeResourceList = []
                computeResourceList = getComputeResource(hostFolder, computeResourceList)
                # print(computeResourceList)
                for computeResource in computeResourceList:
                    # print(computeResource,
                    #       '==========\n', datacenter_name,
                    #       '==========\n', content,
                    #       '==========\n', perf_dict,
                    #       '==========\n', vchtime,
                    #       '==========\n', interval)
                    ComputeResourceInformation(computeResource, datacenter_name, content, perf_dict, vchtime, interval)

        if config.vm_enable == True:
            obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
            for vm in obj.view:
                if (vm.name in config.vm_names) or (len(config.vm_names) == 0):
                    tags = "vm=" + vm.name
                    if vm.runtime.powerState == "poweredOn":
                        VmInfo(vm, content, vchtime, interval, perf_dict, tags)
                        add_data("vm.power", 1, "GAUGE", tags)
                    else:
                        add_data("vm.power", 0, "GAUGE", tags)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return False, error.msg
    return True, "ok"


def getComputeResource(Folder, computeResourceList):
    if hasattr(Folder, 'childEntity'):
        for computeResource in Folder.childEntity:
            getComputeResource(computeResource, computeResourceList)
    else:
        computeResourceList.append(Folder)
    return computeResourceList


def hello_vcenter(vchost, username, password, port):
    try:
        si = SmartConnectNoSSL(
            host=vchost,
            user=username,
            pwd=password,
            port=port)

        atexit.register(Disconnect, si)
        return True, "ok"
    except vmodl.MethodFault as error:
        return False, error.msg
    except Exception as e:
        return False, str(e)


def BuildQuery(content, vchtime, counterId, instance, entity, interval):
    perfManager = content.perfManager
    metricId = vim.PerformanceManager.MetricId(counterId=counterId, instance=instance)
    startTime = vchtime - timedelta(seconds=(interval + 60))
    endTime = vchtime - timedelta(seconds=60)
    query = vim.PerformanceManager.QuerySpec(intervalId=20, entity=entity, metricId=[metricId], startTime=startTime,
                                             endTime=endTime)
    perfResults = perfManager.QueryPerf(querySpec=[query])
    if perfResults:
        return perfResults
    else:
        return False
