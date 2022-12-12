转载自 https://www.jianshu.com/p/6e8381c9b01d

#### 一、什么是REST

一句话来概括RESTful API(具有REST风格的API): 用URL定位资源，用HTTP动词（GET,HEAD,POST,PUT,PATCH,DELETE）描述操作，用响应状态码表示操作结果。

REST是一种软件架构风格，或者说是一种规范，其强调HTTP应当以资源为中心，并且规范了URI的风格；规范了HTTP请求动作（GET/PUT/POST/DELETE/HEAD/OPTIONS）的使用，具有对应的语义。 核心概念包括：

#### 资源（Resource）：

在REST中，资源可以简单的理解为URI，表示一个网络实体。比如，/users/1/name，对应id=1的用户的属性name。既然资源是URI，就会具有以下特征：名词，代表一个资源；它对应唯一的一个资源，是资源的地址。

#### 表现（Representation）：

资源呈现出来的形式，比如上述URI返回的HTML或JSON，包括HTTP Header等；  REST是一个无状态的架构模式，因为在任何时候都可以由客户端发出请求到服务端，最终返回自己想要的数据，当前请求不会受到上次请求的影响。也就是说，服务端将内部资源发布REST服务，客户端通过URL来定位这些资源并通过HTTP协议来访问它们。