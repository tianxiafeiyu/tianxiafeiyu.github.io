---
title: 使用Fillder抓包安卓APP
date: 2023-6-15 12:00:00
updated: 2023-6-15 12:00:00
toc: true
tags: 
    - 使用Fillder抓包安卓APP
---
## fiddler 简介
Fiddler是一个http协议调试代理工具，它能够记录并检查所有你的电脑和互联网之间的http通讯，设置断点，查看所有的“进出”Fiddler的数据（指cookie,html,js,css等文件）。 Fiddler 要比其他的网络调试器要更加简单，因为它不仅仅暴露http通讯还提供了一个用户友好的格式。

## windows 端 fiddler 配置
1. 允许https和远程连接
2. 设置代理端口
3. 获取本机ip地址

## 手机端 设置
1. wifi设置代理服务器，填写上面获取到的ip和设置的端口
2. 浏览器访问 http://ip:port
3. 下载证书
4. 设置里安装证书

到此，fiddler 就可以抓手机上的请求了

## fiddler 使用
1. 请求过滤
2. 格式化请求
3. 获取响应体


## 实战，jump游戏资讯抓包
