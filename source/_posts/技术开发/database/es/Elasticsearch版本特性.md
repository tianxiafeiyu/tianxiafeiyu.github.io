# elasticsearch 各版本特性

## 5.0

支持Lucene 6.x

Instant Aggregations，在Shard层面提供了Aggregation缓存

新增 Sliced Scroll类型，现在Scroll接口可以并发来进行数据遍历了。每个Scroll请求，可以分成多个Slice请求，可以理解为切片，各Slice独立并行，利用Scroll重建或者遍历要快很多倍。

新增了Profile API

同时支持search和aggregation的profile

有一个新的 Search After 机制，其实和 scroll 类似，也是游标的机制，它的原理是对文档按照多个字段进行排序，然后利用上一个结果的最后一个文档作为起始值，拿 size 个文档，一般我们建议使用 _uid 这个字段，它的值是唯一的 id

新增Shrink API

新增了Rollover API

新增Reindex

提供了第一个Java原生的REST客户端SDK 基于HTTP协议的客户端对Elasticsearch的依赖解耦，没有jar包冲突，提供了集群节点自动发现、日志处理、节点请求失败自动进行请求轮询，充分发挥Elasticsearch的高可用能力

新增Wait for refresh，提供了文档级别的Refresh

新增Ingest Node

新增Painless Scripting

新增Task Manager

新增Depreated logging

新增Cluster allocation explain API

新增 half_float 类型

新增 :Matrix Stats Aggregation

为索引写操作添加顺序号

引入新的字段类型 Text/Keyword 来替换 String

关于 Index Settings 现在，配置验证更加严格和保证原子性，如果其中一项失败，那个整个都会更新请求都会失败，不会一半成功一半失败。下面主要说两点： 1.设置可以重设会默认值，只需要设置为 null即可 2.获取设置接口新增参数include_defaults,可以直接返回所有设置和默认值

集群管理方面，新增Deleted Index Tombstones

Cluster state 的修改现在会和所有节点进行 ack 确认。

Shard 的一个副本如果失败了， Primary 标记失败的时候会和 Master 节点确认完毕再返回。

使用 UUID 来作为索引的物理的路径名，有很多好处，避免命名的冲突。

_timestamp 和 _ttl 已经移除，需要在 Ingest 或者程序端处理。

ES 可直接用 HDFS 来进行备份还原（ Snapshot/Restore ）了

Delete-by-query 和 Update-by-query 重新回到 core ，以前是插件，现在可以直接使用了，也是构建在 Reindex 机制之上。(es1.x版本是直接支持，在es2.x中提取为插件，5.x继续回归直接支持)

HTTP 请求默认支持压缩，当然 http 调用端需要在 header 信息里面传对应的支持信息。

创建索引不会再让集群变红了，不会因为这个卡死集群了。

默认使用 BM25 评分算法，效果更佳，之前是 TF/IDF。

快照 Snapshots 添加 UUID 解决冲突

限制索引请求大小，避免大量并发请求压垮 ES

限制单个请求的 shards 数量，默认 1000 个

移除 site plugins ，就是说 head 、 bigdesk 都不能直接装 es 里面了，不过可以部署独立站点（反正都是静态文件）或开发 kibana 插件

允许现有 parent 类型新增 child 类型

这个功能对于使用parent-child特性的人应该非常有用。

支持分号（；）来分割 url 参数，与符号（ & ）一样

## 6.0

无宕机升级 使之能够从 5 的最后一个版本滚动升级到 6 的最后一个版本，不需要集群的完整重启。无宕机在线升级，无缝滚动升级

跨多个 Elasticsearch 群集搜索 和以前一样，Elasticsearch 6.0 能够读取在 5.x 中创建的 Indices ，但不能读取在 2.x 中创建的 Indices 。不同的是，现在不必重新索引所有的旧 Indices ，你可以选择将其保留在 5.x 群集中，并使用跨群集搜索同时在 6.x 和 5.x 群集上进行搜索

迁移助手 Kibana X-Pack 插件提供了一个简单的用户界面，可帮助重新索引旧 Indices ，以及将 Kibana、Security 和 Watcher 索引升级到 6.0 。 群集检查助手在现有群集上运行一系列检查，以帮助在升级之前更正任何问题。 你还应该查阅弃用日志，以确保您没有使用 6.0 版中已删除的功能

