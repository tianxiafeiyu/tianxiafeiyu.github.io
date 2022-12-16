---
title: go项目标准布局
date: 2022-12-15 23:19:25
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - go项目标准布局
---
### 建议的目录

#### /cmd

项目主要的应用程序。

对于每个应用程序来说这个目录的名字应该和项目可执行文件的名字匹配（例如，/cmd/myapp）。

不要在这个目录中放太多的代码。如果目录中的代码可以被其他项目导入并使用，那么应该把他们放在/pkg目录。如果目录中的代码不可重用，或者不希望被他人使用，应该将代码放在/internal目录。显示的表明意图比较好！

通常来说，项目都应该拥有一个小的main函数，并在main函数中导入或者调用/internal和/pkg目录中的代码。

更多详情，请看/cmd目录中的例子。

#### /internal

私有的应用程序代码库。这些是不希望被其他人导入的代码。请注意：这种模式是Go编译器强制执行的。详细内容情况Go 1.4的release notes。再次注意，在项目的目录树中的任意位置都可以有internal目录，而不仅仅是在顶级目录中。

可以在内部代码包中添加一些额外的结构，来分隔共享和非共享的内部代码。这不是必选项（尤其是在小项目中），但是有一个直观的包用途是很棒的。应用程序实际的代码可以放在/internal/app目录（如，internal/app/myapp），而应用程序的共享代码放在/internal/pkg目录（如，internal/pkg/myprivlib）中。

#### /pkg

外部应用程序可以使用的库代码（如，/pkg/mypubliclib）。其他项目将会导入这些库来保证项目可以正常运行，所以在将代码放在这里前，一定要三思而行。请注意，internal目录是一个更好的选择来确保项目私有代码不会被其他人导入，因为这是Go强制执行的。使用/pkg目录来明确表示代码可以被其他人安全的导入仍然是一个好方式。Travis Jeffery撰写的关于 I’ll take pkg over internal 文章很好地概述了pkg和inernal目录以及何时使用它们。

当您的根目录包含大量非Go组件和目录时，这也是一种将Go代码分组到一个位置的方法，从而使运行各种Go工具更加容易。

点击查看/pkg就能看到那些使用这个布局模式的流行Go代码仓库。这是一种常见的布局模式，但未被普遍接受，并且Go社区中的某些人不推荐这样做。

如果项目确实很小并且嵌套的层次并不会带来多少价值（除非你就是想用它），那么就不要使用它。请仔细思考这种情况，当项目变得很大，并且根目录中包含的内容相当繁杂（尤其是有很多非Go的组件）。

#### /vendor

应用程序的依赖关系（通过手动或者使用喜欢的依赖管理工具，如新增的内置Go Modules特性）。执行go mod vendor命令将会在项目中创建/vendor目录，注意，如果使用的不是Go 1.14版本，在执行go build进行编译时，需要添加-mod=vendor命令行选项，因为它不是默认选项。

构建库文件时，不要提交应用程序依赖项。

请注意，从1.13开始，Go也启动了模块代理特性（使用https：//proxy.golang.org作为默认的模块代理服务器）。点击这里阅读有关它的更多信息，来了解它是否符合所需要求和约束。如果Go Module满足需要，那么就不需要vendor目录。

#### /api

OpenAPI/Swagger规范，JSON模式文件，协议定义文件。

更多样例查看/api目录。

#### /web

Web应用程序特定的组件：静态Web资源，服务器端模板和单页应用（Single-Page App，SPA）。

#### /configs

配置文件模板或默认配置。

将confd或者consul-template文件放在这里。

#### /init

系统初始化（systemd、upstart、sysv）和进程管理（runit、supervisord）配置。

#### /scripts

用于执行各种构建，安装，分析等操作的脚本。

这些脚本使根级别的Makefile变得更小更简单（例如 <https://github.com/hashicorp/terraform/blob/master/Makefile> ）。

更多样例查看/scripts。

#### /build

打包和持续集成。

将云（AMI），容器（Docker），操作系统（deb，rpm，pkg）软件包配置和脚本放在/build/package目录中。

将CI（travis、circle、drone）配置文件和就脚本放在build/ci目录中。请注意，有一些CI工具（如，travis CI）对于配置文件的位置有严格的要求。尝试将配置文件放在/build/ci目录，然后链接到CI工具想要的位置。

#### /deployments

IaaS，PaaS，系统和容器编排部署配置和模板（docker-compose，kubernetes/helm，mesos，terraform，bosh）。请注意，在某些存储库中（尤其是使用kubernetes部署的应用程序），该目录的名字是/deploy。

/test
外部测试应用程序和测试数据。随时根据需要构建/test目录。对于较大的项目，有一个数据子目录更好一些。例如，如果需要Go忽略目录中的内容，则可以使用/test/data或/test/testdata这样的目录名字。请注意，Go还将忽略以“.”或“\_”开头的目录或文件，因此可以更具灵活性的来命名测试数据目录。

更多样例查看/test。

#### /docs

设计和用户文档（除了godoc生成的文档）。

更多样例查看/docs。

#### /tools

此项目的支持工具。请注意，这些工具可以从/pkg和/internal目录导入代码。

更多样例查看/tools。

#### /examples

应用程序或公共库的示例。

更多样例查看/examples。

#### /third\_party

外部辅助工具，fork的代码和其他第三方工具（例如Swagger UI）。

#### /githooks

Git的钩子。

#### /assets

项目中使用的其他资源（图像，Logo等）。

#### /website

如果不使用Github pages，则在这里放置项目的网站数据。

更多样例查看/website。

### 不应该出现的目录

#### /src

有一些Go项目确实包含src文件夹，但通常只有在开发者是从Java（这是Java中一个通用的模式）转过来的情况下才会有。如果可以的话请不要使用这种Java模式。你肯定不希望你的Go代码和项目看起来像Java。

不要将项目级别的/src目录与Go用于其工作空间的/src目录混淆，就像How to Write Go Code中描述的那样。`$GOPATH环境变量指向当前的工作空间（默认情况下指向非Windows系统中的$`HOME/go）。此工作空间包括顶级/pkg，/bin和/src目录。实际的项目最终变成/src下的子目录，因此，如果项目中有/src目录，则项目路径将会变成：/some/path/to/workspace/src/your\_project/ src/your\_code.go。请注意，使用Go 1.11，可以将项目放在GOPATH之外，但这并不意味着使用此布局模式是个好主意。
