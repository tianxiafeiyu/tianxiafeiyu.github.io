---
title: spring boot + jasypt实现配置文件信息加密
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - spring boot + jasypt实现配置文件信息加密
---
配置文件敏感信息的加密，对于生产环境来说还是很有必要的。之前自己实现了一个粗糙的配置文件加密方案，详见[spring boot中代码修改配置文件](https://note.youdao.com/ynoteshare1/index.html?id=0d316c739a394177dd492a8ff4710257&type=note)。后面有老师傅提出了有更成熟通过的方案，jasypt，本次就来使用它。

1、添加Maven依赖

```
 <dependency>
            <groupId>com.github.ulisesbocchio</groupId>
            <artifactId>jasypt-spring-boot-starter</artifactId>
            <version>1.8</version>
 </dependency>
```

最新版本是2.1.1，但是只能spring-boot-2.x以上使用。因为我的程序中使用的是spring-boot-1.5.3,所以选择1.8版本。

2、编写加密脚本

下载jasypt-1.9.2.jar，添加依赖后，也可以从本地仓库中获取，如：LocalRepository\org\jasypt\jasypt\1.9.2

Windows脚本：

```
@echo off
cd /d %~dp0
cd ..
set /p user=请输入要加密的账户名称: 
java -cp lib/jasypt-1.9.2.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI input=%user% password=apusic.net algorithm=PBEWithMD5AndDES
set /p password=请输入要加密的密码: 
java -cp lib/jasypt-1.9.2.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI input=%password% password=apusic.net algorithm=PBEWithMD5AndDES
pause
```

Linux脚本：

```
#!/bin/sh

BASE_DIR=$(cd `dirname $0`; pwd)/..
cd $BASE_DIR

read -p "输入要加密的账户名称：" user
java -cp $BASE_DIR/lib/jasypt-1.9.2.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI input=$user password=apsuic.net algorithm=PBEWithMD5AndDES

read -p "输入要加密的账号密码：" password
java -cp $BASE_DIR/lib/jasypt-1.9.2.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI input=$password password=apsuic.net algorithm=PBEWithMD5AndDES
```

运行脚本，根据提示输入账号密码后可以获得加密串

3、使用加密字符串

程序入口（main）添加注解：@EnableConfigurationProperties

配置文件中如下格式填写加密串：

```
client.user=ENC(40+Fa4B+kj2wbOQHa+JuWQ==)
client.password=ENC(qX2Its/37OKPVUgxM38I7qgEhitVnuPV)
```

加密串用ENC()标注

填写加密key,即jasypt.encryptor.password，可以在注入到程序运行时变量中，也可以写在配置文件中，不推荐。

运行时变量方式：

```
java -jar lib/exporter-aas-v9-0.0.1-SNAPSHOT.jar --spring.config.location=conf/application.properties --jasypt.encryptor.password=apusic.net
```

配置文件方式：

```
asypt.encryptor.password=apusic.net
```

这样在程序运行时候jasypt就会先解析加密串，程序获取到的是解析后的账号密码。

完成