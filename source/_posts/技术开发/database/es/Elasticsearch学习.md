---
title: Elasticsearch学习
date: 2022-12-16 00:43:25
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Elasticsearch学习
---

最近在做skywalking相关的项目，skywalking使用了Elasticsearch对数据指标进行存取，要理解skywalking的工程项目，就需要对 Elasticsearch 有一定的了解。

转载自 https://www.jianshu.com/p/d48c32423789

## 什么是 Elasticsearch
https://www.elastic.co/cn/elasticsearch


Elasticsearch是一个开源的分布式、RESTful 风格的搜索和数据分析引擎，它的底层是开源库Apache Lucene。

Elasticsearch用 Java 编写，内部采用 Lucene 做索引与搜索，但是它的目标是使全文检索变得更简单，简单来说，就是对Lucene 做了一层封装，它提供了一套简单一致的 RESTful API 来帮助我们实现存储和检索。

Elasticsearch 不仅仅是 Lucene，并且也不仅仅只是一个全文搜索引擎。 它可以被下面这样准确地形容：

- 一个分布式的实时文档存储系统，每个字段可以被索引与搜索；
- 一个分布式实时分析搜索引擎；
- 能胜任上百个服务节点的扩展，并支持 PB 级别的结构化或者非结构化数据。

现在，Elasticsearch已成为全文搜索领域的主流软件之一。维基百科、卫报、Stack Overflow、GitHub等都纷纷采用它来做搜索。

##  Elasticsearch 一些概念
【Cluster】

集群,一个ES集群由一个或多个节点(Node)组成,每个集群都有一个cluster name作为标识

【node】

节点,一个ES实例就是一个node,一个机器可以有多个实例,所以并不能说一台机器就是一个node，大多数情况下每个node运行在一个独立的环境或者虚拟机上。

【index】
索引，即文档的集合

【shard】

1. 分片,ES是分布式搜索引擎,每个索引有一个或多个分片,索引的数据被分配到各个分片上，相当于一桶水分N个杯子装。
2. 分片有助于横向扩展，N个分片会尽可能平均地分配在不同的节点上。（2个节点，4个分片，则每个节点会分到2个分片。后面增加2个节点后，ES会自动感知进行分配，每个节点一个分片）
3. 分片是独立的。
4. 每个分片都是一个Lucene Index，所以一个分片只能存放Integer.MAX_VALUE-128=2,147,483,519个docs。
5. 分片中有 主分片（primary shard）和备份分片（replica shard），主分片和备份分片不会出现在同一个节点上（防止单点故障），默认情况下一个索引会创建5个分片及它们的备份（5primary 5replica=10个分片）。如果只有一个节点，备份分片将会无法分配（unassigned）,此时集群状态为Yellow。
6. 对于一个索引，除非重建索引，否则不能调整分片数目（主分片数目, number_of_shards）,但是可以随时调整备份分片数目（number_of_replicas）

【ES集群状态】
- Green：所有主分片和备份分片都准备就绪（分配成功）。
- Yellow：所有主分片准备就绪，存在至少一个备份分片没有准备就绪。
- Red：存在至少一个主分片没有准备就绪，此时查询可能会出现数据丢失。

【replica作用】
- 容灾：primary分片丢失,replica分片就会被顶上去成为新的主分片,同时根据这个新的主分片创建新的replica，集群数据安然无恙。
- 提高查询性能：主分片和备份分片的数据是相同的，所有对于查询请求既可以查主分片也可以查备份分片，在合适的范围内多个replica性能会更优。


### 1. 文档

#### 1.1 什么是文档？

对象 or 文档
```
{
    "name":         "John Smith",
    "age":          42,
    "confirmed":    true,
    "join_date":    "2014-06-01",
    "home": {
        "lat":      51.5,
        "lon":      0.1
    },
    "accounts": [
        {
            "type": "facebook",
            "id":   "johnsmith"
        },
        {
            "type": "twitter",
            "id":   "johnsmith"
        }
    ]
}
```
通常情况下，我们使用的术语 `对象` 和 `文档` 是可以互相替换的。不过，有一个区别： 一个对象仅仅是类似于 hash 、 hashmap 、字典或者关联数组的 JSON 对象，对象中也可以嵌套其他的对象。 对象可能包含了另外一些对象。在 Elasticsearch 中，`文档` 有着特定的含义。它是指最顶层或者根对象, 这个根对象被序列化成 JSON 并存储到 Elasticsearch 中，指定了唯一 ID。

#### 1.2 文档元数据
一个文档不仅仅包含它的数据 ，也包含 元数据 —— 有关 文档的信息。
三个必须的元数据元素如下：
- _index  
 文档在哪存放  
  我们可以简单理解为一个文档存储在一个索引内，索引和文档是一对多的关系。  
>  实际上，在 Elasticsearch 中，我们的数据是被存储和索引在 分片 中，而一个索引仅仅是逻辑上的命名空间， 这个命名空间由一个或者多个分片组合在一起。 然而，这是一个内部细节，我们的应用程序根本不应该关心分片，对于应用程序而言，只需知道文档位于一个 索引 内。 Elasticsearch 会处理所有的细节。

