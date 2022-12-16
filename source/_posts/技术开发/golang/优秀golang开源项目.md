---
title: 优秀golang开源项目
date: 2022-12-15 23:19:25
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 优秀golang开源项目
---
作者：茹姐
链接：https://www.zhihu.com/question/20801814/answer/685254356
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

根据go语言中文社区提供的资料，还有互联网企业架构设计中的常见组件分类， 共精心挑选了153个开源项目（项目不限于在github开源的项目）， 分成以下17个大类。项目初衷是帮助到那些想学习和借鉴优秀golang开源项目，和在互联网架构设计时期望快速寻找合适轮子的人。

# 监控系统
## grafana/grafana
Grafana是用于监控指标分析和图表展示的工具， 后端支持 Graphite, InfluxDB & Prometheus & Open-falcon等， 它是一个流行的监控组件， 目前在各大中小型公司中广泛应用。

## prometheus/prometheus
Prometheus 是开源的服务监控系统和时间序列数据库， 提供监控数据存储，展示，告警等功能。

## bosun-monitor/bosun
专业的跨平台开源系统监控项目，go语言编写，灵活的模板和表达式配合上各种collector可以监控任何应用或系统级的运行数据，比 zabbix更轻量级、更易入手和更适合定制。

## sourcegraph/checkup
一个分布式的无锁的站点健康状态检查工具。 支持检查http，tcp，dns等的状态 并可将结果保存在s3。 自带了一个美观的界面。

## rapidloop/rtoprtop
是一个简单的无代理的远程服务器监控工具，基于 SSH 连接进行工作。无需在被监控的服务器上安装任何软件。rtop 直接通过 SSH 连接到待监控服务器，然后执行命令来收集监控数据。rtop 每几秒钟就自动更新监控数据，类似其他 *top 命令。

## influxdata/kapacitor
Kapacitor 是一个开源框架，用来处理、监控和警告时间序列数据。

## open-falcon/of-release
OpenFalcon是一款小米开源的监控系统。功能：数据采集免配置：agent自发现、支持Plugin、主动推送模式; 容量水平扩展：生产环境每秒50万次数据收集、告警、存储、绘图，可持续水平扩展。告警策略自发现：Web界面、支持策略模板、模板继承和覆盖、多种告警方式、支持回调动作。告警设置人性化：支持最大告警次数、告警级别设置、告警恢复通知、告警暂停、不同时段不同阈值、支持维护周期，支持告警合并。历史数据高效查询：秒级返回上百个指标一年的历史数据。Dashboard人性化：多维度的数据展示，用户自定义Dashboard等功能。架构设计高可用：整个系统无核心单点，易运维，易部署。

## rach/pome
Pome 是 Postgres Metrics 的意思。Pome 是一个 PostgreSQL 的指标仪表器，用来跟踪你的数据库的健康状况。

## TalkingData/owl
OWL是TalkingData公司推出的一款开源分布式监控系统, 演示环境http://54.223.127.87/，登录账号密码demo/demo

## gy-games/smartping
SmartPing为一个各机器(点)间间互PING检测工具，支持互PING，单向PING，绘制拓扑及报警功能。 系统设计为无中心化原则，所有的数据均存储自身点中，默认数据循环保留1个月时间，由自身点的数据绘制 出PING包 的状态，由各其他点的数据绘制 进PING包 的状态，并API接口获取其他点数据绘制整体PING拓扑图，拓扑图中存在报警功能。

## pinggg/pingd
pingd 是世界上最简单的监控服务，使用 golang 编写。软件支持 IPv6，但是服务器不支持. pingd 允许同时 ping 上千个 IPs，在此期间还可以管理监控的主机。用户提供主机名或者 IP，还有用户邮箱地址，就可以使用 3 个生成 URLs 来开启，停止或者删除你的追踪。每当你的服务器停机或者后台在线都会发送通知，还包含控制 URLs。

