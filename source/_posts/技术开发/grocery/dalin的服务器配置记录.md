---
title: dalin的服务器配置记录
date: 2022-12-15 23:10:53
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - dalin的服务器配置记录
---
阿里云上重新买了台穷鬼t5，菜是菜了点，但是该折腾还是要折腾的。。。

## 设置虚拟内存

### 安装
`free -m` 查看内存状态, `Swap` 的值都是0，说明还没有安装虚拟内存

在 /opt 下创建虚拟内存文件
```
dd if=/dev/zero of=/opt/swap bs=2048 count=2048000
```

将swap文件设置为swap分区文件
```
chmod 600 /opt/swap    //注意更改swap文件的权限
mkswap /opt/swap
```

激活swap,启用分区交换文件
```
swapon /opt/swap
```

查看结果
```
[root@dalin1 opt]# free -m
              total        used        free      shared  buff/cache   available
Mem:           1829        1329         169           0         330         357
Swap:          3999         429        3570
```

重启自动启用设置，否则机器重启后分区就失效了
```
vim /etc/rc.local
```
底部添加
```
swapon /home/swap
```

### 卸载
停止swap分区
```
swapoff /opt/swap
```
删除掉swap文件
```
rm -rf /opt/swap
```

查看磁盘情况：
```
[root@dalin1 opt]# df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        900M     0  900M   0% /dev
tmpfs           915M     0  915M   0% /dev/shm
tmpfs           915M  612K  915M   1% /run
tmpfs           915M     0  915M   0% /sys/fs/cgroup
/dev/vda1        40G  9.5G   31G  24% /
tmpfs           183M     0  183M   0% /run/user/1000
overlay          40G  9.5G   31G  24% /var/lib/docker/overlay2/cb6202d7408b52de4ca486b57263e33e6dbb34d3adf35e86bfdffe62b9d33339/merged
overlay          40G  9.5G   31G  24% /var/lib/docker/overlay2/25f9d8b78fa8906f7b379efce90fdd90f8e5771399f537988cf15ca450641596/merged
```



## mysql 安装

上一次鄙人的mysql开启了远程访问，并且没有注意安全防范，被比特币勒索了。。。但是使用远程msql服务的需求还是需要的，毕竟真的是方便，这次注意一下安全方面的配置，应该不至于再没了吧。。。

#### 1. centos8 安装mysql8
使用最新的包管理器安装MySQL
```
sudo dnf install @mysql
```

设置开机自启并启动
```
sudo systemctl enable --now mysqld
```

运行mysql_secure_installation脚本，该脚本执行一些与安全性相关的操作并设置MySQL根密码：
```
mysql_secure_installation
```
按提示往下走即可，注意在 `Disallow root login remotely?`选项中选择 `n`

#### 2. 更换 mysql 默认端口
`vim /etc/my.cnf`，添加字段 `port=6612`

`systemctl restart mysqld` 重启 mysql


防火墙添加6612端口白名单
```
firewall-cmd --add-port=6612/tcp --permanent
firewall-cmd --reload
```

centos默认使用的是firewall作为防火墙，一些常用命令：
1. firewall-cmd --list-ports       ##查看已开放的端口
2. firewall-cmd --add-port=6612/tcp --permanent ##永久开放6612端口
3. firewall-cmd --remove-port=6612/tcp --permanent ##永久关闭6612端口
4. firewall-cmd --reload ##刷新


阿里云控制台安全组开放 6612 端口

#### 3. mysql 允许远程主机访问

登录mysql
```
mysql -uroot -p<密码>
```

将 `mysql.user` 中的 `root` 的 `host` 字段设为`'%'`：
```
use mysql;
update user set host='%' where user='root';
flush privileges;
```

#### 4. 使用脚本自动备份数据
```
#!/bin/bash
#数据库服务器
dbserver='localhost'
#数据库用户名
dbuser='root'
#数据库用密码
dbpasswd='********'
#需要备份的数据库，多个数据库用空格分开
dbname='backdata01 backdata02'
#备份时间
backtime=`date +%Y%m%d`
#日志备份路径
logpath='/opt/data/mysqlbak/'
#数据备份路径
datapath='/opt/data/mysqlbak/'
 
 
echo '##################$backtime##########################'
 
#日志记录头部
echo ‘"备份时间为${backtime},备份数据库表 ${dbname} 开始" >> ${logpath}/mysqlback.log
#正式备份数据库
for table in $dbname; do
source=`mysqldump -h ${dbserver} -u ${dbuser} -p${dbpasswd} ${table} > ${logpath}/${backtime}.sql` 2>> ${logpath}/mysqlback.log;
#备份成功以下操作
if [ "$?" == 0 ];then
cd $datapath
#为节约硬盘空间，将数据库压缩
tar zcf ${table}${backtime}.tar.gz ${backtime}.sql > /dev/null
#删除原始文件，只留压缩后文件
rm -f ${datapath}/${backtime}.sql
#删除七天前备份，也就是只保存7天内的备份
find $datapath -name "*.tar.gz" -type f -mtime +7 -exec rm -rf {} \; > /dev/null 2>&1
echo "数据库表 ${dbname} 备份成功!!" >> ${logpath}/mysqlback.log
else
#备份失败则进行以下操作
echo "数据库表 ${dbname} 备份失败!!" >> ${logpath}/mysqlback.log
fi
done
 
echo '##################完成############################'
```
创建定时任务
```
crontab -e
59 23 * * * ./opt/mysqldata/mysqlbak.sh  ## 每天23:59执行命令
```

