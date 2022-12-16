---
title: cmdb_mock
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:37:31
toc: true
tags: 
    - cmdb_mock
---
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
用于在批量创建cmdb数据
1.创建资源
python cmdb_mock.py -action create -type plat -size 10
2. 清理资源
python cmdb_mock.py -action delete -type plat
"""
import argparse
import logging
import os
import random
import uuid

from oslo_config import cfg
from oslo_utils import uuidutils
from pymongo import MongoClient
from aops_api.common.client import Client
from sf_libs.utils.mongodb_lib import get_mongodb_client_auth_dict
from sf_libselect import libselect

_MONGODB_HOST = 'mongodb.cloud.vt'
_MONGODB_PORT = 27017
_MONGODB_MAX_POOL_SIZE = 256
_MONGODB_DB_NAME = 'cmdb'
_MONGODB_USER = 'aops'

PROJECT = 'sync_scp_host'
CONF = cfg.CONF

LOG_FILE_NAME = '/sf/log/today/%s.log' % os.path.basename(__file__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] '
                           '%(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=LOG_FILE_NAME)

# mock资源名称的前缀，方便清理
MOCK_NAME_PREFIX = 'mock-resource'

LOG = logging.getLogger(__name__)


class MongoManager(object):
    def __init__(self, pool_size, host, port, db):
        self.cachedb = self._get_mongo_client(pool_size, host, port, db)

    def _get_mongo_client(self, pool_size, host, port, db):
        return libselect.Libselect(pool_size=pool_size, host=host,
                                   port=port, db=db).get_mongodb()

    def list_scp(self):
        scps = self.cachedb['sf_scp'].find()
        return scps

    def get_host(self, vmid):
        filters = {
            'host.sf_uuid': vmid
        }
        hosts = self.cachedb['host'].find(filters)
        hosts = [host for host in hosts]
        return hosts[0] if hosts else None

    def get_user(self, username):
        filters = dict(name=username)
        users = self.cachedb['user'].find(filters)
        users = [user for user in users]
        return users[0] if users else None


class CmdbManager(object):
    def __init__(self):
        self.client = Client.cmdb_no_auth()
        self.mongo_db = self.get_mongodb()

    @staticmethod
    def get_mongodb():
        """获取mongo客户端"""
        auth_dict = get_mongodb_client_auth_dict(_MONGODB_USER)
        client = MongoClient(maxPoolSize=_MONGODB_MAX_POOL_SIZE, **auth_dict)
        mongo_db = client.get_database(_MONGODB_DB_NAME)
        return mongo_db

    def create_scp_host(self, scp_manage_ip, vmid, project_id):
        host = {
            "host_info": {
                "0": {
                    "bk_host_type": "1",
                    "bk_host_name": "SCP_" + scp_manage_ip,
                    "bk_host_innerip": "127.0.0.1",
                    "bk_uuid": vmid,
                    "bk_project_id": project_id
                }
            }
        }
        try:
            self.client.hosts.add_host(host)
        except Exception:
            LOG.exception("Failed to create scp host: %s.", host)
            return

        LOG.info("Succeeded to create scp host: %s.", host)

    def create_all(self, size=1):
        """所有类型资源都mock一份"""
        for inst_type in INST_TYPE_SET:
            func_name = 'create_{type}'.format(type=inst_type)
            if getattr(self, func_name, None) is not None:
                getattr(self, func_name)(size)

    def create_plat(self, size=1):
        """批量添加数据中心"""
        documents = []
        for i in range(0, size):
            temp_plat = PLAT_TEMPLATE.copy()
            temp_plat['bk_cloud_name'] = rand_name(MOCK_NAME_PREFIX, '')
            temp_plat['bk_cloud_id'] = rand_int_id()
            documents.append(temp_plat)

        self.mongo_db['cc_PlatBase'].insert_many(documents)

    EMPLATE, size)

    def create_host(self, size=1):
        """批量添加机房"""
        self._create_host(SERVER_TEMPLATE, size)

    def _create_instance(self, template, size):
        """批量添加实例"""
        documents = []
        for i in range(0, size):
            temp_inst = template.copy()
            temp_inst['bk_inst_name'] = rand_name(MOCK_NAME_PREFIX, '')
            temp_inst['bk_inst_id'] = rand_int_id()
            documents.append(temp_inst)

        self.mongo_db['cc_ObjectBase'].insert_many(documents)

    def create_sf_room(self, size=1):
        """批量添加机房"""
        self._create_instance(ROOM_TEMPLATE, size)

    def create_sf_rack(self, size=1):
        """批量添加机房"""
        self._create_instance(RACK_TEMPLATE, size)

    def create_sf_switch(self, size=1):
        """批量添加机房"""
        self._create_instance(SWITCH_TEMPLATE, size)

    def create_sf_az(self, size=1):
        """批量添加资源池"""
        self._create_instance(AZ_TEMPLATE, size)

    def create_cluster(self, size=1):
        """批量添加集群"""
        self._create_instance(CLUSTER_TEMPLATE, size)

    def create_sf_line_type(self, size=1):
        """批量添加线路"""
        self._create_instance(LINE_TYPE_TEMPLATE, size)

    def create_sf_oracle(self, size=1):
        """批量添加线路"""
        self._create_instance(ORACLE_TEMPLATE, size)

    def create_sf_sqlserver(self, size=1):
        """批量添加线路"""
        self._create_instance(SQLSERVER_TEMPLATE, size)

    def delete_all(self):
        """清理所有mock出来的数据"""
        for inst_type in INST_TYPE_SET:
            func_name = 'delete_{type}'.format(type=inst_type)
            if getattr(self, func_name, None) is not None:
                getattr(self, func_name)()

    def delete_plat(self):
        """批量添加数据中心"""
        condition = {
            'bk_cloud_name': {
                '$regex': '^{prefix}'.format(
                    prefix=MOCK_NAME_PREFIX)}}
        self.mongo_db['cc_PlatBase'].delete_many(condition)

    def _delete_host(self, inst_type):
        """批量删除实例"""
        type_map = {
            "sf_server": "2",
            "host": "1"
        }
        condition = {
            'bk_host_type': type_map[inst_type],
            'bk_host_name': {
                '$regex': '^{prefix}'.format(prefix=MOCK_NAME_PREFIX)
            }
        }
        self.mongo_db['cc_ObjectBase'].delete_many(condition)

    def delete_sf_server(self):
        """批量删除机房"""
        self._delete_instance('sf_server')

    def delete_host(self):
        """批量删除机房"""
        self._delete_instance('host')

    def _delete_instance(self, inst_type):
        """批量删除实例"""
        condition = {
            'bk_obj_id': inst_type,
            'bk_inst_name': {
                '$regex': '^{prefix}'.format(prefix=MOCK_NAME_PREFIX)
            }
        }
        self.mongo_db['cc_ObjectBase'].delete_many(condition)

    def delete_sf_room(self):
        """批量删除机房"""
        self._delete_instance('sf_room')

    def delete_sf_rack(self):
        """批量删除机架"""
        self._delete_instance('sf_rack')

    def delete_sf_switch(self):
        """批量删除交换机"""
        self._delete_instance('sf_switch')

    def delete_sf_az(self):
        """批量删除机房"""
        self._delete_instance('sf_az')

    def delete_cluster(self):
        """批量删除机架"""
        self._delete_instance('sf_cluster')

    def delete_sf_line_type(self):
        """批量删除交换机"""
        self._delete_instance('sf_line_type')

    def delete_sf_oracle(self):
        """批量删除交换机"""
        self._delete_instance('sf_oracle')

    def delete_sf_sqlserver(self):
        """批量删除交换机"""
        self._delete_instance('sf_sql_server')


def mock_cmdb_data(action, inst_type, size):
    cmdb_manager = CmdbManager()

    func_name = '{action}_{type}'.format(action=action, type=inst_type)
    func_inst = getattr(cmdb_manager, func_name)

    if action == 'create':
        func_inst(size)
    elif action == 'delete':
        func_inst()

# =============================================================================
#                       数据模板
# =============================================================================
PLAT_TEMPLATE = {
    "bk_project_id": "9119535f9c544115bc9fba43ed24734f",
    "create_time": "2021-10-26T09:37:51.734Z",
    "bk_business_contact": "dalin2",
    "bk_duty_officer": "dalin1",
    "bk_location": "",
    "bk_supplier_account": "0",
    "creator": "e901f2c93c34465181353921cab3ef7e",
    "bk_duty_phone": "13444444444",
    "bk_open_time": "2021-05-28 00:00:00",
    "bk_region_name": "",
    "bk_region_maintainer": None,
    "bk_business_contact_phone": "13444444444",
    "bk_comment": "mark",
    "last_time": "2021-10-26T09:37:51.734Z",
    "modifier": "e901f2c93c34465181353921cab3ef7e"
}

ROOM_TEMPLATE = {
    "bk_column": 10,
    "bk_row": 10,
    "bk_supplier_account": "0",
    "bk_cloud_id": 0,
    "region_id": "",
    "create_time": "2021-10-14T01:11:08.087Z",
    "modifier": "e901f2c93c34465181353921cab3ef7e",
    "creator": "e901f2c93c34465181353921cab3ef7e",
    "bk_obj_id": "sf_room",
    "bk_project_id": "9119535f9c544115bc9fba43ed24734f",
    "bk_serial_num": "1",
    "bk_floor": 1,
    "last_time": "2021-11-05T02:27:04.918Z",
    "bk_comment": ""
}

RACK_TEMPLATE = {
    "bk_open_time": "2021-10-28 00:00:00",
    "bk_project_id": "9119535f9c544115bc9fba43ed24734f",
    "bk_serial_num": "1",
    "bk_u_position": 1,
    "modifier": "e901f2c93c34465181353921cab3ef7e",
    "creator": "e901f2c93c34465181353921cab3ef7e",
    "bk_obj_id": "sf_rack",
    "bk_supplier_account": "0",
    "bk_comment": "zxcz123123",
    "region_id": "",
    "last_time": "2021-11-05T02:27:04.918Z",
    "bk_column": 10,
    "create_time": "2021-10-28T03:50:57.452Z",
    "bk_cloud_id": 584346202,
    "bk_row": 10,
    "bk_electric_limit": 4,
    "bk_close_time": "2021-10-29 00:00:00",
}

SWITCH_TEMPLATE = {
    "bk_obj_id": "sf_switch",
    "bk_device_runtime": 464400,
    "bk_device_web_version": "",
    "bk_asset_num": "2",
    "bk_used_by": "",
    "bk_u_position": 12,
    "bk_project_id": "",
    "bk_uuid": "192.200.112.253",
    "create_time": "2021-08-31T01:46:21.300Z",
    "bk_device_mac": "",
    "bk_supplier_account": "0",
    "bk_device_type": "0",
    "bk_u_position_num": 2,
    "bk_password": "",
    "bk_comment": "123",
    "region_id": "",
    "modifier": "e901f2c93c34465181353921cab3ef7e",
    "creator": "cc_collector",
    "bk_device_master": "physics",
    "bk_device_model": "aSW1100",
    "bk_device_status": "0",
    "bk_agreement": "",
    "bk_cloud_id": 0,
    "user_id": "",
    "last_time": "2021-11-09T06:38:34.761Z",
    "bk_device_brand": "2",
    "bk_device_os_soft_version": "11",
    "bk_account": "",
    "bk_device_patch": "",
    "bk_put_on_time": "2021-11-01",
    "bk_device_serial_num": "222222",
    "bk_device_stack": "",
    "bk_device_cascade": "",
    "bk_device_ip": "192.200.112.253",
    "bk_device_start_time": 1633651200,
    "bk_device_fan_status": "0"
}

AZ_TEMPLATE = {
    "creator": "cc_cloudsync",
    "bk_scp_id": None,
    "bk_type": "1",
    "bk_uuid": "515881e1-1825-400e-861e-93ce4ef59ae2",
    "bk_supplier_account": "0",
    "last_time": "2021-11-04T07:52:32.363Z",
    "bk_cloud_id": 0,
    "bk_total_mem": 0,
    "bk_obj_id": "sf_az",
    "modifier": "cc_collector",
    "region_id": "dffff2398540418cab1575d480bea8a4",
    "create_time": "2021-10-26T13:01:17.665Z",
    "bk_total_core": 10,
    "bk_comment": ""
}

CLUSTER_TEMPLATE = {
    "bk_az_id": "8af74a76-f822-4bb3-b512-8ebd34c6c23b",
    "bk_uuid": "04a2b635-feb8-4a8a-8624-272df2f785a7",
    "version": "6.2.0",
    "create_time": "2021-10-26T13:01:15.885Z",
    "last_time": "2021-11-04T07:42:02.784Z",
    "bk_scp_id": None,
    "type": "1",
    "user_id": "",
    "bk_comment": "",
    "modifier": "cc_collector",
    "bk_cloud_id": 0,
    "region_id": "dffff2398540418cab1575d480bea8a4",
    "status": "3",
    "bk_supplier_account": "0",
    "pwd": "",
    "project_id": "",
    "bk_obj_id": "cluster",
    "import_from": "0",
    "ip": "10.134.82.35",
    "port": 443,
    "username": "",
    "creator": "cc_cloudsync"
}

# 服务器模板
SERVER_TEMPLATE = {
    "bk_raid": "",
    "hugepage": False,
    "last_time": "2022-01-13T03:57:29.571Z",
    "bk_cloud_id":0,
    "bk_sla": None,
    "bk_disk": None,
    "bk_slot_num": None,
    "bk_mem": None,
    "bk_mem_max_size": None,
    "invtsc": False,
    "bk_host_type": "2",
    "bk_u_position": None,
    "bk_outer_mac": "",
    "bk_mem_used_num": None,
    "creator": "cc_cloudsync",
    "bk_cpu": 16,
    "operator": [],
    "bk_bak_operator": [],
    "bk_province_name": None,
    "bk_model_number": "",
    "bk_idle_percent": None,
    "disk_preallocate_full": False,
    "bk_project_id": "",
    "bk_runtime": None,
    "bk_scp_uuid": "",
    "cmdline": "",
    "bk_sn": "",
    "bk_asset_belong": None,
    "bk_cpu_physical_cores": None,
    "bk_last_monitor_time": None,
    "bk_mem_info": None,
    "disk_cache_real_direct_sync": False,
    "vmnics_attribute": "",
    "bk_mem_num": None,
    "bk_cpu_over_commit": None,
    "pid": "",
    "bk_host_id": 584368814,
    "bk_host_name": "10.134.91.66",
    "bk_os_version": "",
    "bk_device_type": None,
    "bk_brand": None,
    "bk_collect_status": "2",
    "bk_host_turbo": False,
    "disk_preallocate_metadata": False,
    "bk_uuid": "host-0cc47a6c5bea",
    "disk_vs": False,
    "net0_info": "",
    "mtu": None,
    "bk_az_id": "35ab7223-93d9-47d2-b26e-616c1107945b",
    "bk_host_outerip": [],
    "docker_server_version": "",
    "bk_server_id": "",
    "bk_u_position_num": 1,
    "bk_snmp_port": "",
    "bk_asset_num": "",
    "schedopt": False,
    "bk_rated_power": "",
    "bk_scp_id": 584368694,
    "bk_os_type": None,
    "bk_idle_evidence": "",
    "host_cpu": False,
    "bk_host_status": "running",
    "bk_service_term": None,
    "bk_hci_id": None,
    "modifier": "cc_collector",
    "docker_client_version": "",
    "bk_bios_version": "",
    "bk_az_name": "10.134.90.63",
    "bk_host_innerip": [
        "10.134.91.66"
    ],
    "bk_asset_id": "",
    "bk_os_name": "",
    "bk_cpu_module": "",
    "bk_raid_info": "",
    "bk_mem_card": False,
    "disk_cdrom": False,
    "bk_cpu_mhz": None,
    "bk_business_module": "",
    "bk_server_type": "1",
    "bk_mem_over_commit": None,
    "bk_server_status": None,
    "bk_serial_num": "",
    "region_id": "3f8da76540a34ea0a02dcb9f7ee7dce8",
    "bk_mac": "",
    "bk_nic_type": "",
    "bk_idle_status": "0",
    "using_hugepage": False,
    "bk_network_type": "1",
    "bk_state_name": None,
    "create_time": "2021-12-29T02:07:25.663Z",
    "bk_disk_info": "",
    "bk_comment": "",
    "bk_vtool_installed": None,
    "numa": False,
    "bk_bmc_ip": "",
    "bk_put_on_time": "",
    "hci_dp_info": "",
    "cpu_microcode": "",
    "bk_boot_time": None,
    "bk_hyper_threading": False,
    "bk_cpu_num": 2,
    "bk_os_bit": "",
    "bk_single_power": False,
    "bk_server_name": "",
    "bk_project_name": "",
    "bk_isp_name": None,
    "bk_vhost_type": "1",
    "import_from": "2",
    "bk_supplier_account": "0",
    "bk_state": None
}

# 云主机模板
HOST_TEMPLATE = {
    "bk_raid": "",
    "hugepage": False,
    "last_time": "2022-01-13T03:57:29.571Z",
    "bk_cloud_id": 0,
    "bk_sla": None,
    "bk_disk": None,
    "bk_slot_num": None,
    "bk_mem": None,
    "bk_mem_max_size": None,
    "invtsc": False,
    "bk_host_type": "2",
    "bk_u_position": None,
    "bk_outer_mac": "",
    "bk_mem_used_num": None,
    "creator": "cc_cloudsync",
    "bk_cpu": 16,
    "operator": [],
    "bk_bak_operator": [],
    "bk_province_name": None,
    "bk_model_number": "",
    "bk_idle_percent": None,
    "disk_preallocate_full": False,
    "bk_project_id": "",
    "bk_runtime": None,
    "bk_scp_uuid": "",
    "cmdline": "",
    "bk_sn": "",
    "bk_asset_belong": None,
    "bk_cpu_physical_cores": None,
    "bk_last_monitor_time": None,
    "bk_mem_info": None,
    "disk_cache_real_direct_sync": False,
    "vmnics_attribute": "",
    "bk_mem_num": None,
    "bk_cpu_over_commit": None,
    "pid": "",
    "bk_host_id": 584368814,
    "bk_host_name": "10.134.91.66",
    "bk_os_version": "",
    "bk_device_type": None,
    "bk_brand": None,
    "bk_collect_status": "2",
    "bk_host_turbo": False,
    "disk_preallocate_metadata": False,
    "bk_uuid": "host-0cc47a6c5bea",
    "disk_vs": False,
    "net0_info": "",
    "mtu": None,
    "bk_az_id": "35ab7223-93d9-47d2-b26e-616c1107945b",
    "bk_host_outerip": [],
    "docker_server_version": "",
    "bk_server_id": "",
    "bk_u_position_num": 1,
    "bk_snmp_port": "",
    "bk_asset_num": "",
    "schedopt": False,
    "bk_rated_power": "",
    "bk_scp_id": 584368694,
    "bk_os_type": None,
    "bk_idle_evidence": "",
    "host_cpu": False,
    "bk_host_status": "running",
    "bk_service_term": None,
    "bk_hci_id": None,
    "modifier": "cc_collector",
    "docker_client_version": "",
    "bk_bios_version": "",
    "bk_az_name": "10.134.90.63",
    "bk_host_innerip": [
        "10.134.91.66"
    ],
    "bk_asset_id": "",
    "bk_os_name": "",
    "bk_cpu_module": "",
    "bk_raid_info": "",
    "bk_mem_card": False,
    "disk_cdrom": False,
    "bk_cpu_mhz": None,
    "bk_business_module": "",
    "bk_server_type": "1",
    "bk_mem_over_commit": None,
    "bk_server_status": None,
    "bk_serial_num": "",
    "region_id": "3f8da76540a34ea0a02dcb9f7ee7dce8",
    "bk_mac": "",
    "bk_nic_type": "",
    "bk_idle_status": "0",
    "using_hugepage": False,
    "bk_network_type": "1",
    "bk_state_name": None,
    "create_time": "2021-12-29T02:07:25.663Z",
    "bk_disk_info": "",
    "bk_comment": "",
    "bk_vtool_installed": None,
    "numa": False,
    "bk_bmc_ip": "",
    "bk_put_on_time": "",
    "hci_dp_info": "",
    "cpu_microcode": "",
    "bk_boot_time": None,
    "bk_hyper_threading": False,
    "bk_cpu_num": 2,
    "bk_os_bit": "",
    "bk_single_power": False,
    "bk_server_name": "",
    "bk_project_name": "",
    "bk_isp_name": None,
    "bk_vhost_type": "1",
    "import_from": "2",
    "bk_supplier_account": "0",
    "bk_state": None
}

# 线路模板
LINE_TYPE_TEMPLATE = {
    "region_id": "",
    "bk_bandwidth": 1000,
    "last_time": "2021-11-09T04:50:08.426Z",
    "bk_ip_sections": "[{\"port_ids\": [584345359], \"cidr\": \"10.134.88.1/24\", \"switch_ids\": [584345369]}]",
    "bk_ip_total": 256,
    "bk_supplier_account": "0",
    "user_id": "",
    "modifier": "e901f2c93c34465181353921cab3ef7e",
    "bk_obj_id": "sf_line_type",
    "bk_cloud_id": 0,
    "bk_comment": "111",
    "create_time": "2021-11-01T03:03:10.280Z",
    "creator": "e901f2c93c34465181353921cab3ef7e"}

# oracle服务
ORACLE_TEMPLATE = {
    "create_time": "2021-12-10T10:07:11.806Z",
    "last_time": "2021-12-10T10:07:11.806Z",
    "bk_cluster_hosts": "5.096611959E+09",
    "bk_cluster_ip": None,
    "bk_run_host_uuid": "7979718770500",
    "bk_obj_id": "sf_oracle",
    "bk_supplier_account": "0",
    "modifier": "cc_collector",
    "bk_inst_name": "oracle-127.0.0.1:1433",
    "creator": "cc_collector"
}

# sqlserver服务
SQLSERVER_TEMPLATE = {
    "create_time": "2021-12-10T10:07:11.806Z",
    "last_time": "2021-12-10T10:07:11.806Z",
    "bk_cluster_hosts": "5.096611959E+09",
    "bk_cluster_ip": None,
    "bk_run_host_uuid": "7979718770500",
    "bk_obj_id": "sf_sqlserver",
    "bk_supplier_account": "0",
    "modifier": "cc_collector",
    "bk_inst_name": "sqlserver-127.0.0.1:1433",
    "creator": "cc_collector"
}

TEMPLATE_SET = [
    PLAT_TEMPLATE,
    ROOM_TEMPLATE,
    RACK_TEMPLATE,
    SWITCH_TEMPLATE,
    AZ_TEMPLATE,
    CLUSTER_TEMPLATE,
    SERVER_TEMPLATE,
    HOST_TEMPLATE,
    LINE_TYPE_TEMPLATE,
    ORACLE_TEMPLATE,
    SQLSERVER_TEMPLATE,
]

INST_TYPE_SET = [
    'plat',
    'sf_room',
    'sf_rack',
    'sf_switch',
    'sf_az',
    'cluster',
    'sf_server',
    'host',
    'sf_line_type',
    'sf_oracle',
    'sf_sqlserver'
]


# =============================================================================
#                       工具方法
# =============================================================================
def rand_uuid():
    """Generate a random UUID string

    :return: a random UUID (e.g. '1dc12c7d-60eb-4b61-a7a2-17cf210155b6')
    :rtype: string
    """
    return uuidutils.generate_uuid()


def rand_uuid_hex():
    """Generate a random UUID hex string

    :return: a random UUID (e.g. '0b98cf96d90447bda4b46f31aeb1508c')
    :rtype: string
    """
    return uuid.uuid4().hex


def rand_name(name='', prefix='unit'):
    """Generate a random name that includes a random number

    :param str name: The name that you want to include
    :param str prefix: The prefix that you want to include
    :return: a random name. The format is
             '<prefix>-<name>-<random number>'.
             (e.g. 'prefixfoo-namebar-154876201')
    :rtype: string
    """
    rand_name = str(random.randint(1, 0x7fffffff))
    if name:
        rand_name = name + '-' + rand_name
    if prefix:
        rand_name = prefix + '-' + rand_name
    return rand_name


def rand_int_id(start=0, end=0x7fffffff):
    """Generate a random integer value

    :param int start: The value that you expect to start here
    :param int end: The value that you expect to end here
    :return: a random integer value
    :rtype: int
    """
    return random.randint(start, end)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cmdb_mock',
        description='mock tool for cmdb',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-action', required=True, dest='action',
                        type=str, help=u'[create, delete]')

    parser.add_argument(
        '-type',
        required=True,
        dest='inst_type',
        type=str,
        help=u'[all, plat, sf_room, sf_rack, sf_switch, sf_az, cluster, sf_line_type]',
        choices=INST_TYPE_SET)
    parser.add_argument('-size', dest='size', type=int, default=10,
                        help=u'number of resource mock')
    args = parser.parse_args()

    ACTION = args.action
    INST_TYPE = args.inst_type
    SIZE = args.size

    mock_cmdb_data(ACTION, INST_TYPE, SIZE)

```

