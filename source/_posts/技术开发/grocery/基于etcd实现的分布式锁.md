---
title: 基于etcd实现的分布式锁
date: 2022-12-15 23:41:44
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 基于etcd实现的分布式锁
---
- lock.sh
```bash
\#!/bin/bash

# @CreateTime:   2021-03-23 16:00:00

# @Description:  分布式锁

# @Note:         在axis中实现分布式锁时，由于Python的语言特性，导致性能特别差；

# 因此这里直接基于etcd进行实现，对性能有大幅提升！

# 锁名

LOCK\_NAME=""

# 会话超时时间，即服务异常退出时锁的最长自动释放时间，单位/秒

TTL=30

# 是否本地锁，如果是本地锁，那么作用和flock类似，不会对集群的其他节点造成影响

IS\_LOCAL=false

# 待执行命令

COMMAND=""

# 连接|获取锁|释放锁的超时时间，单位/秒

TIMEOUT=""

# 是否输出调试信息

DEBUG=false

# 函数: 用法说明

function usage()
{
echo
echo "Usage: dlock \[-n|--name] \[-t|--ttl] \[-w|--timeout] \[-l|--local] \[-d|--debug] \[-h|--help] \<command> \[command args]"
echo
echo "Options:"
echo "  -n  --name        锁名，默认为被执行命令名"
echo "  -t  --ttl         会话超时时间，即服务异常退出时锁的最长自动释放时间，单位/秒"
echo "  -w  --timeout     连接超时时间，单位/秒"
echo "  -l  --local       本地锁，类似flock"
echo "  -d  --debug       输出调试信息"
echo "  -h  --help        输出帮助信息并退出"
echo

    exit 1

}

# 函数: 解析命令行参数

function parse\_cmdline\_args()
{
local parsed\_args
parsed\_args=`$(getopt -a -n dlock -o n:t:w:ldh --long name:,ttl:,timeout:,local,debug,help -- "$`@")
if \[ \$? -ne 0 ]; then
usage
fi

    eval set -- "$parsed_args"
    while true; do
        case "$1" in
            -n | --name)    LOCK_NAME="$2"         ; shift 2  ;;
            -t | --ttl)     TTL=$2                 ; shift 2  ;;
            -w | --timeout) TIMEOUT=$2             ; shift 2  ;;
            -l | --local)   IS_LOCAL=true          ; shift    ;;
            -d | --debug)   DEBUG=true             ; shift    ;;
            -h | --help)    usage ;;
            --)             shift; break ;;
            *)              usage ;;
        esac
    done

    # 剩余参数就当做被执行命令看待
    COMMAND="$@"
    if [ -z "$COMMAND" ]; then
        usage
    fi

}

# 函数: 主函数

function main()
{
parse\_cmdline\_args "\$@"

    # 未指定锁名的情况下，默认使用可执行文件作为锁名
    if [ -z "$LOCK_NAME" ]; then
        LOCK_NAME=$(echo $COMMAND | awk '{print $1}')
    fi

    # 为本地锁的情况下，使用主机名作为锁名前缀
    if [ $IS_LOCAL = true ]; then
        local hostname
        hostname=$(hostname)
        LOCK_NAME="$hostname/$LOCK_NAME"
    fi

    # 目前基于etcd来实现分布式锁
    if [ ! -z "$TIMEOUT" ]; then
        export ETCDCTL_CONNECTION_TIMEOUT=$TIMEOUT
    fi
    # TODO: 需要把etcdctl的第一行warning日志去掉或者过滤掉
    /sf/bin/etcdctl lock --debug=$DEBUG --ttl=$TTL "$LOCK_NAME" $COMMAND

}

main "\$@"
```
