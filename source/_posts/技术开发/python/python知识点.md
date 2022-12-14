---
title: python知识点
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - python知识点
---
实在是对python没有好感，但是还在吃这口饭，姑且还是要提升自己的。

### Python的优势

1、Python 易于学习;

2、用少量的代码构建出很多功能（高效的高级数据结构）

3、Python 拥有海量全面的库

4、Python完全支持面向对象

5、Python 是跨平台且开源的

6、动态类型

### 解释型和编译型编程语言

解释型 python javascript php matlab

边解释边执行，将源代码解释成机器码，然后才能够执行

编译型 c c++ go

编译后再执行，一次将源代码编译成机器语言文件，之后执行不需要再编译

Java语言既具有编译语言的特征又具有解释语言的特征

### Python的解释器种类以及相关特点

CPython

使用C语言开发，官方版本的解释器，

IPython

基于CPython之上的一个交互式解释器 支持变量自动补全，自动缩进，支持bash shell命令

### PE8规范

PEP8是Python的官方文档中提供的代码规范

```python
1、使用4个空格而不是tab键进行缩进。
2、每行长度不能超过79
3、使用空行来间隔函数和类，以及函数内部的大块代码
4、必要时候，在每一行下写注释
5、使用文档注释，写出函数注释
6、在操作符和逗号之后使用空格，但是不要在括号内部使用
7、命名类和函数的时候使用一致的方式，比如使用CamelCase来命名类，使用lower_case_with_underscores来命名函数和方法
8、在类中总是使用self来作为默认
9、尽量不要使用魔法方法
10、默认使用UTF-8，甚至ASCII作为编码方式
11、换行可以使用反斜杠，最好使用圆括号。
12、不要在一句import中多个库，
13、空格的使用：
	各种右括号前不要加空格。
	逗号、冒号、分号前不要加空格。
	函数的左括号前不要加空格。如Func(1)
	序列的左括号前不要加空格。如list[2]
	操作符左右各加一个空格，不要为了对齐增加空格
	函数默认参数使用的赋值符左右省略空格	
14、不要将多句语句写在同一行，尽管使用‘；’允许
15、if/for/while语句中，即使执行语句只有一句，也必须另起一行
16、函数命名使用全部小写的方式，常量命名使用大写，类属性（方法和变量）使用小写
17、类的命名首字母大写
```

### 进制之间转换

```python
# 二进制转换成十进制-->int
v = "0b1111011"
b = int(v,2)
print(b)  
# 123

# 十进制转换成二进制--->bin
v2 = 18
print(bin(int(v2)))
# 0b10010
# ob是python的概念，代表这是一个二进制数，同理 0o 八进制，0x 十六进制

# 八进制转换成十进制
v3 = "011"
print(int(v3))
# 11

# 十进制转换成八进制：---> oct
v4 = 30
print(oct(int(v4)))
# 0o36

# 十六进制转换成十进制：
v5 = "0x12"
print(int(v5,16))
# 18

# 十进制转换成十六进制：---> hex
v6 = 87
print(hex(int(v6)))
# 0x57
```

## 六大基本数据类型

Python 类型检查
要查看变量的数据类型，可以使用type()函数
使用：`type(变量名，或者直接写变量值)`

#### &#x20;数字

整型(int) - 通常被称为是整型或整数，是正或负整数，不带小数点。Python3 整型是没有限制大小的，可以当作 Long 类型使用，所以 Python3 没有 Python2 的 Long 类型。布尔(bool)是整型的子类型。

浮点型(float) - 浮点型由整数部分与小数部分组成，浮点型也可以使用科学计数法表示（2.5e2 = 2.5 x 102 = 250）

整数进制

十进制：不能以0开头&#x20;

二进制：以0b开头&#x20;

八进制：以0o开头&#x20;

十六进制：以0x开头

#### 字符串