## redis 安装
#### 5. 安装redis并且设置远程访问和密码配置
```
[root@dalin1 ~]# yum -y install redis
[root@dalin1 ~]# systemctl enable --now redis
```
修改redis端口、设置密码、允许远程访问
```
[root@dalin1 ~]# vim /etc/redis.conf
```
修改 `port 6369`

注释掉 `bind 127.0.0.1`，以便让外网访问

去掉 `#requirepass foobared` 注释，foobared改为自己的密码

防火墙添加6369端口白名单
```
firewall-cmd --add-port=6369/tcp --permanent
firewall-cmd --reload
```

阿里云控制台安全组开放 6369 端口

#### 6. 创建普通用户，以后尽量使用普通用户操作
```
[root@dalin1 ~]# adduser dalin  #创建普通用户 dalin
[root@dalin1 ~]# passwd dalin   #修改密码
[root@dalin1 ~]# su dalin   #切换用户
```
普通用户只在 `/home/<username>` 目录下有完整权限

## docker 安装

docker这么方便的东西怎么能不用呢，但是因为服务器实在太菜了，可能会卡顿，而且要时刻注意内存使用情况

#### 1. 安装依赖包
```
[root@dalin1 ~]# yum install -y yum-utils   device-mapper-persistent-data   lvm2
```
#### 2. 设置Docker源
```
[root@dalin1 ~]# yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
```
#### 3. 安装Docker CE

##### 3.1 docker安装版本查看
```
[root@dalin1 ~]# yum list docker-ce --showduplicates | sort -r
```
#### 3.2 安装docker
```
[root@dalin1 ~]# yum install docker-ce-18.09.6 docker-ce-cli-18.09.6 containerd.io
```
指定安装的docker版本为18.09.6，由于该版本目前为最新版，故可以直接安装，不用指定版本：
```
[root@dalin1 ~]# yum install -y docker-ce docker-ce-cli containerd.io
```
#### 4. 启动Docker并设置开机自启
```
[root@dalin1 ~]# systemctl enable --now docker
```
#### 5. 镜像加速

使用阿里云镜像加速地址
```
[root@dalin1 ~]# mkdir -p /etc/docker
[root@dalin1 ~]# tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://khv87vsk.mirror.aliyuncs.com"]
}
EOF
```

## docker 下安装Elasticsearch和Kibana

服务器太菜，基本跑不动

### 安装Elasticsearch

下载镜像：
```
[root@dalin1 ~]# docker pull elasticsearch:7.2.0
```

启动容器
```
[root@dalin1 ~]# docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -d elasticsearch:7.2.0
```

大概率启动失败，查看日志：
```
[root@dalin1 temp]# docker logs elasticsearch
Exception in thread "main" java.lang.RuntimeException: starting java failed with [1]
output:
#
# There is insufficient memory for the Java Runtime Environment to continue.
# Native memory allocation (mmap) failed to map 1073741824 bytes for committing reserved memory.
# An error report file with more information is saved as:
# logs/hs_err_pid132.log
error:
OpenJDK 64-Bit Server VM warning: INFO: os::commit_memory(0x00000000c0000000, 1073741824, 0) failed; error='Not enough space' (errno=12)
	at org.elasticsearch.tools.launchers.JvmErgonomics.flagsFinal(JvmErgonomics.java:126)
	at org.elasticsearch.tools.launchers.JvmErgonomics.finalJvmOptions(JvmErgonomics.java:88)
    ...
```
jvm内存不足。。。
```
[root@dalin1]# find / -name jvm.options
/var/lib/docker/overlay2/aa7a9ac9f293452ddf8947e9fdf3af24d602566d54b6278284751239b43e37e5/diff/usr/share/elasticsearch/config/jvm.options
[root@dalin1]# vim /var/lib/docker/overlay2/aa7a9ac9f293452ddf8947e9fdf3af24d602566d54b6278284751239b43e37e5/diff/usr/share/elasticsearch/config/jvm.options
```
```
## JVM configuration

################################################################
## IMPORTANT: JVM heap size
################################################################
##
## You should always set the min and max JVM heap
## size to the same value. For example, to set
## the heap to 4 GB, set:
##
## -Xms4g
## -Xmx4g
##
## See https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html
## for more information
##
################################################################

# Xms represents the initial size of total heap space
# Xmx represents the maximum size of total heap space

-Xms1g      #服务器实在太菜了，我改成256m
-Xmx1g      #服务器实在太菜了，我改成256m

################################################################

```
重新启动容器
```
[root@dalin1 ~]# docker start elasticsearch
```