## cloudinsight/cloudinsight-agent
提供可视化监控的saas平台cloudinsight开源的一个监控客户端。 Cloudinsight 探针可以收集它所在操作系统的各种指标，然后发送到 Cloudinsight 后端服务

## gravitational/satellite
用于监测kubernetes健康状态的一个工具／库。 其特点是：轻量级定期测试， 高可用性和弹性网络分区， 无单点故障， 以时间序列的格式存储监控数据。

## kovetskiy/zabbixctlZabbixctl
是采用Zabbix服务API的命令行工具，它提供了有效的方式去查询和处理trigger 状态、主机最新数据和用户组。

# 容器技术
## docker/docker
Docker是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）。几乎没有性能开销,可以很容易地在机器和数据中心中运行。最重要的是,他们不依赖于任何语言、框架或包装系统。

## coreos/rkt
Rocket （也叫 rkt）是 CoreOS 推出的一款容器引擎，和 Docker 类似，帮助开发者打包应用和依赖包到可移植容器中，简化搭环境等部署工作。Rocket 和 Docker 不同的地方在于，Rocket 没有 Docker 那些为企业用户提供的“友好功能”，比如云服务加速工具、集群系统等。反过来说，Rocket 想做的，是一个更纯粹的业界标准。

## vmware/harbor
容器应用的开发和运行离不开可靠的镜像管理。从安全和效率等方面考虑，部署在私有环境内的Registry是非常必要的。Project Harbor是由VMware公司中国团队为企业用户设计的Registry server开源项目，包括了权限管理(RBAC)、LDAP、审计、管理界面、自我注册、HA等企业必需的功能，同时针对中国用户的特点，设计镜像复制和中文支持等功能。

## shipyard/shipyard
Shipyard 是一个基于 Web 的 Docker 管理工具，支持多 host，可以把多个 Docker host 上的 containers 统一管理；可以查看 images，甚至 build images；并提供 RESTful API 等等。 Shipyard 要管理和控制 Docker host 的话需要先修改 Docker host 上的默认配置使其支持远程管理。

## zettio/weave
Weave 创建一个虚拟网络并连接到部署在多个主机上的 Docker 容器。

## coreos/clair
Clair 是一个容器漏洞分析服务。它提供一个能威胁容器漏洞的列表，并且在有新的容器漏洞发布出来后会发送通知给用户。

## alibaba/pouch
Pouch 是 Alibaba 公司开源的容器引擎技术，其主要功能包括基本的容器管理能力，安全稳定的强容器隔离能力，以及对应用无侵入性的富容器技术。

## weaveworks/scope
一个docker&kubernetes的管理，监控可视化工具， 可以看到容器间的拓扑关系和tcp通信。

## docker/swarmkit
SwarmKit 是Docker公司开源的Docker集群管理和容器编排工具，其主要功能包括节点发现、基于raft算法的一致性和任务调度等。

## emccode/rexray
REX-Ray 是一个 EMC {code} 团队领导的开源项目，为 Docker、Mesos 及其他容器运行环境提供持续的存储访问。其设计旨在囊括通用存储、虚拟化和云平台，提供高级的存储功能。

## docker/libnetwork
Libnetwork 提供一个原生 Go 实现的容器连接，是容器的网络。libnetwork 的目标是定义一个健壮的容器网络模型（Container Network Model），提供一个一致的编程接口和应用程序的网络抽象。

## cloud66/habitus
一个快速实现docker build 流程的工具， 支持复杂的docker build流程，实现多个dockerfile的build流程，典型应用如将需要静态编译的程序，如go， java这类程序在一个docker build编译好之后，得到的二进制包用到后续的build流程。

## vishvananda/wormhole
Wormhole 是一个能识别命名空间的由 Socket 激活的隧道代理。可以让你安全的连接在不同物理机器上的 Docker 容器。可以用来完成一些有趣的功能，例如连接运行在容器本机的服务或者在连接后创建按需的服务。

