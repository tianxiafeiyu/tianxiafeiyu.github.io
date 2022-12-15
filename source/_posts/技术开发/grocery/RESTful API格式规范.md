## 1 RESTful风格

RESTful是一种API的设计风格，他和GraphQL ，JSON-RPC，WebService类似，用于定义在CS、BS架构下暴露服务端接口。此次设计对接规范，将使用RESTful作为标准。

### 1.1 特征

RESTful风格的特点是：

#### 1）URI资源化

即，URI代表的是资源，而不包含动作。比如，一个班级，有很多学生，我们可以这样表示：/class/students

#### 2）动作由HTTP头里的方法决定。

比如，我们想新增一个学生，我们可以用POST方法：

POST /class/students
{
"name": "Jake",
"age" : 18
}
我们想查看当前有哪些学生，可以用GET方法：

GET /class/students

我们想查看某学生的具体信息，可以用路径指定到某一个ID：

GET /class/students/1

我们想要开除id为1的学生，可以用DELETE方法：

DELETE /class/students/1

HTTP头里面的方法决定了动作后，后端实现也应该严格根据动作来，比如，GET请求不应该对数据造成任何更改，如此，我们对权限控制便非常方便，例如，如果是访客，我们可以只开放GET方法，而对于ADMIN，我们可以开放GET,POST,DELETE等方法。

大多数就是做CRUD，用HTTP头部动作，可以很好满足。

#### 3）资源的表现由Content-Type决定

HTTP请求的头信息中Accept和Content-Type字段，是对资源的表现描述。例如，指定是JSON格式，还是HTML格式。

#### 4）无状态

无状态是指客户端无状态，例如，你不应该在客户端使用类似的逻辑：

if (hasStudent("Jake")) {
getStudentInfo("Jake");
}
因为，hasStudent和getStudentInfo调用之间，可能别人已经将Jake删除了，你的状态维护不一定准确。 你可以直接getStudentInfo(“Jake”)，没有则返回失败即可。 服务端可以维护一些状态，但最好不要维护太多，例如，HTTP登录状态，是应该维护的，但是，记录并强制要求用户A是否请求过某个URL再请求另一个URL，这种设计就不应该了。

#### 5）数据安全

使用HTTPS协议，加密数据。

我们对接统一采用RESTful方式的HTTPS（为了加密）请求，内容为JSON格式，其中，安全、幂等性、无状态之类的约束，请产品线严格按照Restful规定设计。

### 1.2 优点

#### 1）减少沟通成本。

API是开放给别人使用的，由于有既有的约定，会让沟通成本大大减少，这是API提供者最应该考虑的。

#### 2）能够接纳多种客户端(适用于大多数CS BS架构程序)

不止是web程序，基本上的CS架构程序，都可以使用RESTful提供API，这样，不论是WEB Client还是Windows APP还是，Mobile APP，都可以轻松使用服务端的API。

由Facebook开放的GraphQL 等也可能在今后流行，不过当前主流的还是RESTful。

#### 3）思维方式转换为以资源为中心

传统的方式是以操作为中心，例如create\_user, query\_students。

类似于面向对象以对象为中心，RESTful推崇以资源为中心，说不上绝对好，但的确会引导大家考虑资源本身，关注内聚性，关注权限，关注资源间关联。

#### 4）扩展方便

无状态设计对横向扩展非常方便，因为API之间解耦比较好，资源解耦也比较好。 还有一个叫 hypertext-driven 的东西，类似于自描述，但是用起来也不方便，在CodeReview工具提供的API便是这种方式，优点是服务端可以随意更换URL，缺点是请求前要去查询一下该请求什么路径。例如github的参考<https://api.github.com/>

#### 5）建立在HTTP协议基础之上

HTTP协议里面规定的东西很多，例如，缓存，压缩，代理，加密，穿透，等等，都已经让HTTP帮忙完成了，给很多实现减负。

### 1.3 动作

#### GET

获取资源

幂等

举例：获取学生Jake的信息。

GET /class/students?name="Jake"

#### POST

创建资源，不会指定资源ID，但创建完成后，通常会返回资源的ID，这样后续可以通过资源ID操作此资源。

非幂等

举例：创建学生。
POST /class/students
{"name": "Jake", "age" : 18, "score": 0}

#### PUT

