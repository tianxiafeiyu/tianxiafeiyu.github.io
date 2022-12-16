---
title: git 笔记
date: 2022-12-15 23:11:56
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - git 笔记
---
### 删除本地文件后从远程仓库获取问题

在本地删除文件后，`git pull`从远程仓库获取，但是一直提示 `up-to-date`，无法获取被删除的文件。

原因：当前本地库处于另一个分支中，需将本分支发Head重置至master。

将本分支发Head重置至master:

```
$ git checkout master 
$ git reset --hard
```

强行pull并覆盖本地文件

```
$ git fetch --all  
$ git reset --hard origin/master 
$ git pull
```