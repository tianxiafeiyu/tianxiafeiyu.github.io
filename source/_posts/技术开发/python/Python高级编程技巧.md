---
title: Python高级编程技巧
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Python高级编程技巧
---

## 推导式(Comprehensions)

### 列表推导(list comprehensions)
```python
num = [1, 4, -5, 10, -7, 2, 3, -1]
filtered_and_squared = [ x**2 for x in num if x > 0]
# 等效于 filtered_and_squared = map(lambda x: x ** 2, filter(lambda x: x > 0, num))
print filtered_and_squared
 
# [1, 16, 100, 4, 9]
```
整个列表必须一次性加载于内存之中

### 生成器推导(Generatorst comprehensions)
```python
num = [1, 4, -5, 10, -7, 2, 3, -1]
filtered_and_squared = ( x**2 for x in num if x > 0 )
print filtered_and_squared
 
# <generator object <genexpr> at 0x00583E18>
 
for item in filtered_and_squared:
    print item
 
# 1, 16, 100 4,9
```
每次遍历加载一个列表元素

## 装饰器(Decorators)
装饰器是一个包装了另一个函数的特殊函数：主函数被调用，并且其返回值将会被传给装饰器，接下来装饰器将返回一个包装了主函数的替代函数，
```python
# 统计运行时间装饰器
def print_runtime(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()

        print '%s方法运行时间：%s s' % (func.__name__, t2 - t1)

    return wrap
```

## 类成员变量初始化
建议所有变量初始化在__init()__方法下进行，且可变类型的变量不可以设置默认函数参数，否则也会导致共享变量。

```python
class Node(object):
    parents = [] # 危险操作1：init方法外定义可变类型变量

    def __init__(self, children=[]): # 危险操作2：init方法内定义但设置了函数默认参数
        self.children = children


if __name__ == '__main__':
    n1 = Node()
    n2 = Node()
    n1.parents.append('parent for n1')
    n1.children.append('child for n1')

    print 'n1 parents: id: {}, value: {}'.format(id(n1.parents), n1.parents)
    print 'n2 parents: id: {}, value: {}'.format(id(n2.parents), n2.parents)
    print 
    print 'n1 children: id: {}, value: {}'.format(id(n1.children), n1.children)
    print 'n2 children: id: {}, value: {}'.format(id(n2.children), n2.children)

# n1 parents: id: 40216072, value: ['parent for n1']
# n2 parents: id: 40216072, value: ['parent for n1']
# 
# n1 children: id: 40159112, value: ['child for n1']
# n2 children: id: 40159112, value: ['child for n1']
```

## 函数式编程
#### Lambda
我们可以在 Python 中使用 lambda 关键字来定义此类函数。示例如下：
```python
mult = lambda x, y: x * y
mult(1, 2) #returns 2
```
该 mult 函数的行为与使用传统 def 关键字定义函数的行为相同。

注意：lambda 函数必须为单行，且不能包含程序员写的返回语句。

事实上，它们通常具备隐式的返回语句（在上面的示例中，函数想表达 return x * y，不过我们省略了 lambda 函数中的显式返回语句）。

lambda 函数更加强大和精准，因为我们还可以构建匿名函数（即没有名称的函数）：
```python
(lambda x, y: x * y)(9, 10) #returns 90
```
当我们只需要一次性使用某函数时，这种方法非常方便。例如，当我们想填充字典时：
```python
import collections
pre_fill = collections.defaultdict(lambda: (0, 0))
#all dictionary keys and values are set to 0
```

#### Map
map 函数基于指定过程（函数）将输入集转换为另一个集合。这类似于上文提到的 iterate_custom 函数。例如：
```python
def multiply_by_four(x):
    return x * 4
scores = [3, 6, 8, 3, 5, 7]
modified_scores = list(map(multiply_by_four, scores))
#modified scores is now [12, 24, 32, 12, 20, 28]
```
在 Python 3 中，map 函数返回的 map 对象可被类型转换为 list，以方便使用。现在，我们无需显式地定义 multiply_by_four 函数，而是定义 lambda 表达式：
```python
modified_scores = list(map(lambda x: 4 * x, scores))
```
当我们想对集合内的所有值执行某项操作时，map 函数很有用。

#### Filter
就像名称所显示的那样，filter 函数可以帮助筛除不想要的项。例如，我们想要去除 scores 中的奇数，那么我们可以使用 filter：
```python
even_scores = list(filter(lambda x: True if (x % 2 == 0) else False, scores))
#even_scores = [6, 8]
```

由于提供给 filter 的函数是逐个决定是否接受每一个项的，因此该函数必须返回 bool 值，且该函数必须是一元函数（即只使用一个输入参数）。

#### Reduce
reduce 函数用于「总结」或「概述」数据集。例如，如果我们想要计算所有分数的总和，就可以使用 reduce：
```python
sum_scores = reduce((lambda x, y: x + y), scores)
#sum_scores = 32
```
这要比写循环语句简单多了。注意：提供给 reduce 的函数需要两个参数：一个表示正在接受检查的项，另一个表示所用运算的累积结果。

### 参考资料
https://www.cnblogs.com/ajianbeyourself/p/3970508.html