整体(Entire Resource)替换。为了定位资源，要求路径上有资源的唯一ID。

幂等

举例：替换ID为2的学生的信息为如下新信息。

PUT /class/students/2
{"name": "Jim","age": 19}

此操作将原本ID为2的学生的所有属性冲掉了，替换后，ID为2的学生整体内部数据结构变为：

{"id": 2, "name": "Jim","age": 19}

异常：

1.如果Playload为空，返回失败。

2.如果Playload为{}，是正确的，表示清空（重置），例如上述示例内部数据结构将变为：{"id": 2}

#### PATCH

部分(Part Resource)替换。

幂等

为了定位资源，要求路径上有资源的唯一ID。

举例：更新ID为2的学生的年龄从之前的18岁更新为20岁。
PATCH /class/students/2
{"age": 20}

这里，ID为2的学生的其他属性保留，整体内部数据结构变成：

{"id": 2, "name": "Jake", "age" : 20, "score": 0}

异常：

1.如果Playload为空或{}，返回失败。

2.对于嵌套的结构，如果是正常书写，表示整体替换；如果是点分结构，表示部分更新。比如：

{"id": 2, "name": "Jake", "age" : 20, "score": {"English": 86, "Chinese":88, "math":99}}

2.1子结构替换：

PATCH /class/students/2

{"score": {"math":100}}

替换后为：

{"id": 2, "name": "Jake", "age" : 20, "score": {"math":100}}

2.2 子结构更新：

PATCH /class/students/2

{"score.math": 100}

替换后为：

{"id": 2, "name": "Jake", "age" : 20, "score": {"English": 86, "Chinese":88, "math":100}}

3.对于数组，标准用法是表示整体替换，而不能增删。比如：

{"id": 2, "name":"Jake", "friends": \["Jim", "Marry", "Jake"]}

3.1 执行整体替换：

    PATCH /class/students/2

    {"friends": ["Bob"]}

    替换后为：

    {"id": 2, "name":"Jake", "friends": ["Bob"]}

3.2 扩展语法，为了支持增加和删除功能，参考rfc6902（我们修改一下使得一致性更好），我们在URL参数上，附带\_arrayop=\[add,remove]，用于表示增删数组，例如：

    PATCH /class/students/2?_arrayop=add

    {"friends": ["Bob"]}

    增加后为：

    {"id": 2, "name":"Jake", "friends": ["Jim", "Marry", "Jake", "Bob"]}

    PATCH /class/students/2?_arrayop=remove

    {"friends": ["Jim"]}

    删除后为：

    {"id": 2, "name":"Jake", "friends": ["Marry", "Jake"]}

    这种做法的缺陷是，一个_arrayop控制了整个Playload的array动作，所以，同一Playload如果需要多种动作的情况，请拆分为多次请求。

#### DELETE

删除资源。

幂等

DELETE里面能不能带payload，这个RFC 7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content"是这么规定的：

A payload within a DELETE request message has no defined semantics; sending a payload body on a DELETE request might cause some existing implementations to reject the request.

所以，并没有禁止，是否支持依赖于服务端实现，比如某些版本的Tomcat或 Jetty就会忽略payload。

而OpenAPI3.0定义里面描述为：

The request body applicable for this operation. The requestBody is only supported in HTTP methods where the HTTP 1.1 specification RFC7231 has explicitly defined semantics for request bodies. In other cases where the HTTP spec is vague, requestBody SHALL be ignored by consumers.

说明，对OpenAPI规范而言，这种模棱两可的描述，是明确要ignored的。

经过我们的实践，发现DELETE带payload需求很多，所以，我们明确一下，支持DELETE带payload的行为，假如遇到实现不支持时，请使用DELETE Over POST实现。

举例：

删除ID为2的学生。
DELETE /class/students/2

删除有Jim这个朋友的所有学生。

DELETE /class/students

{"friends": \["Jim"]}

或表达为DELETE Over POST：

POST /class/students?\_method=DELETE

{"friends": \["Jim"]}

#### HEAD

获取资源元信息。只有HTTP头，不包含数据。

幂等

举例：查看学生Jake是否存在。

HEAD /class/students?name="Jake"

#### OPTIONS

获取资源选项。例如获取服务端支持的方法子集，HTTP版本等。

幂等

