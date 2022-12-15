## 问题描述
用户登录有时接口会报500的错误，"Network connection error occurred. Please try again later."

## 分析过程
查看接口的具体服务，没有相关的报错信息，应该是发生在网关层的报错。

不是必现的问题，一时也摸不着头脑

开始还安慰自己是环境问题，因为其他的环境确实没有反馈有这个问题

但是过了好几天，这个报错还时不时出现，看来是真的有问题了

好吧，只能硬着头皮排查了

排查问题三板斧：复现2问题，分析日志，定位问题

首先是怎么让报错必现，发现，在长时间不登录系统后，第一次登录时，批量下发的接口中，会有几个接口报这个错误

难道是并发问题？这才几个并发，直接否决

从apisix中抓取日志，发现接口的报错如下：
```
2022/09/01 19:09:27 [error] 44#44: *941885 [lua] init.lua:689: phase_func(): failed to acquire the lock: timeout, client: 172.23.12.158, server: _, request: "GET /aops/overview?sf_cloud_id=5719605851& HTTP/1.1", host: "10.113.2.101:4430", referrer: "https://10.113.2.101:4430/index.html" 
```
度娘了一把，在apisix github的issue倒是找到一个类似的问题，但是最后也没有具体的解决方法，而且问题和我这个也不太一样，放弃

难道要从apisix源码入手？这个我一开始是拒绝的，因为我完全不熟悉apisix，何况它还是用lua写的，难办

但是问题得解决啊，只能硬着头皮搞了。查看环境的apisix是2.11.0版本，github上下了对应版本的apisix源码，看了几篇apisix博客，看了一点lua语法，整呗

定位报错位置，是在请求一个缓存时，由于没有找到，使用 resty_lock 加锁，然后巴拉巴拉一堆看不懂，猜测应该是要写共享缓存，所以加锁了

度娘一下 resty_lock ，默认超时时间 5s，我看报错的接口，刚好都是5s左右超时的，看来问题就在这里了

为啥会超时呢？apisix一直都是这样用的，性能这么差的吗？问了几个人，无果，还得自己看

因为是缓存导致的超时，所以也找到了问题必现的方法，就是重启apisix，缓存会清空，这时候，登录用户一定有接口报这个错误

不知道lua该怎么调试，直接用原始的方法，打日志，把所有可能的流程和加锁、解锁的地方都加上标志打印 

触发报错，查看流程，确实是一个接口在获得锁后，长达8s时间后才释放锁，这8s时间都干了啥？而且前面有的接口加锁释放锁很快就结束了，为啥咧？

根据打印的信息和代码推断，这是在加载第三方插件，这里从缓存中拿的应该是插件实例，在没有缓存的时候，就要去实例化插件，不过这实例化过程居然要这么久，肯定有问题

又去看了一些apisix插件相关的资料，发现这一块是加载其他语言的扩展插件，目前平台使用的主要就是权限认证插件iam_policy，难怪有些接口可以通过，那些都是免认证的接口，不会去实例化认证插件。

又结合之前在日志中发现的插件报错
```
022/09/01 19:09:31 [warn] 50#50: *109 [lua] init.lua:753: 2022-09-01T19:09:31.253+0800	ERROR	common/util.go:33	failed to send http request, url: http://xaas-fees.bss:13003/v1/api-assets, err: Get "http://xaas-fees.bss:13003/v1/api-assets": dial tcp: lookup xaas-fees.bss on 10.43.0.10:53: server misbehaving 
mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/pkg/common.HttpRequest 
	/home/go/src/mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/pkg/common/util.go:33 
mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy.getServerRoute 
	/home/go/src/mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy/route.go:90 
mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy.GetServerRouteInfo 
	/home/go/src/mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy/route.go:52 
mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy.GetServersRouteInfo.func1 
	/home/go/src/mq.code.sangfor.org/CMP/SCC/Infrastructure/GW/sf-apisix-plugins/apisix-go-plugin-runner/cmd/go-runner/plugins/iam_policy/internal/policy/route.go:35 
```
之前还觉得不相关的，现在看来很特么相关，问题就在这里

查看 iam_policy 源码，在实例化插件的时候，向所有配置的服务都会调用一次请求，获取服务器的路由信息；这里配置了bss相关的路由，但是实际环境并没有运行bss服务，所以一定会超时失败（10s）,这就是为什么注册插件会花费10s之多！

删除配置中的bss相关路由，重新生成配置文件，重启apisix，相关报错不再出现。

完结撒花。
