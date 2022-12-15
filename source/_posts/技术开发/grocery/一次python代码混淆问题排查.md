问题描述：

部署加密版本的容器后，有一个容器启动过程失败 aops-api-permission-sync ，该容器是服务启动前做初始化配置，容器启动失败，导致服务也启动失败

正常的日志：
```
Config file not found, using default configs.
2022-09-06 22:01:27.196 6 INFO /usr/lib/python2.7/site-packages/sf_libs/utils/encryption_lib.py:55:get_confuse_aes_key() [-] encryption key is not confused
2022-09-06 22:01:27.250 6 INFO /usr/lib/python2.7/site-packages/migrate/versioning/api.py:348:_migrate() [-] 0 -> 1...
2022-09-06 22:01:27.261 6 INFO /usr/lib/python2.7/site-packages/migrate/versioning/api.py:367:_migrate() [-] done
2022-09-06 22:01:29,695 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:364] - INFO: start processing sync script, data file: /sf/etc/aops-api/iam-policy.yaml
2022-09-06 22:01:29,918 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:184] - INFO: success to parser yaml file: /sf/etc/aops-api/iam-policy.yaml
2022-09-06 22:01:29,919 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:210] - INFO: start to sync OC model data
2022-09-06 22:01:31,488 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:162] - INFO: start to compare 'OC.actions.md5' whether md5 has changed
2022-09-06 22:01:31,493 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:167] - INFO: cacheKey 'OC.actions.md5' old md5:371f3488d2eac117b111484d995d6eba new md5:371f3488d2eac117b111484d995d6eba
2022-09-06 22:01:31,493 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:317] - INFO: app OC actions is not changed, no need to sync
2022-09-06 22:01:31,495 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:162] - INFO: start to compare 'OC.action_groups.md5' whether md5 has changed
2022-09-06 22:01:31,498 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:167] - INFO: cacheKey 'OC.action_groups.md5' old md5:80271c64213658b301632b551b7168ba new md5:80271c64213658b301632b551b7168ba
2022-09-06 22:01:31,498 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:317] - INFO: app OC action_groups is not changed, no need to sync
2022-09-06 22:01:31,501 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:162] - INFO: start to compare 'OC.policies.md5' whether md5 has changed
2022-09-06 22:01:31,503 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:167] - INFO: cacheKey 'OC.policies.md5' old md5:35adbb04e2bf38d2fc7437fc89df0bc6 new md5:35adbb04e2bf38d2fc7437fc89df0bc6
2022-09-06 22:01:31,503 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:317] - INFO: app OC policies is not changed, no need to sync
2022-09-06 22:01:31,505 - /usr/lib/python2.7/site-packages/medusaclient/script/permission_model_sync.py[line:371] - INFO: success to sync permission model, file: /sf/etc/aops-api/iam-policy.yaml
None
```

异常日志：
```
Config file not found, using default configs.
2022-09-07 14:23:40.251 6 INFO <frozen utils.encryption_lib>:55:get_confuse_aes_key() [-] encryption key is not confused
2022-09-07 14:23:40.336 6 INFO /usr/lib/python2.7/site-packages/migrate/versioning/api.py:348:_migrate() [-] 0 -> 1...
2022-09-07 14:23:40.356 6 INFO /usr/lib/python2.7/site-packages/migrate/versioning/api.py:367:_migrate() [-] done
2022-09-07 14:23:42,763 - <frozen script.permission_model_sync>[line:364] - INFO: start processing sync script, data file: /sf/etc/aops-api/iam-policy.yaml
2022-09-07 14:23:42,991 - <frozen script.permission_model_sync>[line:184] - INFO: success to parser yaml file: /sf/etc/aops-api/iam-policy.yaml
2022-09-07 14:23:42,992 - <frozen script.permission_model_sync>[line:210] - INFO: start to sync OC model data
2022-09-07 14:23:44,540 - <frozen script.permission_model_sync>[line:355] - ERROR: get aops_api failed
Traceback (most recent call last):
File "<frozen script.permission_model_sync>", line 353, in _get_routers_info
File "<frozen common.utils>", line 870, in get_routers
File "/usr/lib64/python2.7/importlib/__init__.py", line 37, in import_module
__import__(name)
File "</usr/lib/python2.7/site-packages/aops_api/app/region/routers.py>", line 1, in <module>
RuntimeError: Marshal loads failed
Traceback (most recent call last):
File "./medusa", line 10, in <module>
sys.exit(main())
File "<frozen shell>", line 46, in main
File "<frozen shell>", line 318, in run
File "<frozen commands.iam>", line 290, in cmd_permission_sync
File "<frozen script.permission_model_sync>", line 370, in permission_sync
File "<frozen script.permission_model_sync>", line 225, in do_synchronization
File "<frozen script.permission_model_sync>", line 356, in _get_routers_info
Exception: get_routers_info(aops_api) failed
```

容器启动命令
```
- command:
        - /bin/sh
        - -c
        - /sf/bin/aops-manage --config-file /sf/etc/aops-api/aops-api.conf db_sync;source
          /sf/bin/keystonerc_admin;cd /sf/bin/;./medusa permission-sync --data-file
          /sf/etc/aops-api/iam-policy.yaml
```