使用序列号更快地重启和还原 6.0 版本中最大的一个新特性就是序列 ID，它允许基于操作的分片恢复。 以前，如果由于网络问题或节点重启而从集群断开连接的节点，则节点上的每个分区都必须通过将分段文件与主分片进行比较并复制任何不同的分段来重新同步。 这可能是一个漫长而昂贵的过程，甚至使节点的滚动重新启动非常缓慢。 使用序列 ID，每个分片将只能重放该分片中缺少的操作，使恢复过程更加高效

使用排序索引更快查询 通过索引排序，只要收集到足够的命中，搜索就可以终止。它对通常用作过滤器的低基数字段（例如 age, gender, is_published）进行排序时可以更高效的搜索，因为所有潜在的匹配文档都被分组在一起。

稀疏区域改进 以前，每个列中的每个字段都预留了一个存储空间。如果只有少数文档出现很多字段，则可能会导致磁盘空间的巨大浪费。现在，你付出你使用的东西。密集字段将使用与以前相同的空间量，但稀疏字段将显着减小。这不仅可以减少磁盘空间使用量，还可以减少合并时间并提高查询吞吐量，因为可以更好地利用文件系统缓存

## 7.x

集群连接变化：TransportClient被废弃 以至于，es7的java代码，只能使用restclient。然后，个人综合了一下，对于java编程，建议采用 High-level-rest-client 的方式操作ES集群

ES数据存储结构变化：去除了Type es6时，官方就提到了es7会删除type，并且es6时已经规定每一个index只能有一个type。在es7中使用默认的_doc作为type，官方说在8.x版本会彻底移除type。 api请求方式也发送变化，如获得某索引的某ID的文档：GET index/_doc/id其中index和id为具体的值

High-level REST client 改变 已删除接受Header参数的API方法；Cluster Health API默认为集群级别；

ES程序包默认打包jdk：以至于7.x版本的程序包大小突然边300MB+ 对比6.x发现，包大了200MB+， 正是JDK的大小

默认配置变化：默认节点名称为主机名，默认分片数改为1，不再是5。

查询相关性速度优化：Weak-AND算法 啥是weak-and算法？ 核心原理：取TOP N结果集，估算命中记录数。

简单来说，一般我们在计算文本相关性的时候，会通过倒排索引的方式进行查询，通过倒排索引已经要比全量遍历节约大量时间，但是有时候仍然很慢。 原因是很多时候我们其实只是想要top n个结果，一些结果明显较差的也进行了复杂的相关性计算， 而weak-and算法通过计算每个词的贡献上限来估计文档的相关性上限，从而建立一个阈值对倒排中的结果进行减枝，从而得到提速的效果。

间隔查询(Intervals queries)： 某些搜索用例（例如，法律和专利搜索）引入了查找单词或短语彼此相距一定距离的记录的需要。 Elasticsearch 7.0中的间隔查询引入了一种构建此类查询的全新方式，与之前的方法（跨度查询span queries）相比，使用和定义更加简单。

与跨度查询相比，间隔查询对边缘情况的适应性更强。

引入新的集群协调子系统 移除 minimum_master_nodes 参数，让 Elasticsearch 自己选择可以形成仲裁的节点。 典型的主节点选举现在只需要很短的时间就可以完成。 集群的伸缩变得更安全、更容易，并且可能造成丢失数据的系统配置选项更少了。

节点更清楚地记录它们的状态，有助于诊断为什么它们不能加入集群或为什么无法选举出主节点。

时间戳纳秒级支持，提升数据精度 加粗样式

不再内存溢出 新的 Circuit Breaker 在JVM 堆栈层面监测内存使用，Elasticsearch 比之前更加健壮。

设置indices.breaker.fielddata.limit的默认值已从JVM堆大小的60％降低到40％。



## ES7与旧版本的区别

#### 1. 关于 type（类型）

使用 kibana 开发工具查询时候，指定类型查询会出现下面的提示：

> Deprecation: [types removal] Specifying types in document get requests is deprecated, use the /{index}/_doc/{id} endpoint instead.

es6时，官方就提到了es7会删除type，并且es6时已经规定每一个index只能有一个type。在es7中使用默认的_doc作为type，官方说在8.x版本会彻底移除type。 api请求方式也发送变化，如获得某索引的某ID的文档：

```
GET index/_doc/id
```

其中index和id为具体的值

#### 2. 弃用 "string", 使用 "text" 域

指定映射的时候使用 String 的话将会报错：

```
No handler for type [string] declared on field xxx
```

使用 text 替代 string