举例：获取当前学生API是否支持POST方法。

OPTIONS /class/student

返回值中有Allow字段，标明支持的方法，Responses to this method are not cacheable.

#### TRACE

服务器端loop back消息。

幂等

对RESTful来说基本没用。

#### CONNECT

代理时使用

幂等

对RESTful来说基本没用。

在实际资源操作中，总会有一些不符合 CRUD（Create-Read-Update-Delete） 的情况，处理方法为使用POST加上endpoint, 比如 POST /mail/\:id/resend表示重发邮件，建议在资源的基础上加入动作endpoint。

如果参数里面带有\_method参数，那\_method参数将override掉HTTP协议头里面的动作，用于扩展某些难以支持HTTP头部修改的场景、某些关键字如DELETE无法附带正文内容的问题、某些类防火墙系统截拦PUT等关键字场景。

## 命名规范

### 2.1 关于URL中的横线和下划线

先说结论：URL中使用横线“-”或下划线“\_”各有利弊，本规范中即不使用横线也不使用下划线。

关于横线和下划线的讨论，如有兴趣可参见：关于URL里面使用下划线还是横线的理由.doc

### 2.2 URL命名规范

规范：全部使用小写字母，如果有多个单词，那么单词之间不需要使用任何分隔符（即不使用下划线，也不使用横线），直接将所有单词拼接在一起即可。

例如，即不使用user-name，也不使用user\_name，而是直接使用username。

URL命名规则可用正则描述：/^\[0-9a-z]+\$/

举例子：/api/v1/mailsetting/testemail

讨论：有人提出疑问“很多时候单词长度查不多时，不分隔一下估计都很难知道是那两个单词”，这个需要再收集一下大家的意见，看是否需要把规划放宽松一些。

### 2.3 变量命名规范——驼峰法（camel case）

变量是指URL查询参数（Query String）和请求体中json字段的名字。

规范：强制新代码使用驼峰法命名，大小写敏感。例如userName。不允许使用下划线或横线来连接单词。

目的：减少了下划线带来的字符长度增加，减少了纠结是使用下划线还是横线的情况，是很多种语言的默认风格（JAVA,C#,GO,SWIFT等新派语言代表）。

特殊场景：允许在变量开头加上一个下划线，用于防止和产品线的关键字冲突，例如：\_queryMethod 和 \_cache

变量命名规则可用正则描述：/^\_?\[a-z]\[0-9A-Za-z]\*\$/

举例子：/api/v1/mailsetting/testemail?userName=zhangsan&\_enableAuth=1&\_cache=false

POST json数据举例：{“userName”: "zhangsan", "\_enableAuth": 1, "\_cache": false}

最关键的设计约定是：所有命名尽可能使用单一名称涵盖你要表达的意义，不到万不得已，不要用多个词连接。

### 2.4 历史版本可选命名规则-蛇形法（snake case）

由于有的产品线，例如AD，内部一致使用下划线方式，对转换为驼峰法抗议较多，这里新增一种命名规则，适应这些产品线。

目前发现，使用下划线风格的部门，很难融入整体的驼峰风格，有的规范定义后，显得格格不入，总体规范不会为某个部门单独开一套风格的API。

对接无法保证对端是什么语言，比如是PYTHON、PHP、PERL、JAVASCRIPT，JAVA，GO，不要因为自己的语言习惯下划线而选择下滑线风格。大家不是历史原因万不得已，不要选择这种风格。

所有涉及的参数名称、JSON名称等，都遵循如下命名规范：

1）URL，大小写无感知，user name 使用横线连在一起，写成user-name。

/^\[0-9a-z]\[0-9-a-z]\*\[0-9a-z]\$/

2）变量，只能出现小写，user name写成user\_name。

/^\[\_a-z]\[\_0-9a-z]\*\$/

## URI格式

<https://host:port{/separatePath}/{product}/{version}/{resourceURI}>

例如：

<https://200.200.88.88:443/open/api/sip/v1/log/security>

<https://200.200.88.88:443/doc/acloud/v3/keystone>

<https://200.200.88.88:443/api/sangforinter/v1/>

#### 1）separatePath隔离路径

因为我们的产品，基本上没有域名，只提供IP访问，导致没办法做子域名，所以，一般的URI隔离，就用路径表示，我们将隔离路径表示为separatePath，其功能类似于子域名，上例中open/api就是separatePath。

