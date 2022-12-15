---
title: jsonpath使用心得
---

JsonPath表达式通常是用来路径检索或设置Json的。其表达式可以接受“dot–notation”和“bracket–notation”格式，例如$.store.book[0].title、$[‘store’][‘book’][0][‘title’]

## 操作符

符号 | 说明
---|---
$ | 查询的根节点对象，用于表示一个json数据，可以是数组或对象
@ | 当前节点，类似于this
\* | 通配符，可以表示一个名字或数字
.<name> | 表示一个子节点
..<name> | 深度查询
[‘<name>’ (, ‘<name>’)] |一个或多个子节点
[<number> (, <number>)] |一个或多个数组下标
[start:end] |数组片段，区间为[start,end),不包含end
[?(<expression>)]|过滤器表达式，表达式结果必须是boolean

## 函数
可以在JsonPath表达式执行后进行调用，其输入值为表达式的结果。

名称 | 描述	| 输出
---|---|--
min() |	获取数值类型数组的最小值 |	Double
max() |	获取数值类型数组的最大值 |	Double
avg() |	获取数值类型数组的平均值 |	Double
stddev() |	获取数值类型数组的标准差 |	Double
length() |	获取数值类型数组的长度 |	Integer
## 过滤器
过滤器是用于过滤数组的逻辑表达式，一个通常的表达式形如：`[?(@.age > 18)]`，可以通过逻辑表达式&&或||组合多个过滤器表达式，例如 `[?(@.price < 10 && @.category == ‘fiction’)]`，字符串必须用单引号或双引号包围，例如 `[?(@.color == ‘blue’)] or [?(@.color == “blue”)]`。

操作符| 描述
--|--
== |	等于符号，但数字1不等于字符1(note that 1 is not equal to ‘1’)
!= |	不等于符号
< |	小于符号
<= |	小于等于符号
> |	大于符号
>= |	大于等于符号
=~ |	判断是否符合正则表达式，例如[?(@.name =~ /foo.*?/i)]
in |	所属符号，例如[?(@.size in [‘S’, ‘M’])]
nin |	排除符号
size |	size of left (array or string) should match right
empty |	判空符号

注意：正则过滤 =~，貌似是无效的

## 常见用法
```
{
    "count": 2,
    "success": 1,
    "data": [
        {
            "name": "xiaoxing-y9000p",
            "cpu": "i7 12700k",
            "gpu": "RTX3080",
            "price": 9999
        },
        {
            "name": "xiaomi4",
            "cpu": "rz6800h",
            "gpu": "RTX3060",
            "price": 6999,
        }
    ]
}
```
json数据是一条接口查询返回

- $.count 获得数据条数
- $.data.name 获取所有电脑名称
- $.data[?(@.price)>9000] 获取价格超过9000的电脑

python中使用过jsonpath获取json指定数据
```
import jsonpath

laptop_json = '{"count":2,"success":1,"data":[{"name":"xiaoxing-y9000p","cpu":"i7 12700k","gpu":"RTX3080","price":9999},{"name":"xiaomi4","cpu":"rz6800h","gpu":"RTX3060","price":6999}]}'

laptop_data= json.loads(laptop_json)

names = jsonpath.jsonpath(laptop_data, "$.data.name")
# ["xiaoxing-y9000p", "name"]
```