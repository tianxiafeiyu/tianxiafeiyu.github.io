---
title: Jenkins遇到的坑
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Jenkins遇到的坑
---
1. 一开始是仓库没有jar包，编译报错，上传jar后仍然报错，确认信息填写正确。 报错：

   ```
   Failure to find com.github.sanjusoftware:yamlbeans:jar:1.11 in http://nexus.apusic.net/content/groups/public was cached in the local repository, resolution will not be reattempted until the update interval of nexus has elapsed or updates are forced
   ```

   由于之前编译有了缓存信息，后面再编译不会再从远程仓库拉取，需要删掉本地仓库缓存文件。