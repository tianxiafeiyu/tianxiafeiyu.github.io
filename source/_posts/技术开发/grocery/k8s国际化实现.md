---
title: k8s国际化实现
date: 2022-12-15 23:40:42
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - k8s国际化实现
---
k8s用的是 github.com/gosexy/gettext/go-xgettext 翻译库

项目中提供shell脚本，通过翻译库自带的 go-xgettext 工具进行词条扫描，生成template.po文件

不支持增量扫描