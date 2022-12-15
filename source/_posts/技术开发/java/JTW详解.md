**JTW详解**

**spring boot集成jwt实现token认证；**

\1. 什么是jwt?

Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).定义了一种简洁的，自包含的方法用于通信双方之间以JSON对象的形式安全的传递信息。因为数字签名的存在，这些信息是可信的，JWT可以使用HMAC算法或者是RSA的公私秘钥对进行签名。

\2. jwt的工作流程

\1. 用户使用账号和密码发出post请求；

\2. 服务器使用私钥创建一个jwt；

\3. 服务器返回这个jwt给浏览器；

\4. 浏览器将该jwt串在请求头中向服务器发送请求；

\5. 服务器验证该jwt；

\6. 返回响应的资源给浏览器。

![img](C:\Users\14133\AppData\Local\YNote\data\m18378511016@163.com\f5f9098e49bc44e887b4c730a09776c1\jwt.png)

\3. jwt结构

1）Header 头部：JWT的头部承载两部分信息：token类型和采用的加密算法。

2）Payload：存放有效信息的地方。

3）Signature：签证信息。

（完整见博客https://www.jianshu.com/p/e88d3f8151db）