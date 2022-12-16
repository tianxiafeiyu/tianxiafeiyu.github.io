---
title: python脚本接收参数的几种实现方式
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - python脚本接收参数的几种实现方式
---
### sys.argv

sys.argv\[] 可以接收脚本的参数，得到一个列表类型，列表第一个元素是脚本名称。

    import sys

    arg1 = sys.argv[0]
    arg2 = sys.argv[1]
    arg4 = sys.argv[2]

    # e.g. 
    # python test_func.py test_arg1 test_arg2
    # arg1: test_func.py
    # arg1: test_arg1
    # arg1: test_arg2

### argparse

python专门用于处理命令行参数的标准库

    import argparse


    if __name__ == '__main__':
        parser = argparse.ArgumentParser(
            prog='cmdb_mock',
            description='mock tool for cmdb',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('action')

        parser.add_argument('-size', dest='size', type=int, default=10,
                            help=u'number of resource mock')
        args = parser.parse_args()

        actiom = args.action
        size = args.size
        

    # python cmdb_mock.py create -size 100

