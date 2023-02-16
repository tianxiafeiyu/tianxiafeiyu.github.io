### mysql中的NULL
NULL在MySQL中是一个非常特殊的值，官方表述为“一个未知的值”，NULL不与任何值相等（包括其本身）。

### NULL的长度
```
mysql> select length(NULL), length(''), length(0), length(FALSE);
+--------------+------------+-----------+---------------+
| length(NULL) | length('') | length(0) | length(FALSE) |
+--------------+------------+-----------+---------------+
|         NULL |          0 |         1 |             1 |
+--------------+------------+-----------+---------------+
```
可以看出空值''的长度是0，是不占用空间的；而的NULL长度是NULL，是需要占用额外空间的，所以在一些开发规范中，建议将数据库字段设置为Not NULL,并且设置默认值''或0。

NULL值占用字节空间，具体是多少呢，好像找不到权威的相关资料，部分资料说InnoDB中是1字节

### NULL对查询的影响
NULL对数学比较运算符（>, =, <=, <>）运算出的结果都是FALSE

NULL只支持IS NULL、IS NOT NULL、IFNULL()操作

MIN()、SUM()、COUNT()在运算时会忽略NULL值，但是COUNT(*)不会忽略；

DISTINCT、GROUP BY、ORDER BY中认为所有的NULL值都是相等的；ORDER BY认为NULL是最小的值

### NULL对索引的影响
MySQL中某一列数据含有NULL，并不一定会造成索引失效。

MySQL可以在含有NULL的列上使用索引

在有NULL值得字段上使用常用的索引，如普通索引、复合索引、全文索引等不会使索引失效。但是在使用空间索引的情况下，该列就必须为 NOT NULL。

### NULL对数据的影响
TIMESTAMP类型的字段被插入NULL时，实际写入到表中的是当前时间；

AUTO_INCREMENT属性的字段被插入NULL时，实际写入到表中的是顺序的下一个自增值

想要禁止某个字段被设置为NULL，则对此字段设置NOT NULL属性；

与oracle不同，mysql的唯一索引中允许有NULL字段，但是可能会出现意料之外的数据
比如，uniq_index(a, b, c), insert(1, 2, NULL)；insert(1, 2, NULL)都会成功

因为对于联合索引 a-b-c，1-2-NULL和1-2-NULL的比较结果总会返回false