对于支持域名的产品线（例如云脑），可以将separatePath和product移到子域名。

#### 2）product产品

每个部门，有自己不同的产品，例如vt的acloud，本规范主要是用于全公司产品之间互通，product名称叫sangforinter，此处也可以当成模块名称，比如appstore表示app应用商店模块。

#### 3）version版本号

每个产品可能会定义不同版本的规范，所有这里有版本号。

我们的sangforinter产品，当前版本号为v1。

关于版本号的位置，虽然HTTP头部的Accept: version=1.1里面可以指定version，但是，不太方便操作，不少设计是指定在路径上，例如 /v2/class/students。

#### 4）resourceURI

resourceURI为具体的资源URI，这里可以有resource的嵌套。

例如，用WordPress写文章，就会出现Posts和Comments的关系：

有人认为，Comments应该独立于Posts存在，类似：

GET /api/comments?postId=XXXX

GET /api/comments/\:commentsId

POST /api/comments

也有人认为，Comments是依赖于Posts的，类似：

GET/POST /api/posts/\:postId/comments

如果是后者，则出现了posts和comments两种资源的嵌套。

## 4 GET请求

GET相关文档请参考<https://www.w3.org/2001/tag/doc/get7>

#### 4.1 GET OVER POST

由于有的部门，GET请求参数过于复杂，或者GET请求要发送很长的URL列表，所以，我们建议，对于比较长（超过几百字符）或比较复杂（有嵌套OBJECT或ARRAY）的情况，使用GET OVER POST方式，即上面讲的，使用POST 发送请求，但是参数里面\_method=GET的方式。

#### 4.2 GET语义转变

从语义上，将GET请求资源的概念转换为POST新增一个请求资源的task，也是比较适合的一种转换方式，不需要GET OVER POST。

例如，获取几百条URL的风险状态，可以转换为，新增一个获取几百条URL的风险状态任务，异步情况下，服务器会返回一个任务ID，供下次查询，同步情况下，服务器直接返回数据TASK执行结果也是可以的。其示例如下。

原本：

GET /status/url?list=url1,url2,url3

语义转变后：

POST /status/url/task?\_method=GET

{

    [

        "url1",

        "url2",

        "url3"

    ]

}

#### 4.3 GET传统方式

如果不是上面说的，GET请求参数特别复杂的情况，建议使用传统方式。

1）请求参数的最大长度。

GET请求参数放在了URL里面，有最长限制，RFC7230也并没有强制规定，只是建议：

at a minimum, request-line lengths of 8000 octets.

目前看，2000字节以内才是安全长度，参考“What is the maximum length of a URL in different browsers?”

参考[What is the maximum length of a URL in different browsers?](https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers)

如果请求参数过长，服务器必须返回414 (Request-URI Too Long) HTTP状态码。

2）请求参数的风格

a) 多参数风格：

建议使用 /cars/?color=blue\&type=sedan\&doors=4。

不推荐使用/cars/color\:blue/type\:sedan/doors:4。

b) 数组表示风格：

建议使用/appointments?users=\[id1,id2]。

不推荐使用/appointments?users=id1,id2。虽然这种方式各位简洁，但是下面我们还要表示对象，需统一风格。

c) 对象表示风格：

建议使用/appointments?params={users:\[id1,id2], age:18}。

3）URL编码。

URL参数为key=value形式，key规定为驼峰命名的纯英文+数组+下划线组合，不能出现中文或其他特殊符号，正则规则为：/\[\_A-Za-z]\[0-9A-Za-z]\*/

value部分，由于不同的浏览器和html编码设置差异比较大，参见《关于URL编码》为了统一，我们以rfc3986 为标准（主要是中文必须是UTF-8编码而非其他编码）对value做encode。

JS里面对value做encode/decode的函数为：encodeURIComponent()/decodeURIComponent()

PHP里面对value做encode/decode的函数为（必须关闭magic\_quotes\_gpc）：rawurlencode()/rawurldecode()

## 5 批量处理接口

1）URI相同的操作，RESTFUL本身就支持BATCH操作，只需要将参数改为数组即可。

比如添加学生，添加一个学生为：

    POST /class/students

{"data":{"name":"Jake", "age":18}}

