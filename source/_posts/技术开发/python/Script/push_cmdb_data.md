---
title: push_cmdb_data
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:37:31
toc: true
tags: 
    - push_cmdb_data
---
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import logging
import requests
import signal
import threading
import time

u"""
向环境上的所有服务器推送cmdb采集数据
"""

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='push.log', level=logging.DEBUG,
                    format=LOG_FORMAT)

# scc ip
SCC_HOST = '10.134.47.25'
TRANSFER_GATEWAY_HOST = '10.134.47.25'
# 页面登录用户名
USERNAME = 'admin'
# 加密后的密码
PWD = '6707361739e5ca18002bcb05d464d033da1a499ed5fdf660fadd35e250f518f97da0fa884b079b6193f93ed68040e91ea86be547b7a82d0cf3245c01ca2bb20fd7bbadb937103898b00e47c605226fbaeb13a0348762e8dede31d5b570dc07d4c8e7b5308d531158c672d94204c73a972585ef816c87aaadc2778b40d96c24c45d82b2e6da58aded4bdd30b57a2f49b5e08dc189776ee53c92926be0ee3e25512558ccca953b603fcb9153c94a579c257d0e813d94f2c056f0b129fcbcabab4b54cfc2879112b0e201663cc05a47a3571e9352b693210fb93e72e658625d7fa7dd5326f2ce062f85ecea4d25d9e0af2544b3df95fae839f65672b63c51c51a12'  # noqa

X_WWW_FORM_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'close'
}


class Client(object):
    u"""request库封装"""

    def __init__(self, host, username, pwd):
        self.client = requests.Session()
        self.auth = Auth(host, username, pwd)
        self.client.headers = self.auth.get_header()

    def post(self, url, **kwargs):
        return self.client.post(url, **kwargs)

    def get(self, url, **kwargs):
        return self.client.get(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.client.delete(url, **kwargs)

    def put(self, url, **kwargs):
        return self.client.put(url, **kwargs)


class Auth(object):
    u"""获取cookie和token"""

    def __init__(self, host, username, pwd, status='agree'):
        self.host = host
        self.ticket_url = 'https://%s:4430/ticket' % host
        self.username = username
        self.pwd = pwd
        self.status = status
        self.client = None

    def get_tokens(self, response):  # noqa
        """
        {
            "success": 1,
            "data": {
                "username": "admin",
                "client_ip": "172.23.13.106",
                "CSRFPreventionToken": "4984b0511212d1b2534b7888c9fcdcad",
                "weak_password": 1,
                "days": 18,
                "passwd_is_expired": 0,
                "passwd_remain_days": 0
            }
        }
        :param response:
        :return:
        """
        json_response = json.loads(response.text)
        csrf_prevention_token = json_response['data']["CSRFPreventionToken"]

        acmp_auth_token = list(
            list(list(response.cookies._cookies.values())[0].values())[0].values()  # noqa
        )[0].value

        logging.debug("csrf_prevention_token: %s, acmp_auth_token: %s" % (
            csrf_prevention_token, acmp_auth_token))
        return csrf_prevention_token, acmp_auth_token

    def post_urlencoded_data(self, request_url):
        """获取ticket
        功能说明：发送以form表单数据格式（它要求数据名称（name）和数据值（value）之间以等号相连，
        与另一组name/value值之间用&相连。例如：parameter1=12345&parameter2=23456。）
        请求到远程服务器，并获取请求响应报文。
        该请求消息头要求为：{"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}。  # noqa
        输入参数说明：接收请求的URL;请求报文数据，格式为name1=value1&name2=value2
        输出参数：请求响应报文
        :param request_url:
        :return:
        """
        logging.debug(request_url)
        request_json_data = 'username=%s&password=%s&status=%s' % (
            self.username, self.pwd, self.status)
        request_json_data = str(request_json_data).replace('+', '%2B')
        request_data = request_json_data.encode('utf-8')

        r = requests.post(request_url, data=request_data,
                          headers=X_WWW_FORM_HEADER, verify=False)

        response_data = r.text
        logging.info('response_data:\n %s' % response_data)

        return self.get_tokens(r)

    def get_header(self):
        # 1.按照配置的IP和admin账号密码请求ticket接口
         csrf, auth_token = self.post_urlencoded_data(self.ticket_url)
        # 2.构造API接口请求所需要的请求头
        cookie = 'UEDC_LOGIN_POLICY_VALUE=checked; aCMPAuthToken=%s; ' \
                 'login=local; jump_back=' % auth_token
        header = {
            'CSRFPreventionToken': csrf,
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie
        }
        return header


client = Client(SCC_HOST, USERNAME, PWD)


def get_server_endpoints():
    url = 'https://%s:4430/aops/admin/view/server-list' % SCC_HOST

    res = client.get(url, verify=False)
    servers = res.json()['data']
    # 脚本插数据时 import_from=1，避免和同步过来的数据搞混
    uuids = [server['sf_uuid'] for server in servers if
             server['import_from'] == '1']
    logging.info('the num of servers: %s', len(uuids))
    return uuids


def push_cmdb_data(endpoint, step=30):  # noqa
    url = 'http://%s:8002/api/ams-ce/hosts/report' % SCC_HOST

    while True:
        meta = {
            'objid': 'host',
            'endpoint': endpoint,
            'channel': 'snapshot2',
            'metric': '',
            'data': {
                'model': {
                    'bk_bios_version': 'BOCHS - 1',
                    'bk_boot_time': '2021-07-15 11:47:39',
                    'bk_cpu': 2,
                    'bk_cpu_mhz': 2594,
                    'bk_cpu_module': 'Intel(R) Core(TM)2 Duo CPU T7700 @ 2.40GHz',  # noqa
                    'bk_cpu_num': 1,
                    'bk_disk': 80,
                    'bk_host_innerip': '10.10.10.110',
                    'bk_mac': 'fe:fc:fe:7d:9a:93',
                    'bk_mem': 4096,
                    'bk_os_bit': '64',
                    'bk_os_name': 'Microsoft Windows Server 2012 R2 Standard',
                    'bk_os_type': '2',
                    'bk_os_version': '6.3.9600 Build 9600',
                    'bk_runtime': 440,
                    'bk_uuid': endpoint
                },
                'snap': {},
                'association': None
            }
        }
        meta = json.dumps(meta)

        item = [{
            'metric': 'host.cmdb.info',
            'value': 1,
            'tags': '',
            'meta': meta
        }]

        data = json.dumps(item)
        res = requests.post(url=url, data=data, verify=False)
        logging.info('%s cmdb_data: %s', endpoint, res.status_code)
        time.sleep(step)


def quit_(signum, frame):  # noqa
    print 'Bye'
    os._exit(0)  # noqa


if __name__ == '__main__':
    endpoints = get_server_endpoints()
    logging.info('endpoints: %s', len(endpoints))

    signal.signal(signal.SIGINT, quit_)
    signal.signal(signal.SIGTERM, quit_)

    threads = []
    end_index = max(int(round(len(endpoints) / 100.0 * 5)), 1)
    for endpoint in endpoints[:end_index]:
        t = threading.Thread(
            target=push_cmdb_data, args=(endpoint,)
        )
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

    while True:
        pass

```

