---
title: mysql、redis开启远程访问
date: 2022-12-15 23:11:35
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - mysql、redis开启远程访问
---
要在本地使用云服务器中的mysql、redis服务，需要开启远程访问，阿里云还需要在控制台中开放3306、6379访问端口。

#### 1、mysql开启远程访问

默认情况下，mysql帐号不允许从远程登陆，只能在localhost登录。 在localhost登入mysql后，更改 "mysql" 数据库里的 "user" 表里的 "host" 项，将"localhost"改为"%"

```
$ mysql -u root -p
   Enter password:
    ……
   mysql>
　　mysql>update user set host = '%' where user = 'root';

　　mysql>select host, user from user;
　
```

#### 2、redis开启远程访问

防火墙开放6379端口：

```
vim /etc/sysconfig/iptables
添加字段：
-A RH-Firewall-1-INPUT -m state NEW -m tcp -dport 8080 -j ACCEPT
```

修改redis配置文件
vim /etc/redis.conf

- `bind127.0.0.1` 这一行注释掉
- `protected-mode yes` 改为 `protected-mode no`

保存后重启：
sysremctl restart redis

**2020-6-1：由于鄙人暴露了mysql到公网上，不加约束、放荡不羁，如今数据库已遭到比特币勒索，血与泪的教训，以后要多加规范，防火防盗防小人**