添加多个学生（批）为：

    POST /class/students

{"data":\[{"name":"Jake", "age":18},{"name":"Jakson", "age":19}]}

2）URI不同，可以写一个READ ONLY的BATCH接口，不涉及任何WRITE。

    某些产品线有这种需求，例如首页有很多URL GET请求，可以合并。

再例如，我们想要同时获取之前三个接口提供的统计信息，可以这样写：

POST /status/batch?\_method=GET
{
"items":
\[
{
"path":"status/cpu",
"param" :
{
"max" : 90
}
},
{
"path":"status/memory"
},
{
"path":"status/disk"
}
]
}

3）URI不同，不支持BATCH WRITE操作。

某些产品线有这类需求，但是不建议大家这么设计，原因是很难做到原子操作，会残留中间状态，而且错误处理比较麻烦，幂等性之类的RESTFUL标准也无法满足。

### 5.1 返回结果

子项的格式请参考“回复消息格式”小节。

批量处理，返回结果有三种方式，建议支持第三种返回结果。

1）返回整体错误描述。例如：

{
"code": 0,
"message": "success"
}
2）返回具体的每项错误描述（返回错误数组的顺序和发送时的数组顺序必须一一对应）。例如：

\[{
"code" : 0,
"message" : "success",
"data" : {
"id" : 1
}
}, {
"code" : 22,
"message" : "invalid param"
}
]
3） 返回整体错误描述加具体的每项错误描述（返回错误数组的顺序和发送时的数组顺序必须一一对应），全部成功返回0，部分失败或者全部失败返回错误码57（57本来是EBADSLT(Invalid slot)的意思，取其有的slot有错误的含义，用来表示部分或全部失败）。

{
"code" : 57,
"message" : "Part failed",
"items" : \[{
"code" : 0,
"message" : "success",
"data" : {
"id" : 1
}
}, {
"code" : 22,
"message" : "invalid param"
}
]
}

关于HTTP状态码在Restful API里应该如何结合使用，网上争论激烈，到底应该用状态码来表示错误，还是应该在JSON里面填写errorCode。比如这里：

<https://stackoverflow.com/questions/942951/rest-api-error-return-good-practices/34324179#34324179>

<https://stackoverflow.com/questions/2380554/rest-mapping-application-errors-to-http-status-codes?noredirect=1&lq=1>

我们可以看到，不少厂商，其实结合了两者同时使用，比如IBM的API规范定义如下：

上面，他不仅支持Http Response Code，还将Http Response Code放到JSON块里面返回，目的是为了方便获取Http Response Code，不过有些多此一举，他的错误码，会有一个映射关系，比如404下，有code 1002, 1003分别代表什么含义。这种方式并没有什么问题，而且主流的API管理工具，也支持Http Response Code含义区分。常见的错误码含义：

类型	错误码
GET返回值
200 - 请求成功。

206 - 请求成功，但只返回了部分（分页场景）。

POST返回值
201 - 同步创建成功。

202 - 接收成功，将进行异步处理。

PUT返回值
200 - 同步更新成功（原资源已存在）。

201 - 同步创建成功（原资源不存在，和POST类似）。

202 - 接收成功，将进行异步处理。

PATCH返回值
200 - 同步更新成功（原资源存在）。

202 - 接收成功，将进行异步处理。

DELETE返回值
200 - 同步删除成功。

202 - 接收成功，将进行异步处理。

HEAD返回值	404 - 表示不存在。

通过多方考察和分析，包括Google和Facebook的使用来看，我们得出一个结论，将Http Response Code当成HTTP层的错误码，而errorCode当成应用层的错误码，这样一个划分逻辑更清晰。

所以，只要是到应用层处理逻辑获取到了请求数据，并且不需要状态码协同配合的情况，都应该使用状态码200，然后内部再返回code错误。

举例1，状态码使用场景。

我们收到一个请求/users?token=xxxx，如果是/users这个资源在Apache里面配置为没不具备访问权限，则此时应该由Apache直接返回，此时就是HTTP层错误，返回HTTP Response Code 401。

举例2，错误码使用场景。

我们收到一个请求/users?token=xxxx，如果是/users这个资源具备访问权限，并且进入到了PHP框架代码，框架代码校验token不通过，此时应该返回HTTP Response Code为200，同时附带错误消息：

