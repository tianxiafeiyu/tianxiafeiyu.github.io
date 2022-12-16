---
title: idea+maven+git 开发环境安装
date: 2022-12-15 23:12:09
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - idea+maven+git 开发环境安装
---
#### 1. jdk安装

网上下载jdk，运行安装程序

配置环境变量：

- 系统变量->新增->变量名：JAVA_HOME，变量值：java安装根目录
- path变量->新增 ->%JAVA_HOME%\bin

控制台输入`java -version`验证

#### 2. idea安装

百度搜索下载安装、破解，没啥好说的

#### 3. maven安装

http://maven.apache.org/download.cgi 下载二进制安装包，直接解压到磁盘

配置环境变量：

- 系统变量->新增->变量名：MAVEN_HOME，变量值：maven根目录
- path变量->新增 ->%MAVEN_HOME%\bin

控制台输入`mvn -v`验证

配置本地仓库和远程仓库：打开%MAVEN_HOME%\conf\settings.xml文件，编辑

- 本地仓库：解开localRepository标签注释，将地址改为要设置的本地仓库地址
- 远程仓库：在mirrors标签中添加子标签如下：

```
<mirror>      
  <id>nexus-aliyun</id>    
  <name>nexus-aliyun</name>  
  <url>http://maven.aliyun.com/nexus/content/groups/public</url>    
  <mirrorOf>central</mirrorOf>      
</mirror>  
```

#### 4. git安装

https://git-scm.com/downloads 下载安装程序，会有很多安装选项，可以一路选择默认选项，安装完成

安装过程会自动添加git环境变量，不再需要手动配置

控制台输入`git --version`验证

配置git 用户和邮箱:

```
git config --global user.name [github注册用户名]
git config --global user.email [github邮箱]
git config --global user.password [用户密码]
git config --list   查看当前配置
# 需要修改信息的话重新运行以上命令即可
```

常用命令：

- git init ：给项目添加仓库
- git add . ：添加项目下的所有文件到仓库中，也可以指定文件
- git commit -m [提交时的描述信息] ：提交时的附带信息
- git remote add origin [自己的仓库url地址] ：将本地的仓库关联到github的仓库，需要先在github上创建仓库
- git push -u origin master ：项目上传到github仓库中
- git clone [github仓库url地址] :克隆项目到当前目录下

#### 5. idea使用maven

File -> Settings -> Build, Execution, Deployment -> Build Tools -> Maven :

- Maven home directory -> 选择%MAVEN_HOME%
- User settings file -> 选择%MAVEN_HOME%\conf\settings
- Local repository -> 选择本地仓库

出现版本不兼容的bug:
idea version：2019.1.1
maven version：3.6.3
问题描述：pom文件导入依赖包时报错`No implementation for org.apache.maven.model.path.PathTranslator was bound`
解决办法：升级idea版本或者降低maven版本。

#### 6. idea使用git

从github仓库中下载项目到本地：

- settings -> 配置git.exe
- 首页选择check out from version control，登录github，输入账号密码，就可以选择要下载的仓库了

本地项目更新到gitbub仓库中：