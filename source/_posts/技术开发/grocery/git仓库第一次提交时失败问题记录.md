#### 问题：

1.  本地初始化 git 仓库，并且进行了 add 和 commit 操作。
2.  github 上新建 git 仓库。
3.  本地仓库添加了github上的git仓库作为远程仓库，起名origin。
    \$git remote add origin <https://github.com/>...
4.  本地仓库在想做同步远程仓库到本地为之后本地仓库推送到远程仓库做准备时报错：`fatal: refusing to merge unrelated histories`（拒绝合并不相关的历史）

#### 解决：

出现这个问题的最主要原因还是在于本地仓库和远程仓库实际上是独立的两个仓库。假如我之前是直接clone的方式在本地建立起远程github仓库的克隆本地仓库就不会有这问题了。

查阅了一下资料，发现可以在pull命令后紧接着使用--allow-unrelated-history选项来解决问题（该选项可以合并两个独立启动仓库的历史）。

命令：

    $git pull origin master --allow-unrelated-histories

以上是将远程仓库的文件拉取到本地仓库了。
紧接着将本地仓库的提交推送到远程github仓库上，使用的命令是：

    $ git push <远程主机名> <本地分支名>:<远程分支名>
    也就是
    $git push origin master:master
    提交成功。

#### 其实在github创建空的仓库时候，就已经功能给出仓库初始提交的提示，注意网页上的提示。