# PaaS工具
## kubernetes/kubernetes
Kubernetes 是来自 Google 云平台的开源容器集群管理系统。基于 Docker 构建一个容器的调度服务。该系统可以自动在一个容器集群中选择一个工作容器供使用。其核心概念是 Container Pod。tsuru/tsuru在 Tsuru 的 PaaS 服务下，你可以选择自己的编程语言，选择使用 SQL 或者 NoSQL 数据库，memcache、redis、等等许多服务，甚至与你可以使用 Git 版本控制工具来上传你应用。

## laincloud/lain
Lain 是一个基于 docker 的 PaaS 系统。其面向技术栈多样寻求高效运维方案的高速发展中的组织，devops 人力缺乏的 startup ，个人开发者。统一高效的开发工作流，降低应用运维复杂度；在 IaaS / 私有 IDC 裸机的基础上直接提供应用开发，集成，部署，运维的一揽子解决方案。

## ooyala/atlantis
Atlantis 是一款基于 Docker，使用 Go 编写，为 HTTP 应用准备的开源 PaaS。Atlantis 可以在路由请求中轻松的构建和部署应用到容器。Atlantis 在 Ooyala 的新应用中得到了很广泛的应用。

## weibocom/opendcp
OpenDCP是一个基于Docker的云资源管理与调度平台，集镜像仓库、多云支持、服务编排、服务发现等功能与一身，支持服务池的扩缩容，其技术体系源于微博用于支持节假日及热点峰值流量的弹性调度DCP系统。OpenDCP允许利用公有云服务器搭建起适应互联网应用的IT基础设施，并且将运维的工作量降到最低。

## mesos/cloudfoundry-mesos
Cloud Foundry-Mesos框架由华为与Mesosphere的工程师合作完成，能够为应用提供安全可靠的、可伸缩、可扩展的云端运行环境，并且应用能够 享用Cloud Foundry生态圈内各类丰富的服务资源。企业能够通过Cloud Foundry开发云应用，并通过Cloud Foundry-Mesos将应用部署到DCOS上，使应用能够与DCOS上安装的其他服务及应用框架共享资源，实现资源利用率最大化，能够大幅降低企业 数据中心运营成本。DCOS能够运行在虚拟和物理环境上，能够支持Linux（以及很快支持Windows），并可适用于私有云、公有云及混合云环境。

# 微服务
## istio/istio
Istio是由Google、IBM和Lyft开源的微服务管理、保护和监控框架。使用istio可以很简单的创建具有负载均衡、服务间认证、监控等功能的服务网络，而不需要对服务的代码进行任何修改。

## go-kit/kit
Go-kit 是一个 Go 语言的分布式开发包，用于开发微服务。

## uber/jaeger
Jaeger是Uber的分布式跟踪系统 ，基于google dapper的原理构建， 以Cassandra作为存储层

## micro/micro
Micro是一个专注于简化分布式系统开发的微服务生态系统。可插拔的插件化设计，提供强大的可插拔的架构来保证基础组件可以被灵活替换。

## eBay/fabio
fabio 是 ebay 团队用 golang 开发的一个快速、简单零配置能够让 consul 部署的应用快速支持 http(s) 的负载均衡路由器。这里有一篇中文文章http://dockone.io/article/1567介绍了如何用fabio＋consul实现服务发现，负载均衡，并阐述了原理， 最后还有demo程序

## goadesign/goa
Goa 是一款用 Go 用于构建微服务的框架，采用独特的设计优先的方法。

## NYTimes/gizmo
纽约时报开源的go微服务工具.提供如下特性:标准化配置和日志;可配置策略的状态监测端点;用于管理 pprof 端点和日志级别的配置;结构化日志，提供基本请求信息;端点的有用度量;优雅的停止服务; 定义期待和词汇的基本接口

