#### Span

Span 是分布式追踪系统中一个非常重要的概念，可以理解为一次方法调用、一个程序块的调用、一次 RPC 调用或者数据库访问。

SkyWalking 将 Span 粗略分为两类：LocalSpan 和 RemoteSpan。

1. LocalSpan 代表一次普通的 Java 方法调用，与跨进程无关。
2. RemoteSpan 