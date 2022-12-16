---
title: mysql联合索引
date: 2022-12-15 23:39:27
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - mysql联合索引
---
sqlalchemy 创建联合索引，报索引超长问题:

`DBError: (pymysql.err.InternalError) (1071, u'Specified key was too long; max key length is 3072 bytes')`

mysql联合索引最大长度为3072，这个长度是怎么计算的呢？

### 索引限制
```
(5.6里面默认不能超过767bytes，5.7不超过3072bytes)：

起因是256×3-1=767。这个3是字符最大占用空间（utf8）。但是在5.5以后，开始支持4个字节的uutf8。255×4>767, 于是增加了一个参数叫做 innodb_large_prefix

# 256的由来： 只是因为char最大是255，所以以前的程序员以为一个长度为255的index就够用了，所以设置这个256.历史遗留问题。   --- by 阿里-丁奇
```

字段1字符长度 * 字符最大占用空间 + 字段2字符长度 * 字符最大占用空间 + ...

这个字符最大占用空间取决于编码格式，utf8为3，utf8mb4为4



### 外键约束
CASCADE：对父表进行delete，update操作时，子表也会delete，update掉关联的记录。更新/删除主表中记录时自动更新/删除子表中关联记录。

RESTRICT：如果想要删除/更新父表的记录时，而子表中有关联该父表的记录，则不允许删除/更新父表中的记录

SET NULL：对父表进行delete，updat操作时，会将子表中关联的记录外键所在列设置为null，在设置时该列应设置为可以为null
NO ACTION：同 RESTRICT，立即检查外键约束

外键约束作用的是主表，所以对子表做删除、更新、删表等操作，都不影响。