## koding/kite
一个基于go语言的微服务框架, Kite是Koding公司内部的一个框架, 该框架提供服务发现，多种认证功能，服务端通过RPC进行通信，同时还提供了websocket的js库，方便浏览器于服务器间进行通信。afex/hystrix-go用来隔离远程系统调用， 第三方库调用 ，服务调用， 提供熔断机制，避免雪崩效应的库， Hystrix的go 版本。 注Hystrixs是Netflix开源的一个java库fagongzi/gatewayGateway是一个使用go实现的基于HTTP的API 网关。特性 ：API 聚合 ; 流控; 熔断; 负载均衡; 健康检查; 监控; 消息路由; 后端管理WebUI . 能做什么：规划更友好的URL给调用者。聚合多个API的结果返回给API调用者，利于移动端，后端可以实现原子接口。保护后端API服务不会被突发异常流量压垮。提供熔断机制，使得后端API Server具备自我恢复能力。借助消息路由能力，实现灰度发布，AB测试。goodrain/rainbond云帮是一款以应用为中心的开源PaaS，深度整合Kubernetes的容器管理和Service Mesh微服务架构最佳实践，满足支撑业务高速发展所需的敏捷开发、高效运维和精益管理需求sourcegraph/appdashgo版本的分布式应用跟踪系统， 基于google dapper的原理构建andot/hproseHprose 是高性能远程对象服务引擎（High Performance Remote Object Service Engine）的缩写 —— 微服务首选引擎。它是一个先进的轻量级的跨语言跨平台面向对象的高性能远程动态通讯中间件。它不仅简单易用，而且功能强大。你只需要稍许的时间去学习，就能用它轻松构建跨语言跨平台的分布式应用系统了。CI/CDdrone/droneDrone 是一个基于 Docker 的持续发布平台，使用 Go 语言开发caicloud/cycloneCyclone 是一个打造容器工作流的云原生持续集成持续发布平台，简单易用，使用 Go 语言开发，有详尽的中文文档数据库技术pingcap/tidbTiDB 是国内 PingCAP 团队开发的一个分布式 SQL 数据库。其灵感来自于 Google 的 F1, TiDB 支持包括传统 RDBMS 和 NoSQL 的特性。influxdata/influxdb一个可以水平扩展的时间序列数据库， 内建http api， 支持对数据打tag，灵活的查询策略和数据的实时查询，支持类sql语句进行查询cockroachdb/cockroachCockroachDB (蟑螂数据库）是一个可伸缩的、支持地理位置处理、支持事务处理的数据存储系统。CockroachDB 提供两种不同的的事务特性，包括快照隔离（snapshot isolation，简称SI）和顺序的快照隔离（SSI）语义，后者是默认的隔离级别。google/cayleyCayley 是 Google 的一个开源图(Graph)数据库，其灵感来自于 Freebase 和 Google 的 Knowledge Graph 背后的图数据库。dgraph-io/dgraphdgraph 是可扩展的，分布式的，低延迟图形数据库。DGraph 的目标是提供 Google 生产水平的规模和吞吐量，在超过TB的结构数据里，未用户提供足够低延迟的实时查询。DGraph 支持 GraphQL 作为查询语言，响应 JSON。wandoulabs/codisCodis 是一个分布式 Redis 解决方案, 对于上层的应用来说, 连接到 Codis Proxy 和连接原生的 Redis Server 没有明显的区别 (不支持的命令列表), 上层应用可以像使用单机的 Redis 一样使用, Codis 底层会处理请求的转发, 不停机的数据迁移等工作, 所有后边的一切事情, 对于前面的客户端来说是透明的, 可以简单的认为后边连接的是一个内存无限大的 Redis 服务.youtube/vitessoutube出品的开源分布式MySQL工具集Vitess，自动分片存储MySQL数据表，将单个SQL查询改写为分布式发送到多个MySQL Server上，支持行缓存（比MySQL本身缓存效率高），支持复制容错，已用于Youtube生产环境sosedoff/pgwebgweb 是一个采用 Go 语言开发的基于 Web 的 PostgreSQL 管理系统。flike/kingshard一个高性能的mysql中间件， 支持读写分离， 数据分片， 安全审计等功能olivere/elasticelastic是开源搜索引擎elasticsearch的golang客户端，API友好，支持绝大部分es的接口,支持的es版本全面，从1.x到最新的6.x全覆盖siddontang/ledisdbledisdb是一个参考ssdb，采用go实现，底层基于leveldb，类似redis的高性能nosql数据库，提供了kv，list，hash以及zset数据结构的支持。outbrain/orchestratorMySQL 复制拓扑可视化工具slicebit/qbqb是用来让使更容易使用数据库的go语言的数据库工具包。它受Python最喜欢的ORM SQLAlchemy的启发，既是一个ORM，也是一个查询生成器。它在表达api和查询构建东西的情形下是相当模块化的。mediocregopher/radix.v2radix.v2是redis官方推荐的客户端之一，相比于redigo,radix.v2特点是轻量、接口实现优雅、API友好chasex/redis-go-clusterredis-go-cluster 是基于 Redigo 实现的 Golang Redis 客户端。redis-go-cluster 可以在本地缓存 slot 信息，并且当集群修改的时候会自动更新。此客户端管理每个节点连接池，使用 goroutine 来尽可能的并发执行，达到了高效，低延迟。hidu/mysql-schema-syncmysql-schema-sync 是一款使用go开发的、跨平台的、绿色无依赖的 MySQL 表结构自动同步工具。用于将线上(其他环境)数据库结构变化同步到测试（本地）环境!goshawkdb/serverGoshawkDB 是一个采用 Go 语言开发支持多平台的分布式的对象存储服务，支持事务以及容错。GoshawkDB 的事务控制是在客户端完成的。GoshawkDB 服务器端使用 AGPL 许可，而 Go 语言客户端使用 Apache 许可证degdb/degdbDegDB 是分布式的经济图数据库。存储技术ipfs/go-ipfsIPFS 是分布式文件系统，寻求连接所有计算机设备的相同文件系统。在某些方面，这很类似于原始的 Web 目标，但是 IPFS 最终会更像单个比特流群交换的 git 对象。IPFS ＝ InterPlanetary File Systemchrislusf/seaweedfsSeaweedFS 是简单，高伸缩性的分布式文件系统，包含两部分：存储数十亿的文件；快速为文件服务。SeaweedFS 作为支持全 POSIX 文件系统语义替代，Seaweed-FS 选择仅实现 key-file 的映射，类似 "NoSQL"，也可以说是 "NoFS"。spf13/aferoAfero 是一个文件系统框架，提供一个简单、统一和通用的 API 和任何文件系统进行交互，作为抽象层还提供了界面、类型和方法。Afero 的界面十分简洁，设计简单，舍弃了不必要的构造函数和初始化方法。Afero 作为一个库还提供了一组可交互操作的后台文件系统，这样在与 Afero 协作时，还可以保留 os 和 ioutil 软件包的功能和好处。coreos/torusTorus是一种针对容器集群量身打造的存储系统，可以为通过Kubernetes编排和管理的容器集群提供可靠可扩展的存储。这是继etcd、rkt、flannel，以及CoreOS Linux之后CoreOS发布的另一个开源产品。emccode/rexrayREX-Ray 是一个 EMC {code} 团队领导的开源项目，为 Docker、Mesos 及其他容器运行环境提供持续的存储访问。其设计旨在囊括通用存储、虚拟化和云平台，提供高级的存储功能。Terry-Mao/bfsbfs 是使用 Go 编写的分布式文件系统（小文件存储）。gostor/gotgtGotgt 是使用 Go 编写的高性能、可扩展的 iSCSI target 服务。