{
"code" : 13,
"message" : "Token校验失败！"
}
所以，基本上，我们做API的时候，基本不需要考虑状态码的情况，因为我们全在应用层，如此设计，旨在简化我们的逻辑，对于有的场景，确实需要联动HTTP Response Code的，可以联动，比如上述，也可以返回HTTP Response Code为401，并附带errorCode错误码13。

状态码的具体含义参考：

<https://www.codetinkerer.com/2015/12/04/choosing-an-http-status-code.html>

<https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html>

状态码的RFC参考：

<https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>

## 7 错误码

应用层错误码，其意义在于精确定位错误类型，例如5和3表示不同含义，调用端可以根据不同错误码，做更进一步处理，假设只有message（message变动可能性大，而且国际化导致更改），程序很难对错误做进一步处理，一般只能做错误传递。

错误码为数字的原因：

1）数字是所有语言的内置类型，存储不需要额外开辟对象或者堆空间；错误码通过函数参数等方式传递的时候，也不需要考虑类似谁分配谁释放的问题。

2）数字的比较是非常简单的操作(比如有的语言switch case不支持字符串，但是支持数字，字符串需要if else if else方式去比较)，不消耗多少CPU。

3）数字也可以做一些有具体含义的编码，例如HTTP RESPONSE CODE，用4xx和2xx表示不同含义。

4）数字还可以做范围比较，例如 1000 < errno < 10005 这一段表示某一类型错误。

5）数字的errno如果是连续的，用errno对应“错误描述”时可以不使用hash表，而用array即可做translate。例如 en\[1] = "param invalid"; zh\[1] = "参数错误";

6）数字可以兼容C语言系列的API errno直接转换。

为了提高可读写，建议产品线根据语言将errno定义成类似的宏或者常量（不使用原始的数字），例如，如果要写:

    printf("{\"code\": %d}", 1);

这样一个回复，在c语言里面应该是写为：

```
printf("{\"code\": %d}", EPERM);

```

## 9 编码模式

REST API支持多种Encoding schemes，用的比较多的是JSON和XML，其次还有CSV，ROW格式等，为了对接不同类型的客户端，特别是在联动外部客户设备的时候，编码模式就会显示出他的价值。

理论上，数据构造层是不需要考虑编码模式的，应由专门的编码模式转换层来根据client的请求转换编码模式。

比如，请求为JSON：Content-Type: application/json

{
"id": 0,
"userName": "string",
"email": "string"
}
请求为XML：Content-Type: application/xml

&lt;?xml version="1.0" encoding="UTF-8"?&gt;

&lt;User&gt;
  &lt;id&gt;0&lt;/id&gt;
  &lt;userName&gt;string&lt;/userName&gt;
  &lt;email&gt;string&lt;/email&gt;
&lt;/User&gt;
之所以要说明编码模式，是今后在设计API底层框架的时候，应该要支持encoding schemes之间的转换。

## 10 缓存设计

很多耗时操作，后端会提前做好缓存，请求时直接返回cache。

如果用户不想获取缓存数据（获取实时数据），可以禁用cache。我们统一定义这类需求，只需要在GET参数里面带\_cache=0即表示cache disable； \_cache=1表示cache enable，其他的取值，暂时保留，产品线不能自行定义使用意义（如果有需求，请组织讨论）。

## 11 异步原则

有人提出单独说一下异步消息的处理，这个其实没什么特别的，通用设计是先PUT、POST、DELETE一个异步任务，在返回值里带上后端异步任务的ID，前端间隙GET此异步任务ID，来获取最终的进度。

例如，我们准被创建一个虚拟机，异步请求定义为：

POST /api/vm
{
"name": "MySQL Server",
"cpu" : 2,
"memory" : 1024
}
返回值为：

HTTP / 1.1 200 OK
{
"code":0,
"message" : "VM is creating!",
"data" :
{
"id": string,    // 例如返回id="2018031420080001"
"timeout": int,  // 例如180，表示最多检查180s
}
}
客户端再根据返回的id，再次查询进度：

GET /api/vm/\:id

返回当前更新进度值：

HTTP / 1.1 200 OK
{
"code":0,               //如果找不到此任务id，code为2，ENOENT
"message" : "step 2: copy images!",
"data" :
{
"percent": int,    //完成度，取值范围为\[0, 100]，例如90表示完成90%
}
}

