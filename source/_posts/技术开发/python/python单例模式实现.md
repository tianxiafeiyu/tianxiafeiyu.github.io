---
title: python单例模式实现
---
## 装饰器
```
from functools import wraps
import threading

lock = threading.Lock()

def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return wrapper

@singleton
class MyClass:
    def __init__(self, *args, **kwargs):
        print('MyClass.__init__ called.')
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def cls_method(cls, *args, **kwargs):
        print('Myclass classmethod called.')
```
测试一下：
```
In [2]: a = MyClass(1, 2)
MyClass.__init__ called.

In [3]: b = MyClass(3,4,5)

In [4]: a is b
Out[4]: True

In [5]: a.__dict__
Out[5]: {'args': (1, 2), 'kwargs': {}}

In [6]: b.__dict__
Out[6]: {'args': (1, 2), 'kwargs': {}}
```
可见a和b两个实例其实是一个对象，Myclass只被调用了一次。加锁的目的是为了达到线程安全，防止在操作instances字典的时候被其他线程抢占到时间片执行而重复创建实例。这种方式确实实现了单例模式，但是MyClass现在变成一个函数了，所以不能直接用MyClass调用cls_method了，只能通过实例调用…
```
In [7]: MyClass.cls_method()
---------------------------------------------------------------------------
TypeError Traceback (most recent call last)
<ipython-input-7-7bcbf0e7bf90> in <module>()
----> 1 MyClass.cls_method()

TypeError: 'classmethod' object is not callable

In [8]: a.cls_method()
Myclass classmethod called.COPY
```
## 模块导入
第二种方法是在一个独立模块中创建好实例后导入，由于Python不会重复导入已经导入的对象，因此这样也能实现单例模式:
```
# one.py

print('one.py imported by others.')

class Foobar:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

foo = Foobar(1, '2', x=3)

# two.py
from one import foo
print(id(foo))

from one import foo
print(id(foo))
```
运行two.py:
```
❯ python3 two.py                                                                                                                                                 
one.py imported by others.
140485279112104
140485279112104COPY
```
这样做的优点是简单，缺点和装饰器一样，只能通过实例来调用classmethod.

## __new__

第三种，改写__new__方法:
```
import threading

class Singleton:
    instances = {}
    lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls.lock:
            if cls not in cls.instances:
                cls.instances[cls] = super().__new__(cls)
            return cls.instances[cls]

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargsCOPY
```
测试：
```
In [2]: a = Singleton(1, '2', x=3)

In [3]: b = Singleton(3, '4', y=5)

In [4]: a is b
Out[4]: True

In [5]: a
Out[5]: <one.Singleton at 0x7f7132af6550>

In [6]: b
Out[6]: <one.Singleton at 0x7f7132af6550>

In [7]: a.__dict__
Out[7]: {'args': (3, '4'), 'kwargs': {'y': 5}}

In [8]: b.__dict__
Out[8]: {'args': (3, '4'), 'kwargs': {'y': 5}}
```
前后两个实例是同一个，这点证明确实是单例模式了，但为什么a的属性变了？这个问题，在第四种方法中一并解释。这种方法的缺点是，如果子类改写了__new__方法，那么单例模式就失效了，比如：
```
import threading

class Singleton:
    instances = {}
    lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__new__(cls)
        return cls.instances[cls]

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class Subclass(Singleton):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
```
测试：
```
In [2]: a = Subclass(1, '2', x=3)

In [3]: b = Subclass(3, '4', y=5)

In [4]: a
Out[4]: <one.Subclass at 0x7fe97ad65e80>

In [5]: b
Out[5]: <one.Subclass at 0x7fe97add2a20>

In [6]: a is b
Out[6]: False
```
## metaclass
第四种方法，使用元类：
```
import threading

class Meta(type):
    instances = {}
    lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls.lock:
            if cls not in cls.instances:
                cls.instances[cls] = super().__call__(*args, **kwargs)
            return cls.instances[cls]

class Singleton(metaclass=Meta):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
```
测试：
```
In [2]: a = Singleton(1, '2', x=3)

In [3]: b = Singleton(3, '4', y=5)

In [4]: a is b
Out[4]: True

In [5]: a.__dict__
Out[5]: {'args': (1, '2'), 'kwargs': {'x': 3}}

In [6]: b.__dict__
Out[6]: {'args': (1, '2'), 'kwargs': {'x': 3}}
```
可以看到，a和b是同一个对象，确实是单例模式，但是跟第三种方法不同的是，实例属性是以第一次调用为准，为什么呢？

实例完整的创建过程是这样的：

1.调用Metaclass.__call__

2.Metaclass.__call__调用Class.__new__创建instance

3.Metaclass.__call__以instance和其他参数去调用Class.__init__进行初始化

4.Metaclass.__call__返回instance
在第四种方法，实例已经创建后，就不会再去调用Class.__new__创建实例和Class.__init__进行初始化了，因此实例属性由第一次创建决定。而第三种方法，虽然Class.__new__不会重复创建实例，但是Class.__init__还是会被调用，因此属性随最后一次而定。
使用元类的好处是，元类会附着到子类上，单例模式不会因为继承而失效：
```
class Meta(type):
    pass

class SupClass(metaclass=Meta):
    pass

class SubClass(SupClass):
    pass

print(type(SupClass), type(SubClass))
```
运行结果：
```
<class '__main__.Meta'> <class '__main__.Meta'>
```
因此，以上四种方法，元类的解决方案是最好的！