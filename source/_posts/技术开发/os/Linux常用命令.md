#### 远程文件拷贝
```
//从远程主机拷贝文件到当前目录
scp root@172.23.4.112:/opt/test.txt .

//从远程主机拷贝文件夹到当前目录
scp -r root@172.23.4.112:/opt/test/ .


//拷贝文件到远程主机
scp /opt/test.txt root@172.23.4.112:/opt

//拷贝文夹件到远程主机
scp -r /opt/test/ root@172.23.4.112:/opt

//指定端口
scp -P 22345 ...
```

## 性能问题排除
```
// 查看cpu使用情况
top

// 查看内存使用情况
free -m
// 查看内存占用前20进程
ps aux | head -1;ps aux |grep -v PID |sort -rn -k +4 | head -20


// 查看磁盘使用情况
df -h
// 查看当前目录下的所有一级子目录和文件的磁盘使用情况
du -sh *

```

### vi/vim使用

#### 关键字查询
命令模式下，输入：

/ + <关键字> + 回车 （从开头查找）

? + <关键字> + 回车 （从末尾行查找）

- n（小写）查看下一个匹配

- N(大写）查看上一个匹配

- 命令模式，: + noh/set-noh (nohlsearch或者set nohlsearch)

#### 复制粘贴删除
两种模式，快速模式和命令模式

快速模式
从当前光标作为锚点

yy // 复制当前行
8yy // 从当前光标所在的行开始复制8行

dd // 剪切当前行

8dd // 从当前光标所在的行开始剪切8行

p // 在光标下一行粘贴


: + 1,8d + 回车  // 剪切1-8行

：+ 1,,$d + 回车   // 剪切全部

: + 1,8y + 回车  // 复制1-8行

：+ 1,,$y + 回车   // 复制全部


#### 行号
: + set number + 回车 // 显示行号

: + set nonumber + 回车 // 隐藏行号

: + n  // 跳转到n行

: + ,$ // 跳转到文件末尾

vim +n filename // // 打开文件然后跳转到n行


### ip&dns配置
```
vi /etc/sysconfig/network-scripts/ifcfg-ens32 // 查看配置

cat /etc/resolv.conf
nameserver 114.114.114.114

//查看配置
nslookup 127.0.0.1 | grep Server
```

## journalctl常用命令
 ```
复制代码
# 以flow形式查看日志
$ journalctl -f

# 查看内核日志
$ journalctl -k

# 查看指定服务日志
$ journalctl -u docker.serivce

# 查看指定日期日志
$ journalctl --since="2018-09-21 10:21:00" -u docker
$ journalctl --since="2018-09-21 10:21:00" --until="2018-09-21 10:22:00" -u docker

# 查看指定级别日志
$ journalctl -p 3 -u docker.service
操作系统提供了从0 (emerg) 到 7 (debug) 一共7个级别的日志，7个级别的含义为：
    0: emerg
    1: alert
    2: crit
    3: err
    4: warning
    5: notice
    6: info
    7: debug
    
# 查看日志占用的磁盘空间
$ journalctl --disk-usage

# 设置日志占用的空间
$ journalctl --vacuum-size=500M

# 设置日志保存的时间
$ journalctl --vacuum-time=1month

# 检查日志文件一致性
$ journalctl –-verify
```

### 创建软连接
ln -sfn /sf/etc/n9e/ etc

### 查看进程所在路径
ps aux | grep [name]
ll /proc/{pid} 

### 如何让linux打满 cpu
加压：for i in `seq 1 $(cat /proc/cpuinfo |grep "physical id" |wc -l)`; do cpu_test if=/dev/zero of=/dev/null & done

恢复：ps aux | grep cpu_test | awk '{print $2}' | xargs kill -9

### 查看占用端口的进程
1. 先根据进程名查看进程id  
ps aux | grep 进程名(或者ps -ef | grep 进程名)

2. 通过进程id查看占用的端口  
netstat -nap | grep 进程id

3. 通过端口号查看占用的进程id  
netstat -nap | grep 端口号

### iptables
1、查看所有规则

iptables -nvL --line-number

-L 查看当前表的所有规则，默认查看的是filter表，如果要查看NAT表，可以加上-t NAT参数
-n 不对ip地址进行反查，加上这个参数显示速度会快很多
-v 输出详细信息，包含通过该规则的数据包数量，总字节数及相应的网络接口
–-line-number 显示规则的序列号，这个参数在删除或修改规则时会用到

### 3w命令
```
who #查询系统中的用户(登陆的用户)
whoami  #查看系统当前用户名
whereis #查看系统安装的某个软件的路径
which #查找软件的可执行文件路径 
whereis python #查看python的安装路径
which python #查看python可执行文件路径
```

### 命令行获取和修改文本
```
// 获取第一列第一行
cut -f 1 -d . version | sed -n '1p'

// 获取指定行
awk -F " = " 'NR==2{printf $1 "_suffix"}' envpasswd.conf

awk -F "<分隔符>" '<运算>{printf <列> "<连接符>"}' <指定文件>

sed -i 's/\/home\/bow/\/user\/bw/g' 6.txt


sed -i 's/<匹配内容>/<替换内容>/g' <指定文件>
```

### rpm操作
查看某个项目所属的rpm包

rpm -qf <server_name>

模糊搜索rpm包

rpm -qa | grep <keywords>


查看rpm包所有文件

rpm -ql <rpm_name>


### 查看系统服务启动顺序及耗时
systemd-analyze blame

systemd-analyze plot > a.svg（输出到文件，可直接用chrome打开）