检测是否启动成功
```
[root@dalin1 ~]# curl http://localhost:9200
{
  "name" : "c19d1882a695",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "-zKpqN7TQMqmPULGgdMz3w",
  "version" : {
    "number" : "7.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "508c38a",
    "build_date" : "2019-06-20T15:54:18.811730Z",
    "build_snapshot" : false,
    "lucene_version" : "8.0.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```

解决跨域访问问题

进入容器，修改elasticsearch.yml文件
```
[root@dalin1 ~]# docker exec -it elasticsearch /bin/bash
vim /usr/share/elasticsearch/config/elasticsearch.yml
```
在elasticsearch.yml的文件末尾加上:
```
http.cors.enabled: true
http.cors.allow-origin: "*"
```

es自带的分词器对中文分词不是很友好，所以我们下载开源的IK分词器来解决这个问题。
```
```

`exit` 退出容器后 `docker restart elasticsearch` 重启容器

#### kibana安装
下载镜像
```
[root@dalin1 ~]# docker pull kibana:7.2.0
```

启动kibana

```
[root@dalin1 ~]# docker run --name kibana --link=elasticsearch:es -e ELASTICSEARCH_URL=http://172.17.0.2:9200  -p 5601:5601 -d kibana:7.7.0
```
使用--link连接到elasticsearch容器，并添加环境变量，指定安装es的容器地址

当然也可以进入容器内部修改配置文件来设置es访问地址
```
[root@dalin1 ~]# docker exec -it kibana /bin/bash
vi config/kibana.yml
```
kibana默认是优先使用环境变量的地址，然后才是配置文件kibana.yml

<br>

如何查询容器地址？
```
# 获取到容器的元数据信息
[root@dalin1 ~]# docker inspect [id/name]
```

最后，配置安全组和防火墙，开放9200、5601端口
```
[root@dalin1 ~]# firewall-cmd --add-port=5601/tcp --permanent
[root@dalin1 ~]# firewall-cmd --add-port=9200/tcp --permanent
```

这就结束了吗？是的，网上几乎所有的关于docker下安装kibana教程都是到了这一步就说完事收工、开始体验。。。但是！！！我遇到的情况是访问 `http//:ip:5601`，只会给我冰冷的大字：
```
Kibana server is not ready yet
```
`docker logs kibana`打印日志，报错：
```
{"type":"log","@timestamp":"2020-06-04T08:25:57Z","tags":["warning","elasticsearch","admin"],"pid":6,"message":"Unable to revive connection: http://172.17.0.2:9200/"}
{"type":"log","@timestamp":"2020-06-04T08:25:57Z","tags":["warning","elasticsearch","admin"],"pid":6,"message":"No living connections"}
```
ip地址是没问题的，es服务也确实起了，为什么呢？？这个问题花了我大半天的时间，找遍了网上的教程都没有相关的介绍，官网上关于docker安装kibana的教程更是少。 

进入kibana容器中
```
[root@dalin1 ~]# docker exec -it kibana /bin/bash
bash-4.2$ ping 172.17.0.2    #没有问题，能ping通
bash-4.2$ curl http://120.79.43.44:9200
curl: (7) Failed connect to 120.79.43.44:9200; No route to host
```
问题就出在这里！应该是防火墙的原因导致容器之间无法进行通信

解决方法，依次执行以下命令
```
[root@dalin1 ~]# nmcli connection modify docker0 connection.zone trusted

[root@dalin1 ~]# systemctl stop NetworkManager.service

[root@dalin1 ~]# firewall-cmd --permanent --zone=trusted --change-interface=docker0

[root@dalin1 ~]# systemctl start NetworkManager.service

[root@dalin1 ~]# nmcli connection modify docker0 connection.zone trusted

[root@dalin1 ~]# systemctl restart docker.service
```
把 `docker0` 加入防火墙白名单

重新启动容器，访问地址 http://ip:5601 ，总算没有了 `Kibana server is not ready yet`,显示正在加载的图像，稍作等候即可，部署完成！