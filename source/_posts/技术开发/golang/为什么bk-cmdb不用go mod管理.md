---
title: 为什么bk-cmdb不用go mod管理
date: 2022-12-13 23:43:08
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 为什么bk-cmdb不用go mod管理
---
项目地址 https://github.com/Tencent/bk-cmdb

为什么不用官方推荐的 go mod 管理依赖呢？

bk-cmdb vendor下的一些依赖库都是有修改过的：

- vendor/go.mongodb.org/mongo-driver/mongo/session_exposer.go
```go
// CmdbPrepareCommitOrAbort set state to InProgress, so that we can commit with other
// operation directly. otherwise mongodriver will do a false commit
func CmdbPrepareCommitOrAbort(sess Session) {
	i, ok := sess.(*sessionImpl)
	if !ok {
		panic("the session is not type *sessionImpl")
	}

	i.clientSession.SetState(2)
	i.didCommitAfterStart=false
}

// CmdbContextWithSession set the session into context if context includes session info
func CmdbContextWithSession(ctx context.Context, sess Session) SessionContext {
	return contextWithSession(ctx, sess)
}
```
在mongo driver中添加了CmdbPrepareCommitOrAbort、 CmdbReloadSessio等方法

这些在官方库是没有的，如果切换 go mod,从官方源获取依赖，肯定是不行的

issue：https://github.com/Tencent/bk-cmdb/issues/4748

如果将修改后的官方库上传到github，应该可以解决go mod难切换的问题

会不会有版权问题？

所以，尽量不要修改官方库
