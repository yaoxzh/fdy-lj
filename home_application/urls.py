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

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^$", views.home, name='home'),
    url(r"^dev-guide/$", views.dev_guide),
    url(r"^contact/$", views.contact),
    url(r'^data/$', views.data, name='data'),
    url(r'^log_search/$', views.log_search, name='log_search'),
    url(r'^log_result/$', views.log_result, name='log_result'),
    url(r'^trouble_police/$', views.trouble_police, name='trouble_police'),
    url(r'^monitor_health/$', views.monitor_health, name='monitor_health'),
    url(r'esxi_data/$', views.get_esxi_data, name='esxi_data')



)