- _type  
 文档表示的对象类别  
  `types` （类型）允许在索引中对数据进行逻辑分区。不同 `types` 的文档可能有不同的字段，但最好能够非常相似。一个  `_type` 命名可以是大写或者小写，但是不能以下划线或者句号开头，不应该包含逗号， 并且长度限制为256个字符。

- _id  
文档唯一标识  
它和 _index 以及 _type 组合就可以唯一确定 Elasticsearch 中的一个文档。  
创建一个新的文档时，可以指定 `_id` ，也可以让 Elasticsearch 自动生成。

当然，还有很多其他的元数据


### 2. 分布式文档存储
#### 2.1 文档的存放位置

当索引一个文档的时候，文档会被存储到一个主分片中。 Elasticsearch 如何知道一个文档应该存放到哪个分片中呢？当我们创建文档时，它如何决定这个文档应当被存储在分片 1 还是分片 2 中呢？

首先这肯定不会是随机的，否则将来要获取文档的时候我们就不知道从何处寻找了。实际上，这个过程是根据下面这个公式决定的：
```
shard = hash(routing) % number_of_primary_shards
```
`routing ` : 可变值，默认是文档的 _id ，也可以设置成一个自定义的值

`number_of_primary_shards ` : 主分片的数量

`shard` : 文档所在分片的位置，取值范围 [0, number_of_primary_shards-1]

这也解释了为什么创建索引的时候就确定好主分片的数量 并且永远不会改变这个数量：因为如果数量变化了，那么所有之前路由的值都会无效，文档也再也找不到了。

> 你可能觉得由于 Elasticsearch 主分片数量是固定的会使索引难以进行扩容。实际上当你需要时有很多技巧可以轻松实现扩容。

**所有的文档 API（ get 、 index 、 delete 、 bulk 、 update 以及 mget ）都接受一个叫做 routing 的路由参数 ，通过这个参数我们可以自定义文档到分片的映射。一个自定义的路由参数可以用来确保所有相关的文档——例如所有属于同一个用户的文档——都被存储到同一个分片中**。

#### 2.2 主分片和副本分片如何交互
##### 2.2.1 分片分布规则
假设有一个集群由三个节点组成。 它包含一个叫 blogs 的索引，有两个主分片，每个主分片有两个副本分片，相同分片的副本不会放在同一节点。类似如下图：

