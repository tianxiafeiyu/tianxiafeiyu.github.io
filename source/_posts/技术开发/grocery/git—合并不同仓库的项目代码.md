---
title: git—合并不同仓库的项目代码
date: 2022-12-15 23:37:48
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - git—合并不同仓库的项目代码
---
转载自 https://www.cnblogs.com/phpper/p/8391607.html

### git合并两个不同的仓库

目前开发是2个仓库，线上仓库online\_a（对应的branch分支为online）,测试环境online\_b（对应的branch分支为demo），测试环境需要时刻保持onine\_a上的最新稳定稳定代码同步过来。如何合并呢？特此记录下：
在测试仓库onine\_b 上执行：

1.  测试仓库添加远程生产仓库(切换到自己的测试仓库下执行以下命令，比如我的当期测试online\_b.git)



    git remote add online_a git@github.com:fantasy/online_a.git //将online_a作为远程仓库，添加到online_b中，设置别名为online_a(自定义，这里我是为了方便区分仓库名)

1.  从远程仓库下载，这时我们弄个新的



    $ git fetch online-a
    remote: Counting objects: 21744, done.
    remote: Compressing objects: 100% (7380/7380), done.
    remote: Total 21744 (delta 15332), reused 20415 (delta 14323)
    Receiving objects: 100% (21744/21744), 2.44 MiB | 214.00 KiB/s, done.
    Resolving deltas: 100% (15332/15332), completed with 201 local objects.
    From git@github.com:fantasy/online_a.git* [new branch]          demo              -> online-backend/demo
     * [new branch]          online            -> online-backend/online
     * [new tag]             demo-last-bad     -> demo-last-bad
     * [new tag]             demo-last-ok      -> demo-last-ok
     * [new tag]             v2.0-beta         -> v2.0-beta
     * [new tag]             v2.1-days         -> v2.1-days
     * [new tag]             v2.1-dist         -> v2.1-dist
     * [new tag]             v2.2-dist         -> v2.2-dist
     * [new tag]             v2.2-nosmartbid   -> v2.2-nosmartbid
     * [new tag]             v2.2demo          -> v2.2demo
     * [new tag]             v2.3-bad-smartbid -> v2.3-bad-smartbid
     * [new tag]             demo-no-score     -> demo-no-score
     * [new tag]             tmp-repay-v1      -> tmp-repay-v1
     * [new tag]             tmp-repay-v2      -> tmp-repay-v2
     * [new tag]             transfer-dep-last -> transfer-dep-last
     * [new tag]             transfer-dep-ok   -> transfer-dep-ok

3.将online\_a仓库抓去的online分支作为新分支checkout到本地，新分支名设定为online\_repo1

    $ git checkout -b online_repo1 online-a/online  //注意这里也是别名online_a
    Switched to a new branch 'online_repo1'
    Branch 'online_repo1' set up to track remote branch 'online' from 'online-a'.

4.切换回本地测试的online\_b的demo分支

    $ git checkout demo
    Switched to branch 'demo'
    Your branch is up to date with 'origin/demo'.

5.将online\_repo1合并入demo分支

    git merge online_repo1

6.解决冲突

    git add .
    git commit -m "合并"
    git push online_repo1 online_a:online //上传到远程库
    git checkout demo
    git merge online_repo1
    git branch -d online_repo1

### 总结

*   大致思路是伪造远程的repo1仓库为repo2的一个分支，然后合并进来；
*   若是文件有冲突、或要建立子目录，建议在repo1中先解决，再进行如上操作。

