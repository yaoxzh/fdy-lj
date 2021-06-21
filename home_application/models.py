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

from django.db import models

# Create your models here.
#
#
from datetime import datetime


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    # 将BaseModel抽象成一个基类
    class Meta:
        abstract = True


class Esix(BaseModel):
    name = models.CharField(max_length=50, verbose_name='asix名')
    cpuMhz = models.CharField(max_length=10, verbose_name='cpu频率(MHZ)')
    cpuUsagePercent = models.CharField(max_length=5, verbose_name='cpu使用率(%)')
    maxMemory = models.CharField(max_length=10, verbose_name='内存最大值(GB)')
    memoryUsage = models.CharField(max_length=10, verbose_name='内存使用(GB)')
    memoryUsagePercent = models.CharField(max_length=5, verbose_name='内存使用率(%)')
    numCpuCores = models.CharField(max_length=3, verbose_name='cpu的核数')
    numCpuPkgs = models.CharField(max_length=3, verbose_name='cpu处理器数量')
    storage_percent = models.CharField(max_length=6, verbose_name='磁盘的使用率')

    def __str__(self):
        return self.name


class EsixVm(BaseModel):
    esixName = models.ForeignKey(Esix, on_delete=models.CASCADE, verbose_name='asix名', null=True, blank=True)
    vmName = models.CharField(max_length=50, verbose_name='虚拟机名',)
    maxVmCpuUsage = models.CharField(max_length=10, verbose_name='cpu最大值(MHZ)')
    numCpu = models.CharField(max_length=3, verbose_name='cpu的核数')
    storage_percent = models.CharField(max_length=6, verbose_name='磁盘使用率(%)')
    vmCpuDemand = models.CharField(max_length=5, verbose_name='cpuDemand')
    vmCpuUsage = models.CharField(max_length=5, verbose_name='cpu使用(MHZ)')
    vmCpuUsagePercent = models.CharField(max_length=6, verbose_name='cpu使用率(%)')
    vmMemoryUsage = models.CharField(max_length=10, verbose_name='内存使用(MHZ)')
    vmMemoryUsagePercent = models.CharField(max_length=6, verbose_name='内存使用率(%)')

    def __str__(self):
        return self.vmName






















