# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.shortcuts import render, HttpResponse
import json
from home_application.utils import config
from home_application.utils.vsphere_monitor import add_data, hello_vcenter, run, payload
import time
import requests
import sys


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, "home_application/monitor_line.html")


def log_search(request):
    """
    日志搜索
    """
    return render(request, 'home_application/log_index.html')


def log_result(request):
    """
    日志搜索结果
    """
    return render(request, 'home_application/log_result.html')


def trouble_police(request):
    """
    故障预警
    """
    return render(request, 'home_application/monitor_police.html')


def monitor_health(request):
    """
    数据健康度
    """
    return render(request, 'home_application/monitor_health.html')


def get_esxi_data(request):
    """
    获取esxi数据
    """
    host = config.host
    user = config.user
    pwd = config.pwd
    port = config.port
    interval = config.interval

    # 获取时间
    dt = time.time()
    timeStamp = dt
    # print(timeStamp)
    timeArray = time.localtime(timeStamp)
    YMD = time.strftime("%Y-%m-%d", timeArray)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    # print(otherStyleTime, type(otherStyleTime))
    struct_time = time.strptime(otherStyleTime, "%Y-%m-%d %H:%M")
    # print(struct_time)
    # print(struct_time.tm_hour, type(struct_time.tm_hour))
    # ts = int(time.mktime(struct_time))
    # todo 我们需要的时间戳
    ts = float(time.mktime(struct_time))
    print(ts, type(ts))
    # timeArray = time.localtime(ts)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime, type(otherStyleTime))

    # 连接上vcenter
    success, msg = hello_vcenter(host, user, pwd, port)
    if success == False:
        print(msg)
        add_data("vcenter.alive", 0, "GAUGE", "")
        # print json.dumps(payload,indent=4)
        sys.exit(1)

    run(host, user, pwd, port, interval)
    from pprint import pprint

    print('==============================')
    pprint(data)
    return HttpResponse('...')


def data(request):
    """
    获取数据
    """
    data_test = {
        "code": 0,
        "result": True,
        "messge": "success",
        "data": {
            "xAxis": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
            "series": [
                {
                    "name": "磁盘数据",
                    "type": "line",
                    "data": [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
                },
                {
                    "name": "cpu使用",
                    "type": "line",
                    "data": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
                },
                {
                    "name": "net数据",
                    "type": "line",
                    "data": [1, 5, 9.0, 22.4, 25.7, 12, 175.6, 179, 36, 25, 26, 25]
                }
            ]
        }
    }
    return HttpResponse(json.dumps(data_test, ensure_ascii=False))


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "home_application/dev_guide.html")


def contact(request):
    """
    联系页
    """
    return render(request, "home_application/contact.html")
