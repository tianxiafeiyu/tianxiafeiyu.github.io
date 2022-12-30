---
title: cpu加压脚本
date: 2022-12-30 23:10:53
updated: 2022-12-30 21:36:16
toc: true
tags: 
    - cpu加压脚本
---

```shell
#! /bin/bash
#############################################################
#       this scripts for cpu usage testing
#       eg.  cpu_test.sh start  50 #start testing use 50% cpu
#       eg.  cpu_test.sh stop  #stop testing
#############################################################
op=$1
num=$2

mkcsp()
{

        touch ./killcpu.c
        echo 'int main(){while(1);return 0;}' > killcpu.c
        gcc -o out killcpu.c
        chmod +x ./out

}

start()
{
cpu_num=$(cat /proc/cpuinfo | grep "physical id" | wc -l)

for i in `seq 1 $(expr $num \* $cpu_num / 100)`
        do
            ./out &
        done

}

stop()
{
for i in $( ps -ef | grep './out'| grep -v grep | awk '{print $2}')
        do
                kill -9 $i
        done
rm -rf killcpu.c out
}

main()
{
if [ $op == "start" ]
then
        mkcsp
fi
        $op
}


main
```