字符串是 Python 中最常用的数据类型。我们可以使用引号( ’ 或 " )来创建字符串。

Python 格式化符号

*   %s 字符串
*   %d 有符号的十进制整数；%0nd  代表位数不足用0代替 n:代表几位数
*   %f 浮点数（默认保留6位小数；%.nf .代表小数点 n代表.后面保留几位数

#### list(列表)

什么是列表？

用来装载不同数据类型的数据集结构

列表的特点？

*   有序的 -
*   可以装载任意数据类型&#x20;
*   可以更改的

如何表示list？

```python
# 通过list()新建一个列表
list("hello world")

# 通过[]声明一个列表
a = [1, 2, 3]
```

#### tuple(元组)

什么是元组?

可以简单地认为, 元组就是不可修改的列表, 常用来表示记录.

元组的特点?

有序的
可以装载任意数据类型
不可更改

如何表示tuple

```python
# 通过tuple()新建一个元组
tuple("hello")
# 通过(,)来声明一个元组
a = (1, 2, 3)
# 声明单个元素的元组, 要添加逗号
a = (1, )
```

#### dict(字典)

什么是字典?

字典也叫hashtable, 通过hash(散列)函数将传入的key值生成地址来查找value

key -> hash函数 -> 返回了value的地址 -> 通过地址返回value值

字典的特点?

*   无序的

> python3.6是有序的...

*   字典中的key必须是可hash的, 也就是不可更改的, 唯一的
*   可以更改的

如何表示字典？

```python
# 通过dict()来创建字典
dict(a=2)
# 通过{}来声明一个字典
a = {"a": 2}

```

#### set(集合)

什么是set？

set其实是没有value的字典

集合的特点？

*   无序的&#x20;
*   集合中的key必须是可hash的
*   可以更改的
*   元素是唯一的&#x20;

如何表示set？？

```python
# 通过set()来创建集合
set([1,2,2])
# 通过{}来表示
{1, 2, 3}

```

### 文本编码格式

python2内容进行编码（默认ascii），python3对内容进行编码的默认为utf-8。

*   ascii   最多只能用8位来表示（一个字节），即：2\*\*8 = 256，所以，ASCII码最多只能表示 256 个符号。
*   unicode  万国码，任何一个字符等于两个字节
*   utf-8     万国码的升级版  一个中文字符等于三个字节   英文是一个字节  欧洲的是 2个字节
*   gbk       国内版本  一个中文字符等于2个字节 ，英文是一个字节，gbk 转 utf-8  需通过媒介 unicode

### &#x20;机器码与字节码

*   机器码 学名机器语言指令，有时也被称为原生码，是电脑的CPU可直接解读的数据。
*   字节码 是一种中间状态（中间码）的二进制代码（文件）。需要直译器转译后才能成为机器码。

### &#x20;小数据池

#### 代码块

Python程序是由代码块构造的。块是一个python程序的文本，他是作为一个单元执行的。

代码块：一个模块，一个函数，一个类，一个文件等都是一个代码块。

而作为交互方式输入的每个命令都是一个代码块，如命令行终端。

### 代码块的缓存机制

Python在执行同一个代码块的初始化对象的命令时，会检查是否其值是否已经存在，如果存在，会将其重用。换句话说：执行同一个代码块时，遇到初始化对象的命令时，他会将初始化的这个变量与值存储在一个字典中，在遇到新的变量时，会先在字典中查询记录，如果有同样的记录那么它会重复使用这个字典中的之前的这个值。

代码块的缓存机制的适用范围：

*   int(float):任何数字在同一代码块下都会复用。
*   bool\:True和False在字典中会以1，0方式存在，并且复用。
*   str：几乎所有的字符串都会符合缓存机制。

#### &#x20;小数据池

小数据池，也称为小整数缓存机制，或者称为驻留机制

小数据池也是只针对 int(float)，str，bool，是针对不同代码块之间的缓存机制。

Python的一种优化机制，对一些常见数据进行缓存，当需要使用这个数据时，直接从池中获取，不会重复创建对象。

*   int(float):  -5\~256 的整数 进行了缓存，当你将这些整数赋值给变量时，并不会重新创建对象，而是使用已经创建好的缓存对象。
*   字符串

&#x20; 1.字符串的长度为0或者1，默认都采用了驻留机制（小数据池）。

&#x20; 2.字符串的长度>1,且只含有大小写字母，数字，下划线时，才会默认驻留。

&#x20; 3\. 乘法运算的字符串，当，乘数>=2时：仅含大小写字母，数字，下划线，总长度<=20，默认驻留。

*   bool：True，False，无论你创建多少个变量指向True，False，那么他在内存中只存在一个

#### 总结

如果在同一代码块下，则采用同一代码块下的换缓存机制。

如果是不同代码块，则采用小数据池的驻留机制。

缓存机制适用的是未运算的变量，如果变量是经过 + - % / 计算的，不适用缓存机制。

#### id, is，==

Python中，id是内存地址，比如你利用id()内置函数去查询一个数据的内存地址。

\== 是比较的两边的数值是否相等，而 is 是比较的两边的内存地址是否相等。&#x20;

要注意 is 进行比较带来的坑\* \*

### Python3和Python2的区别

```python
1：打印时，py2需要可以不需要加括号，py3 需要
python 2 ：print ('lili')   ,   print 'lili'
python 3 : print ('lili')   
python3 必须加括号

exec语句被python3废弃，统一使用exec函数

2：内涵
Python2：1，臃肿，源码的重复量很多。
         2，语法不清晰。
Python3：几乎是重构后的源码，规范，清晰，优美。

3、默认字符编码
python2中默认使用ascii,python3中默认使用utf-8

python2：要输出中文 需加 # -*- encoding:utf-8 -*-
Python3 ： 直接搞

4：input不同
python2 ：raw_input
python3 ：input 统一使用input函数

5：指定字节
python2在编译安装时，可以通过参数-----enable-unicode=ucs2 或-----enable-unicode=ucs4分别用于指定使用2个字节、4个字节表示一个unicode；
python3无法进行选择，默认使用 ucs4
查看当前python中表示unicode字符串时占用的空间：

impor sys
print（sys.maxunicode）
#如果值是65535，则表示使用usc2标准，即：2个字节表示
#如果值是1114111，则表示使用usc4标准，即：4个字节表示

6：
py2：xrange
　　　　range
py3：range  统一使用range，Python3中range的机制也进行修改并提高了大数据集生成效率

7：在包的知识点里
包：一群模块文件的集合 + __init__
区别：py2 ： 必须有__init__
　　　py3：不是必须的了

8：不相等操作符"<>"被Python3废弃，统一使用"!="

9：long整数类型被Python3废弃，统一使用int

10：迭代器iterator的next()函数被Python3废弃，统一使用next(iterator)

11：异常StandardError 被Python3废弃，统一使用Exception

12：字典变量的has_key函数被Python废弃，统一使用in关键词

13：file函数被Python3废弃，统一使用open来处理文件，可以通过io.IOBase检查文件类型
```

### &#x20;字符串、列表、元组、字典每个常用的5个方法？

```python
字符串：字符串用单引号(')或双引号(")括起来，不可变
1，find通过元素找索引，可切片，找不到返回-1
2，index，找不到报错。
3，split 由字符串分割成列表，默认按空格。
4，captalize 首字母大写，其他字母小写。
5，upper 全大写。
6，lower 全小写。
7，title，每个单词的首字母大写。
8，startswith 判断以什么为开头，可以切片，整体概念。
9，endswith 判断以什么为结尾，可以切片，整体概念。
10，format格式化输出#format的三种玩法 格式化输出res='{} {} {}'.format('egon',18,'male')  ==>  egon 18 maleres='{1} {0} {1}'.format('egon',18,'male')  ==> 18 egon 18res='{name} {age} {sex}'.format(sex='male',name='egon',age=18)
11,strip 默认去掉两侧空格，有条件， 12，lstrip,rstrip 14,center 居中，默认空格。 15，count查找元素的个数，可以切片，若没有返回0 16，expandtabs 将一个tab键变成8个空格，如果tab前面的字符长度不足8个，则补全8个， 17，replace（old，new,次数） 18，isdigit 字符串由字母或数字组成 isalpha, 字符串只由字母组成 isalnum 字符串只由数字组成 19,swapcase 大小写翻转 20，for i in 可迭代对象。 字典：1无序（不能索引）2：数据关联性强3:键值对，键值对。唯一一个映射数据类型。
#字典的键必须是可哈希的   不可变类型。
在同一个字典中，键(key)必须是唯一的。
列表是有序的对象集合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取
key： 输出所有的键
clear：清空                       
dic：删除的键如果没有则报错
pop：键值对删，有返回，没有原来的键会报错（自行设置返回键就不会报错）
popitem：随机删键值对
del：删除的键如果没有则报错
改 update
查  用get时。不会报错# 没有可以返回设定的返回值
    注意：
1、字典是一种映射类型，它的元素是键值对。
2、字典的关键字必须为不可变类型，且不能重复。
3、创建空字典使用 { }。

列表：索引，切片，加，乘，检查成员。
增加：有三种，
append：在后面添加。
Insert按照索引添加，
expend：迭代着添加。
list.extend(seq) - 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
pop 删除   (pop 有返回值)
remove 可以按照元素去删
clear  清空列表
del 1、可以按照索引去删除 2、切片 3、步长（隔着删）
改  1、索引  2、切片：先删除，再迭代着添加
list.count(obj) - 统计某个元素在列表中出现的次数
list.index(obj) - 从列表中找出某个值第一个匹配项的索引位置
list.reverse() - 反向列表中元素
list.sort([func]) - 对原列表进行排序
注意：
1、List写在方括号之间，元素用逗号隔开。
2、和字符串一样，list可以被索引和切片。
3、List可以使用+操作符进行拼接。
4、List中的元素是可以改变的。

元组：（）元组的元素不能修改
1、cmp(tuple1, tuple2)：比较两个元组元素。
2、len(tuple)：计算元组元素个数。
3、max(tuple)：返回元组中元素最大值。
4、min(tuple)：返回元组中元素最小值。
5、tuple(seq)：将列表转换为元组。
注意
1、与字符串一样，元组的元素不能修改。
2、元组也可以被索引和切片，方法一样。
3、注意构造包含0或1个元素的元组的特殊语法规则。
4、元组也可以使用+操作符进行拼接。


Set（集合）：集合（set）是一个无序不重复元素的序列。
可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
```

### lambda表达式

```python
函数名 = lambda 参数 ：返回值

#参数可以有多个，用逗号隔开
#匿名函数不管逻辑多复杂，只能写一行，且逻辑执行结束后的内容就是返回值
#返回值和正常的函数一样可以是任意数据类型

lambda 表达式
temp = lambda x,y:x+y
print(temp(4,10))   # 14
```

转载自 https://www.cnblogs.com/JetpropelledSnake/p/9396511.html
