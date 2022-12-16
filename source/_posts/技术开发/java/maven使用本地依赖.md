---
title: maven使用本地依赖
date: 2022-12-15 23:40:30
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - maven使用本地依赖
---
```xml
<dependency>
   <groupId>com.test</groupId>
   <artifactId>core</artifactId>
   <version>1.0</version>
   <scope>provided</scope>
   <systemPath>${project.basedir}/lib/jasperreports-html-component-6.5.0.jar</systemPath>
</dependency>
```