## 12 国际化

所有字符串，全部采用UTF-8编码，禁止采用任何其他编码，对于ANSI表里面可显示字符\[0x20,0x80)之外的字符，全部采用Unicode code point，即\uxxx方式编码：

/\[\u0009\u000A\u000D\u0020-\uFFFF]/

转换Unicode code point的时候注意，对于超过0xFFFF的部分，以UTF-16的编码代理方式(surrogate pair)表示，即将Unicode code point以两个code unit表示。

UNICODE参考：<http://unicode.org/standard/standard.html>

同时，所有API请求，必须在头部附带如下固定Content-Type：

Content-Type\:application/json;charset=UTF-8

其中charset如果不指定，默认表示UTF-8。

转换示例代码：

CMP > RESTful API格式规范v2.4（公司规范） > image2020-7-28\_9-21-27.png

请处理好字符串截断，不能包含截断后的UTF8字符！给一段截断示例代码：

int Utf8CharLength(const char\* start, int length)
{
if (NULL == start || length <= 0)
{//invalid param
return -1;
}

    int firstChar = (unsigned char)(*start);
    //这是单字节情况：0xxxxxxx -> [0b00000000(0x00), 0b10000000(0x80))
    if (firstChar < 0x80)
    {
        return 1; //1字节
    }

    //这是follow字节：10xxxxxx -> [0b10000000(0x80), 0b11000000(0xC0))
    if (firstChar < 0xC0)//
    {
        return 0; //0表示follow字节
    }

    // 0000 0080 - 0000 07FF | 110xxxxx 10xxxxxx
    // 这是双字节：110xxxxx -> [0b11000000(0xC0), 0b11100000(0xE0))
    if (firstChar < 0xE0)
    {
        return (length >= 2) ? 2 : -2;
    }

    // 0000 0800 - 0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
    // 这是三字节：1110xxxx -> [0b11100000(0xE0), 0b11110000(0xF0))
    if (firstChar < 0xF0)
    {
        return (length >= 3) ? 3 : -3;
    }

    // 0001 0000 - 0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
    // 这是四字节：11110xxx -> [0b11110000(0xF0), 0b11111000(0xF8))
    if (firstChar < 0xF8)
    {//四字节的时候，我们还应该判断是否Codepoint < 0x10FFFF，这里省略了。
        return (length >= 4) ? 4 : -4;
    }

    // invalid char
    return -1;

}

int Utf8RoundCut(char\* str, int\* plength)
{
if (NULL == str || NULL == plength || \*plength < 0)
{
return -1;
}

    int length = *plength;
    if (0 == length)
    {
        return 0;
    }

    int offset = (length <= 4) ? 0 : (length - 4), chMaxLen, chLen;

    while (offset < length)
    {
        chMaxLen = length - offset;
        chLen = Utf8CharLength(&str[offset], chMaxLen);
        if (chLen < 0)
        {
            str[offset] = '\0';
            *plength = offset;
            return chMaxLen;
        }
        else
        {// == 0 || > 0
            offset += ((0 == chLen)?1:chLen); //check next
        }
    }
    return 0;

}

### 12.2 Language定义

复用HTTP协议头部信息定义，国际化所需语言，直接在HTTP头部定义，例如：

Accept-Language\:zh-CN

请求英文，头部定义为：

Accept-Language\:en-US

如果参数里面定义了lang，则参数里面的lang会override掉Accept-Language动作，用于扩展支持某些场景，无法修改HTTP头部的情况。同时，在一些具备让用户下拉选择国际化的设计中，用lang参数可能会比Accept-Language来得方便一些。

### 12.3 时间格式

建议尽量传 UTC seconds，就是c语言中的time(NULL)返回的秒数。

time() returns the time since the Epoch (00:00:00 UTC, January 1, 1970), measured in seconds.

如果觉得可视方面不便，可以采用ISO 8601标准："yyyy-MM-dd'T'HH\:mm\:ss.SSS'Z'"，例如，将本地时间"Thu Sep 27 2012 11:00:00 GMT+0800" 转换为 "2012-09-27T03:00:00Z"，对于有毫秒的情况，在Z前添加毫秒，如："2012-09-27T03:00:00.300Z"，不到万不得已不要用这种方案。

