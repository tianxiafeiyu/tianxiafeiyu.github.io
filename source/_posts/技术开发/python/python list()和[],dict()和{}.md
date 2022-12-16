---
title: python list()和[],dict()和{}
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - python list()和[],dict()和{}
---
参考资料： https://www.cnblogs.com/wlfya/p/13856482.html

Python疑难问题：[] 与 list() 哪个快？为什么快？快多少呢？

在日常使用 Python 时，我们经常需要创建一个列表，相信大家都很熟练了吧？
```
# 方法一：使用成对的方括号语法
list_a = []

# 方法二：使用内置的 list()
list_b = list()
```

结论：[] 是 list() 的三倍快
2、list() 比 [] 执行步骤多
那么，我们继续来分析一下第二个问题：为什么 [] 会更快呢？

这一次我们可以使用dis模块的 dis() 函数，看看两者执行的字节码有何差别：
```
>>> from dis import dis
>>> dis("[]")
>>> dis("list()")
```
结果
```
>>> dis("[1]")
          0 DELETE_NAME     23857 (23857)
>>> dis("list(1)")
          0 IMPORT_NAME     29545 (29545)
          3 LOAD_GLOBAL     12584 (12584)
          6 STORE_SLICE+1
>>>
```
前者明显少了步骤
```
>>> from dis import dis
>>> dis("{1}")
          0 <123>           32049
>>> dis("dict(1)")
          0 LOAD_CONST      25449 (25449)
          3 LOAD_GLOBAL     12584 (12584)
          6 STORE_SLICE+1
>>>
```
{}初始化，只需要通过一次常量指令即可完成
dict()，需要执行CALL_FUNCTION指令