![集群](https://note.youdao.com/yws/api/personal/file/410BA879B6594958B1AAC8F3DF0DD8F7?method=getImage&version=8841&cstk=XTuNqpzO)

我们可以发送请求到集群中的任一节点。 每个节点都有能力处理任意请求。 每个节点都知道集群中任一文档位置，所以可以直接将请求转发到需要的节点上。负责转发的节点称为 ***协调节点(coordinating node)***。

##### 2.2.2 索引、新建和删除
```
# 索引文档- 存储和使文档可被搜索 (也可以作为更新功能)
PUT /{index}/{type}/{id}
{
  "field": "value",
  ...
}

// 例如
PUT /website/blog/123
{
  "title": "My first blog entry",
  "text":  "Just trying this out...",
  "date":  "2014/01/01"
}

# 新建新文档（与索引的区分就是确保生成新的文档，而不是覆盖）
POST /website/blog/  # es自动生成_id，保证唯一
{ ... }

PUT /website/blog/123/_create   # 指定 _id 为 123，若是已存在_id，则创建失败并且返回409
{ ... }

# 删除文档
DELETE /{index}/{type}/{id}

```
***注意：在 Elasticsearch 中文档是 不可改变 的，不能修改它们。如果想要更新现有的文档，需要 重建索引 或者进行替换***

新建、索引和删除 请求都是 写 操作， 必须在主分片上面完成之后才能被复制到相关的副本分片，如下图所示：

![新建、索引和删除单个文档](https://note.youdao.com/yws/api/personal/file/6A476F43F8264DDBB17485EF3150A97B?method=getImage&version=7159&cstk=kixc2ey7)

以下是在主副分片和任何副本分片上面 成功新建，索引和删除文档所需要的步骤顺序：

1. 客户端向 `Node 1` 发送新建、索引或者删除请求。
1. 节点使用文档的 `_id` 确定文档属于分片 0 。请求会被转发到 `Node 3`，因为分片 0 的主分片目前被分配在 `Node 3` 上。
1. `Node 3` 在主分片上面执行请求。如果成功了，它将请求并行转发到 `Node 1` 和 `Node 2` 的副本分片上。一旦所有的副本分片都报告成功, `Node 3` 将向协调节点报告成功，协调节点向客户端报告成功。

在客户端收到成功响应时，文档变更已经在主分片和所有副本分片执行完成，变更是安全的。

##### 2.2.3 单文档查询
```
GET /website/blog/123?pretty
#pretty 参数，将会调用 Elasticsearch 的 pretty-print 功能，该功能将会格式化数据，提高可读性。

# 获取文档部分内容
GET /website/blog/123?_source=title,text

# 只想得到 _source 字段，不需要任何元数据
GET /website/blog/123?_source
```

响应体包括常见元数据元素，再加上  `_source` 字段，这个字段包含我们索引数据时发送给 Elasticsearch 的原始 JSON 文档：
```
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 1,
  "found" :    true,
  "_source" :  {
      "title": "My first blog entry",
      "text":  "Just trying this out...",
      "date":  "2014/01/01"
  }
}
```


Get 获取文档，可以从主分片或者从其它任意副本分片检索文档 ，如下图所示：

![获取文档](https://note.youdao.com/yws/api/personal/file/A249BA20D8BC434FB1329C7EE93D2093?method=getImage&version=8204&cstk=XTuNqpzO)

以下是从主分片或者副本分片检索文档的步骤顺序：

1. 客户端向 `Node 1` 发送获取请求。

1. 节点使用文档的 `_id` 来确定文档属于分片 0 。分片 0 的副本分片存在于所有的三个节点上。 在这种情况下，它将请求转发到 `Node 2` 。

1. `Node 2` 将文档返回给 `Node 1` ，然后将文档返回给客户端。

在处理读取请求时，协调结点在每次请求的时候都会通过轮询所有的副本分片来达到负载均衡。

在文档被检索时，已经被索引的文档可能已经存在于主分片上但是还没有复制到副本分片。 在这种情况下，副本分片可能会报告文档不存在，但是主分片可能成功返回文档。 一旦索引请求成功返回给用户，文档在主分片和副本分片都是可用的。

##### 2.2.4 局部更新文档

update 请求最简单的一种形式是接收文档的一部分作为 doc 的参数， 它只是与现有的文档进行合并。对象被合并到一起，覆盖现有的字段，增加新的字段。 例如，我们增加字段 tags 和 views 到我们的博客文章，如下所示：
```
POST /website/blog/1/_update
{
   "doc" : {
      "tags" : [ "testing" ],
      "views": 0
   }
}
```
如果请求成功，我们看到类似于 index 请求的响应：
```
{
   "_index" :   "website",
   "_id" :      "1",
   "_type" :    "blog",
   "_version" : 3
}
```
检索文档显示了更新后的 _source 字段：
```
{
   "_index":    "website",
   "_type":     "blog",
   "_id":       "1",
   "_version":  3,
   "found":     true,
   "_source": {
      "title":  "My first blog entry",
      "text":   "Starting to get the hang of this...",
      "tags": [ "testing" ],    #新添加
      "views":  0   #新添加
   }
}
```

局部更新文档，`update` API 结合了先前说明的读取和写入模式：

![局部更新文档](https://note.youdao.com/yws/api/personal/file/E5B6A405579E4720854EAFF23B14CC0A?method=getImage&version=7157&cstk=kixc2ey7)

以下是部分更新一个文档的步骤：

1. 客户端向 `Node 1` 发送更新请求。
1. 它将请求转发到主分片所在的 `Node 3` 。
1. Node 3 从主分片检索文档，修改 `_source` 字段中的 `JSON` ，并且尝试重新索引主分片的文档。 如果文档已经被另一个进程修改，它会重试步骤 3 ，超过 `retry_on_conflict` 次后放弃。
1. 如果 `Node 3` 成功地更新文档，它将新版本的文档并行转发到 `Node 1` 和 `Node 2` 上的副本分片，重新建立索引。 一旦所有副本分片都返回成功， `Node 3` 向协调节点也返回成功，协调节点向客户端返回成功。

`update` API 还接受在 新建、索引和删除文档 章节中介绍的 `routing` 、 `replication` 、 `consistency` 和 `timeout` 参数。

> 当主分片把更改转发到副本分片时， 它不会转发更新请求。 相反，它转发完整文档的新版本。请记住，这些更改将会异步转发到副本分片，并且不能保证它们以发送它们相同的顺序到达。 如果Elasticsearch仅转发更改请求，则可能以错误的顺序应用更改，导致得到损坏的文档。

##### 2.2.5 多文档操作
将多个请求合并成一个，避免单独处理每个请求花费的网络延时和开销。 如果你需要从 Elasticsearch 检索很多文档，那么使用 `multi-get` 或者 `mget` API 来将这些检索请求放在一个请求中，将比逐个文档请求更快地检索到全部文档。

`mget` API 要求有一个 `docs` 数组作为参数，每个元素包含需要检索文档的元数据， 包括 `_index` 、 `_type` 和  `_id` 。如果你想检索一个或者多个特定的字段，那么你可以通过 `_source` 参数来指定这些字段的名字：
```
#查询多个文档
GET /_mget
{
   "docs" : [
      {
         "_index" : "website",
         "_type" :  "blog",
         "_id" :    2
      },
      {
         "_index" : "website",
         "_type" :  "pageviews",
         "_id" :    1,
         "_source": "views" #指定查询字段
      }
   ]
}

#
GET /website/blog/_mget
{
   "docs" : [
      { "_id" : 2 },
      { "_type" : "pageviews", "_id" :   1 }
   ]
}

#
GET /website/blog/_mget
{
   "ids" : [ "2", "1" ]
}
```
单个文档的检索是异步执行的，相互之间不会有影响。

![获取多文档](https://note.youdao.com/yws/api/personal/file/8D769E5874344107A60A740E11852523?method=getImage&version=7154&cstk=kixc2ey7)

以下是使用单个 `mget` 请求取回多个文档所需的步骤顺序：
1. 客户端向 `Node 1` 发送 `mget` 请求。
2. `Node 1` 为每个分片构建多文档获取请求，然后并行转发这些请求到托管在每个所需的主分片或者副本分片的节点上。一旦收到所有答复， `Node 1` 构建响应并将其返回给客户端。

可以对 docs 数组中每个文档设置 `routing` 参数。

##### 2.2.6 多文档创建、索引、删除和更新

`mget` 可以使我们一次取回多个文档同样的方式， `bulk` API 允许在单个步骤中进行多次 `create` 、 `index` 、 `update` 或 `delete` 请求。 如果你需要索引一个数据流比如日志事件，它可以排队和索引数百或数千批次。

bulk 与其他的请求体格式稍有不同，如下所示：
```
{ action: { metadata }}\n
{ request body        }\n
{ action: { metadata }}\n
{ request body        }\n
...
```
一个完整的 bulk 请求：
```
POST /_bulk
{ "delete": { "_index": "website", "_type": "blog", "_id": "123" }} 
{ "create": { "_index": "website", "_type": "blog", "_id": "123" }}
{ "title":    "My first blog post" }
{ "index":  { "_index": "website", "_type": "blog" }}
{ "title":    "My second blog post" }
{ "update": { "_index": "website", "_type": "blog", "_id": "123", "_retry_on_conflict" : 3} }
{ "doc" : {"title" : "My updated blog post"} } 
```
每个子请求都是独立执行，因此某个子请求的失败不会对其他子请求的成功与否造成影响。 

`mget` 和 `bulk` API 的模式类似于单文档模式。区别在于协调节点知道每个文档存在于哪个分片中。 它将整个多文档请求分解成 每个分片 的多文档请求，并且将这些请求并行转发到每个参与节点。

协调节点一旦收到来自每个节点的应答，就将每个节点的响应收集整理成单个响应，返回给客户端。

`bulk` API，允许在单个批量请求中执行多个创建、索引、删除和更新请求，如下图所示：

![使用 bulk 修改多个文档](https://note.youdao.com/yws/api/personal/file/019587FBADCB4224812553F474652AB1?method=getImage&version=7158&cstk=kixc2ey7)

bulk API 按如下步骤顺序执行：

1. 客户端向 Node 1 发送 bulk 请求。
2. Node 1 为每个节点创建一个批量请求，并将这些请求并行转发到每个包含主分片的节点主机。
3. 主分片一个接一个按顺序执行每个操作。当每个操作成功时，主分片并行转发新文档（或删除）到副本分片，然后执行下一个操作。 一旦所有的副本分片报告所有操作成功，该节点将向协调节点报告成功，协调节点将这些响应收集整理并返回给客户端。

bulk API 还可以在整个批量请求的最顶层使用 consistency 参数，以及在每个请求中的元数据中使用 routing 参数。


>  "为什么 bulk API 需要有换行符的有趣格式，而不是发送包装在 JSON 数组中的请求，例如 mget API？"

 在批量请求中引用的每个文档可能属于不同的主分片， 每个文档可能被分配给集群中的任何节点。这意味着批量请求 bulk 中的每个 操作 都需要被转发到正确节点上的正确分片。

 如果单个请求被包装在 JSON 数组中，那就意味着我们需要执行以下操作：

1. 将 JSON 解析为数组（包括文档数据，可以非常大）
1. 查看每个请求以确定应该去哪个分片
1. 为每个分片创建一个请求数组
1. 将这些数组序列化为内部传输格式
1. 将请求发送到每个分片

这是可行的，但需要大量的 RAM 来存储原本相同的数据的副本，并将创建更多的数据结构，Java虚拟机（JVM）将不得不花费时间进行垃圾回收。

相反，Elasticsearch可以直接读取被网络缓冲区接收的原始数据。 它使用换行符字符来识别和解析小的  action/metadata 行来决定哪个分片应该处理每个请求。

这些原始请求会被直接转发到正确的分片。没有冗余的数据复制，没有浪费的数据结构。整个请求尽可能在最小的内存中处理。

## Elasticsearch 搜索

 Elasticsearch 真正强大之处在于可以从无规律的数据中找出有意义的信息——从“大数据”到“大信息”。

 搜索（search） 可以做到：

- 在类似于 gender 或者 age 这样的字段上使用结构化查询，join_date 这样的字段上使用排序，就像SQL的结构化查询一样。
- 全文检索，找出所有匹配关键字的文档并按照_相关性（relevance）_ 排序后返回结果。
- 以上二者兼而有之。

关键概念：

- 映射（Mapping）  
描述数据在每个字段内如何存储
- 分析（Analysis）  
全文是如何处理使之可以被搜索的
- 领域特定查询语言（Query DSL）  
Elasticsearch 中强大灵活的查询语言

### 空搜索
搜索API的最基础的形式是没有指定任何查询的空搜索，它简单地返回集群中所有索引下的所有文档：
```
GET /_search
```
返回的结果（为了界面简洁编辑过的）类似如下：
```
{
   "hits" : {
      "total" :       14,   #匹配到的文档总数
      "hits" : [    #hits 数组包含所查询结果的前十个文档。
        {
          "_index":   "us",
          "_type":    "tweet",
          "_id":      "7",
          "_score":   1,    #衡量了文档与查询的匹配程度,默认情况下，首先返回最相关的文档结果，即返回的文档是按照 _score 降序排列的，
          "_source": {
             "date":    "2014-09-17",
             "name":    "John Smith",
             "tweet":   "The Query DSL is really powerful and flexible",
             "user_id": 2
          }
       },
        ... 9 RESULTS REMOVED ...
      ],
      "max_score" :   1   #查询所匹配文档的 _score 的最大值
   },
   "took" :           4,    #执行整个搜索请求耗费了多少毫秒
   "_shards" : {    #查询中参与分片的总数和查询情况
      "failed" :      0,
      "successful" :  10,
      "total" :       10
   },
   "timed_out" :      false   #查询是否超时，默认情况下，搜索请求不会超时，可以自定义超时时间 GET /_search?timeout=10ms
}
```

### 多索引、多类型搜索
在一个或多个特殊的索引并且在一个或者多个特殊的类型中进行搜索，如下所示：

- /_search  
在所有的索引中搜索所有的类型
-  /gb/_search  
在 gb 索引中搜索所有的类型
- /gb,us/_search  
在 gb 和 us 索引中搜索所有的文档
- /g*,u*/_search  
在任何以 g 或者 u 开头的索引中搜索所有的类型
-  /gb/user/_search  
在 gb 索引中搜索 user 类型
- /gb,us/user,tweet/_search  
在 gb 和 us 索引中搜索 user 和 tweet 类型
- /_all/user,tweet/_search  
在所有的索引中搜索 user 和 tweet 类型

当然，可以在url后面加上 `pretty` 提高返回结果的可阅读性，如 `/gb/_search?pretty`

当在单一的索引下进行搜索的时候，Elasticsearch 转发请求到索引的每个分片中，可以是主分片也可以是副本分片，然后从每个分片中收集结果。多索引搜索恰好也是用相同的方式工作的—只是会涉及到更多的分片。

tip：搜索一个索引有五个主分片和搜索五个索引各有一个分片准确来所说是等价的。

### 分页
默认情况下`hits` 数组中只有前 10 个文档（有10个或以上的话），要在搜索中显示其余的文档，需要使用分页功能。

和 SQL 使用 `LIMIT` 关键字返回单个 `page` 结果的方法相同，Elasticsearch 接受 `from` 和 `size` 参数：

- size  
显示应该返回的结果数量，默认是 10
- from  
显示应该跳过的初始结果数量，默认是 0

如果每页展示 5 条结果，可以用下面方式请求得到 1 到 3 页的结果：
```
GET /_search?size=5   #第1页
GET /_search?size=5&from=5    #第2页
GET /_search?size=5&from=10   #第3页
```

### 轻量搜索
两种形式的搜索 API：
1. “轻量的” 查询字符串 版本  
使用 Get 请求，参数通过url传递

2. 请求体 版本  
使用 Post 请求，使用 JSON 格式和更丰富的查询表达式作为搜索语言

现介绍轻量搜索

查询字符串搜索非常适用于通过命令行做即席查询（用户自定义查询条件）。例如，查询在 `tweet` 类型中 `tweet` 字段包含 `elasticsearch` 单词的所有文档：
```
GET /_all/tweet/_search?q=tweet:elasticsearch
```
查询在 name 字段中包含 john 并且在 tweet 字段中包含 mary 的文档，实际的地址是这样子的：
```
GET /_search?q=%2Bname%3Ajohn+%2Btweet%3Amary   #在url编码中，%2B为“+”，%3A为“:”
```
\+ 前缀表示必须与查询条件匹配。类似地， - 前缀表示一定不与查询条件匹配。没有 + 或者 - 的所有其他条件都是可选的——匹配的越多，文档就越相关。

#### `_all` 字段

查询字段值中存在mary的文档：
```
GET /_search?q=mary
```
其实，当索引一个文档的时候，Elasticsearch 取出所有字段的值拼接成一个大的字符串，作为 `_all` 字段进行索引。相当于增加了一个名叫 `_all` 的额外字段，所以如果不指定字段名，将会匹配 `_all`字段，也即匹配所有字段。

例如，当索引这个文档时：
```
{
    "tweet":    "However did I manage before Elasticsearch?",
    "date":     "2014-09-14",
    "name":     "Mary Jones",
    "user_id":  1
}
```
这就好似增加了一个名叫 _all 的额外字段：
```
"_all": "However did I manage before Elasticsearch? 2014-09-14 Mary Jones 1"
```


当然，也可以设置 `_all` 字段无效。

#### 更复杂一点的查询
下面的查询针对 `tweents` 类型，并使用以下的条件：
- name 字段中包含 mary 或者 john
- date 值大于 2014-09-10
- _all 字段包含 aggregations 或者 geo
```
# GET /_all/tweents/_search?q=+name:(mary john) +date:>2014-09-10 +(aggregations geo)
GET /_all/tweents/_search?q=%2Bname%3A(mary+john)+%2Bdate%3A%3E2014-09-10+%2B(aggregations+geo)
```

Get查询虽然比较简洁轻量，但是可读性很差，难以扩展，不好维护，主要是用于开发测试和简单的查询，生产环境中更多地使用功能全面的 request body 查询API

## 分析和映射

### 精确值和全文
Elasticsearch 中的数据可以概括的分为两类：精确值和全文

精确值如日期、数字等数据，字符串也可以作为精确值。对于精确值来讲，Foo 和 foo 是不同的，2014 和 2014-09-15 也是不同的。

全文通常是指非结构化的数据，例如一个推文的内容或一封邮件的内容。

精确值很容易查询。结果是二进制的：要么匹配查询，要么不匹配。这种查询很容易用 SQL 表示：
```
WHERE name    = "John Smith"
  AND user_id = 2
  AND date    > "2014-09-15"
```
我们很少对全文类型的域做精确匹配。相反，我们希望在文本类型的域中搜索。不仅如此，我们还希望搜索能够理解我们的 意图 ：
- 搜索 `UK` ，会返回包含 `United Kindom` 的文档。
- 搜索 `jump` ，会匹配 `jumped` ， `jumps` ， `jumping` ，甚至是 `leap` 。
- 搜索 `johnny walker` 会匹配 `Johnnie Walker` ， `johnnie depp` 应该匹配 `Johnny Depp` 。
- `fox news hunting` 应该返回福克斯新闻（ Foxs News ）中关于狩猎的故事，同时， `fox hunting news` 应该返回关于猎狐的故事。

Elasticsearch 使用到排索引完成这类查询。

### 倒排索引
Elasticsearch 使用一种称为 倒排索引 的结构，它适用于快速的全文搜索。一个倒排索引由文档中所有不重复词的列表构成，对于其中每个词，有一个包含它的文档列表。

例如，假设我们有两个文档，每个文档的 content 域包含如下内容：
1. The quick brown fox jumped over the lazy dog
2. Quick brown foxes leap over lazy dogs in summer

为了创建倒排索引，我们首先将每个文档的 content 域拆分成单独的 词（我们称它为 词条 或 tokens ），创建一个包含所有不重复词条的排序列表，然后列出每个词条出现在哪个文档。结果如下所示：
```
Term      Doc_1  Doc_2  
-------------------------  
Quick   |       |  X 
The     |   X   |
brown   |   X   |  X
dog     |   X   |
dogs    |       |  X
fox     |   X   |
foxes   |       |  X
in      |       |  X
jumped  |   X   |
lazy    |   X   |  X
leap    |       |  X
over    |   X   |  X
quick   |   X   |
summer  |       |  X
the     |   X   |
------------------------
```
现在，如果我们想搜索 quick brown ，我们只需要查找包含每个词条的文档：
```
TermTerm      Doc_1  Doc_2
-------------------------
brown   |   X   |  X
quick   |   X   |
------------------------
Total   |   2   |  1     
-------------------------
brown   |   X   |  X
quick   |   X   |
------------------------
Total   |   2   |  1
```
两个文档都匹配，但是第一个文档比第二个匹配度更高。如果我们使用仅计算匹配词条数量的简单 相似性算法 ，那么，我们可以说，对于我们查询的相关性来讲，第一个文档比第二个文档更佳。

但是，我们目前的倒排索引有一些问题：
- Quick 和 quick 以独立的词条出现，然而用户可能认为它们是相同的词。
- fox 和 foxes 非常相似, 就像 dog 和 dogs ；他们有相同的词根。
- jumped 和 leap, 尽管没有相同的词根，但他们的意思很相近。他们是同义词。

我们的用户可以合理的期望两个文档与查询匹配。我们可以做的更好。

如果我们将词条规范为标准模式，那么我们可以找到与用户搜索的词条不完全一致，但具有足够相关性的文档。例如：

- Quick 可以小写化为 quick 。
- foxes 可以 词干提取 --变为词根的格式-- 为 fox 。类似的， dogs 可以为提取为 dog 。
- jumped 和 leap 是同义词，可以索引为相同的单词 jump 。

现在索引看上去像这样：
```
Term      Doc_1  Doc_2
-------------------------
brown   |   X   |  X
dog     |   X   |  X
fox     |   X   |  X
in      |       |  X
jump    |   X   |  X
lazy    |   X   |  X
over    |   X   |  X
quick   |   X   |  X
summer  |       |  X
the     |   X   |  X
------------------------
```
这还远远不够。我们搜索 +Quick +fox 仍然 会失败，因为在我们的索引中，已经没有 Quick 了。但是，如果我们对搜索的字符串使用与 content 域相同的标准化规则，会变成查询 +quick +fox ，这样两个文档都会匹配！

分词和标准化的过程称为 分析。
### 分析
分析是决定文档如何被搜索到的方式。

分析 包含下面的过程：
- 首先，将一块文本分成适合于倒排索引的独立的 词条 ，
- 之后，将这些词条统一化为标准格式以提高它们的“可搜索性”，或者 recall

分析器执行上面的工作。 分析器 实际上是将三个功能封装到了一个包里：

1. 字符过滤器  
首先，字符串按顺序通过每个 字符过滤器 。他们的任务是在分词前整理字符串。一个字符过滤器可以用来去掉HTML，或者将 & 转化成 and。
2. 分词器  
其次，字符串被 分词器 分为单个的词条。一个简单的分词器遇到空格和标点的时候，可能会将文本拆分成词条。
3. Token 过滤器  
最后，词条按顺序通过每个 token 过滤器 。这个过程可能会改变词条（例如，小写化 Quick ），删除词条（例如， 像 a， and， the 等无用词），或者增加词条（例如，像 jump 和 leap 这种同义词）。

Elasticsearch提供了开箱即用的字符过滤器、分词器和token 过滤器。 这些可以组合起来形成自定义的分析器以用于不同的目的。

#### 内置分析器
Elasticsearch 内置了常用的分析器。用下面字符串举例：

`"Set the shape to semi-transparent by calling set_trans(5)"`

使用不同的分析器将会得到不同的结果：

##### 1. 标准分析器
标准分析器是Elasticsearch默认使用的分析器。它是分析各种语言文本最常用的选择。它根据 Unicode 联盟 定义的 单词边界 划分文本。删除绝大部分标点。最后，将词条小写。它会产生：
```
set, the, shape, to, semi, transparent, by, calling, set_trans, 5
```
##### 2. 简单分析器
简单分析器在任何不是字母的地方分隔文本，将词条小写。它会产生：
```
set, the, shape, to, semi, transparent, by, calling, set, trans
```

##### 3. 空格分析器
空格分析器在空格的地方划分文本。它会产生：
```
Set, the, shape, to, semi-transparent, by, calling, set_trans(5)
```
##### 4. 语言分析器
特定语言分析器可用于 很多语言。它们可以考虑指定语言的特点。例如， 英语 分析器附带了一组英语无用词（常用单词，例如 and 或者 the ，它们对相关性没有多少影响），它们会被删除。 由于理解英语语法的规则，这个分词器可以提取英语单词的 词干 。

英语 分词器会产生下面的词条：
```
# transparent、 calling 和 set_trans 已经变为词根格式。
set, shape, semi, transpar, call, set_tran, 5
```
#### 测试分析器
有些时候很难理解分词的过程和实际被存储到索引中的词条，特别是你刚接触Elasticsearch。为了理解发生了什么，你可以使用 analyze API 来看文本是如何被分析的。在消息体里，指定分析器和要分析的文本：
```
GET /_analyze
{
  "analyzer": "standard",
  "text": "Text to analyze"
}
```
结果中每个元素代表一个单独的词条：
```
{
   "tokens": [
      {
         "token":        "text",    #实际存储到索引中的词条
         "start_offset": 0,     #指明字符在原始字符串中的开始位置
         "end_offset":   4,     #指明字符在原始字符串中的结束位置
         "type":         "<ALPHANUM>",
         "position":     1      #指明词条在原始文本中出现的位置
      },
      {
         "token":        "to",
         "start_offset": 5,
         "end_offset":   7,
         "type":         "<ALPHANUM>",
         "position":     2
      },
      {
         "token":        "analyze",
         "start_offset": 8,
         "end_offset":   15,
         "type":         "<ALPHANUM>",
         "position":     3
      }
   ]
}
```

可以在在映射中指定分析器。

### 映射（Mapping）
映射定义了文档结构，类似与关系数据库中的表结构概念。

在 Elasticsearch 中，索引中每个文档都有 **类型** 。每种类型都有它自己的 **映射**。映射定义了类型中的域，每个域的数据类型，以及Elasticsearch如何处理这些域。映射也用于配置与类型有关的元数据。

注：“域”指的是数据类型、属性，比如时间域、数字域、字符串域

#### 核心简单域类型
Elasticsearch 支持如下简单域类型：
- 字符串: string
- 整数 : byte, short, integer, long
- 浮点数: float, double
- 布尔型: boolean
- 日期: date

索引（创建）一个包含新域的文档—之前未曾出现-- Elasticsearch 会使用 动态映射 ，通过JSON中基本数据类型，尝试猜测域类型，使用如下规则：

| JSON type                    | 域 type |
| ---------------------------- | ------- |
| 布尔型: true 或者 false      | boolean |
| 整数: 123                    | long    |
| 浮点数: 123.45               | double  |
| 字符串，有效日期: 2014-09-15 | date    |
| 字符串: foo bar              | string  |

> 这意味着如果你通过引号( "123" )索引一个数字，它会被映射为 string 类型，而不是 long 。但是，如果这个域已经映射为 long ，那么 Elasticsearch 会尝试将这个字符串转化为 long ，如果无法转化，则抛出一个异常。

#### 查看映射
通过 `/_mapping` ，我们可以查看 Elasticsearch 在一个或多个索引中的一个或多个类型的映射。比如获取索引 `gb` 中类型 `tweet` 的映射：
```
GET /gb/_mapping/tweet
```
Elasticsearch 根据我们索引的文档，为域(称为 属性 )动态生成的映射:
```
{
   "gb": {
      "mappings": {
         "tweet": {
            "properties": {
               "date": {
                  "type": "date",
                  "format": "strict_date_optional_time||epoch_millis"
               },
               "name": {
                  "type": "string"
               },
               "tweet": {
                  "type": "string"
               },
               "user_id": {
                  "type": "long"
               }
            }
         }
      }
   }
}
```
#### 自定义域映射
尽管在很多情况下基本域数据类型已经够用，但你经常需要为单独域自定义映射，特别是字符串域。自定义映射允许你执行下面的操作：
- 全文字符串域和精确值字符串域的区别
- 使用特定语言分析器
- 优化域以适应部分匹配
- 指定自定义数据格式
- 更多

域最重要的属性是 `type` 。对于不是 `string` 的域，一般只需要设置 `type` ：
```
{
    "number_of_clicks": {
        "type": "integer"
    }
}
```

默认， `string` 类型域会被认为包含全文。就是说，它们的值在索引前，会通过一个分析器，针对于这个域的查询在搜索前也会经过一个分析器。

`string` 域映射的两个最重要属性是 `index` 和 `analyzer` 。

##### index

index 属性控制怎样索引字符串。它可以是下面三个值：  
    1. analyzed  
    首先分析字符串，然后索引它。换句话说，以全文索引这个域。
    2. not_analyzed  
    索引这个域，所以它能够被搜索，但索引的是精确值。不会对它进行分析。
    3. no  
    不索引这个域。这个域不会被搜索到。

`string` 域 `index` 属性默认是 `analyzed` 。如果我们想映射这个字段为一个精确值，我们需要设置它为 `not_analyzed` ：
```
{
    "tag": {
        "type":     "string",
        "index":    "not_analyzed"
    }
}
```


其他简单类型（例如 long ， double ， date 等）也接受 `index` 参数，但有意义的值只有 `no` 和 `not_analyzed` ， 因为它们永远不会被分析，总是使用精确匹配。

##### analyzer
对于 `analyzed` 字符串域，用 `analyzer` 属性指定在搜索和索引时使用的分析器。默认， Elasticsearch 使用 `standard` 分析器， 但你可以指定一个内置的分析器替代它，例如 `whitespace` 、 `simple` 和 `english`，当然也可以自定义分析器。
```
{
    "tweet": {
        "type":     "string",
        "index":     "analyzed",
        "analyzer":    "english"
    }
}
```

#### 更新映射
首次创建一个索引的时候，可以指定类型的映射。也可以使用 `_mapping` 为新类型增加映射或者为已存在的类型更新映射。

我们可以更新一个映射来添加一个新域，但不能将一个存在的域从 analyzed 改为 not_analyzed 。

创建一个新索引，指定 tweet 域使用 english 分析器：
```
PUT /gb 
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "string",
          "analyzer": "english"
        },
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "string"
        },
        "user_id" : {
          "type" :   "long"
        }
      }
    }
  }
}
```
更新这个索引的类型的映射，`tweet` 映射增加一个新的名为 `tag` 的 `not_analyzed` 的文本域，使用 `_mapping` ：
```
PUT /gb/_mapping/tweet
{
  "properties" : {
    "tag" : {
      "type" :    "string",
      "index":    "not_analyzed"
    }
  }
}
```
不能修改和删除映射已存在域，只能新增域。

#### 测试映射
使用 analyze API 测试字符串域的映射：
```
GET /gb/_analyze
{
  "field": "name",
  "text": "Black-cats" 
}

GET /gb/_analyze
{
  "field": "tag",
  "text": "Black-cats" 
}
```
`name` 域产生两个词条 `black` 和 `cat`（分词） ， `tag` 域产生单独的词条 `Black-cats` （不分词）。换句话说，我们的映射正常工作。