得知，后台手动同步权限命令
```
source /sf/bin/keystonerc_admin
cd /sf/bin/
./medusa permission-sync --data-file /sf/etc/aops-api/iam-policy.yaml
```

使用镜像启动容器 `docker run -it docker.sangfor.com/scc-docker-history/aops-api:v2.1.1_EN.stable.20220907111917.encrypt`

```
Type "help", "copyright", "credits" or "license" for more information.
>>> from aops_api.app.agent import controllers
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "</usr/lib/python2.7/site-packages/aops_api/app/agent/__init__.py>", line 1, in <module>
  File "<frozen app.agent>", line 17, in <module>
  File "</usr/lib/python2.7/site-packages/aops_api/app/agent/provider.py>", line 1, in <module>
  File "<frozen app.agent.provider>", line 20, in <module>
  File "</usr/lib/python2.7/site-packages/phoenix/common/manager.py>", line 1, in <module>
  File "<frozen common.manager>", line 22, in <module>
  File "</usr/lib/python2.7/site-packages/phoenix/common/wsgi.py>", line 1, in <module>
  File "<frozen common.wsgi>", line 37, in <module>
  File "/usr/lib/python2.7/site-packages/rpdb/__init__.py", line 9, in <module>
    import pdb
  File "/usr/lib64/python2.7/pdb.py", line 59, in <module>
    class Pdb(bdb.Bdb, cmd.Cmd):
AttributeError: 'module' object has no attribute 'Cmd'
```

其他容器的镜像同步权限没有问题
```
>>> import importlib
>>> module = importlib.import_module("aops_api.app.agent.routers")
>>> module = importlib.import_module("aops_api.app.region.routers")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
  File "</usr/lib/python2.7/site-packages/aops_api/app/region/routers.py>", line 1, in <module>
RuntimeError: Marshal loads failed
>>>
```

其他app导入正常，看来问题就在这里

替换容器内的 /usr/lib/python2.7/site-packages/aops_api/app/region/routers.py 文件

再执行以上命令，不报错！

看来就是这个routers.py加密文件有问题


容器内运行代码失败，报错：
```
2022-09-08 11:50:29.299 155 WARNING <frozen version.service>:65:wrapper() [-] 'local conf' from PasteDeploy INI is being ignored.
2022-09-08 11:50:29.336 155 ERROR <frozen version.service>:52:wrapper() [-] Marshal loads failed: RuntimeError: Marshal loads failed
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service Traceback (most recent call last):
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service   File "<frozen version.service>", line 49, in wrapper
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service   File "<frozen version.service>", line 67, in wrapper
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service   File "<frozen version.service>", line 108, in public_app_factory
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service   File "/usr/lib64/python2.7/importlib/__init__.py", line 37, in import_module
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service     __import__(name)
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service   File "</usr/lib/python2.7/site-packages/aops_api/app/region/routers.py>", line 1, in <module>
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service RuntimeError: Marshal loads failed
2022-09-08 11:50:29.336 155 ERROR phoenix.version.service
2022-09-08 11:50:29.338 155 CRITICAL <frozen version.service>:55:wrapper() [-] Marshal loads failed: RuntimeError: Marshal loads failed
```

查看pyarmor版本

```
Sangfor:SCC/scc-fefcfe86b56e /sf/data/local/test/usr/lib/python2.7/site-packages x pyarmor -v
PyArmor Version 6.4.2
Registration Code: pyarmor-vax-000713
Because of internet exception, could not query registration information.
```
容器上的和打包环境的一致

从制品库下载rpm，替换环境代码，报错

本地环境加密代码，替换，无报错

问题出在 流水线打rpm加密包

Python 版本不一致？

查看打包镜像 docker.sangfor.com/cicd_2336/scc-docker-base/cmp-builder-rpm-q 的 python
```
[root@5bcb6cfeeb1f /]# python
Python 2.7.5 (default, Nov 16 2020, 22:23:17)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
一模一样

咋整啊，僵住了

实在没招了，看代码，找不同！

region.routers
```
class Routers(wsgi.RoutersBase):
    """API for the aops_api region."""

    def append_routers(self, mapper, routers):
        self._controllers = controllers.Controller()

        self._add_resource(
            mapper, self._controllers,
            path="/regions",
            get_action='list_regions',
            rel=json_home.build_resource_relation('list_regions'),
            iam_action=OCRegionAction(action='list_regions')
        )
```
其中self._controllers = controllers.Controller()这里IDE会提示

"Instance attribute _controllers defined outside __init__"

这里的写法和其他的routers都不同，缺失__init__函数，在方法中增加对象属性，会不会是这个问题呢，python写法问题


其他的routers
```
class Routers(wsgi.RoutersBase):

    def __init__(self):
        super(Routers, self).__init__()
        self._controllers = controllers.Controller()

    def append_routers(self, mapper, routers):
        self._add_admin_routers(mapper)
        self._add_tenant_routers(mapper)
        self._add_msp_routers(mapper)

        # 获取agent列表
        self._add_resource(
            mapper, self._controllers,
            path="/agent/host-agent-list",
            get_action='list_agent',
            rel=json_home.build_resource_relation('list_agent'),
            iam_action=OCAgentAction(action='list_agent')
        )

```   
修改代码，流水线打出rpm包，然后替换，居然没报错了！问题就出在这里！！！

问题算是解决了，但是，为什么会这样呢？
