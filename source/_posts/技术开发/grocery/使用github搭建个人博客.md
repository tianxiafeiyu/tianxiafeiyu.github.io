---
abbrlink: '0'
---
看到一篇文章 GitHub Pages + Hexo 搭建个人博客，感觉效果不错

想当年，自己也曾用阿里云+spring boot搭建过个人博客，不过后面也是不了了之（甚至服务器到期都懒得去看了~~），现在有这个白嫖的方案怎么能错过呢

今天晚上下班就开整

## 关于 github pages

GitHub Pages 是一项静态站点托管服务，它直接从 GitHub 上的仓库获取 HTML、CSS 和 JavaScript 文件，然后来解析他们，发布服务。

### 类型

有三种类型的 GitHub Pages 站点：项目、用户和组织。&#x20;

项目站点连接到 GitHub 上托管的特定项目，例如 JavaScript 库或配方集合。

若要发布用户站点，必须创建名为 `<username>.github.io` 的个人帐户拥有的存储库。 若要发布组织站点，必须创建名为 `<organization>.github.io` 的组织帐户拥有的存储库。 除非使用的是自定义域，否则用户和组织站点在 `http(s)://<username>.github.io` 或 `http(s)://<organization>.github.io` 中可用。

项目站点的源文件与其项目存储在同一个仓库中。 除非使用的是自定义域，否则项目站点在 `http(s)://<username>.github.io/<repository>` 或 `http(s)://<organization>.github.io/<repository>` 中可用。

GitHub 上的每个帐户创建一个用户或组织站点。 项目站点（无论是组织还是个人帐户拥有）没有限制。

### 发布

GitHub Pages 会发布您推送到仓库的任何静态文件。 您可以创建自己的静态文件或使用静态站点生成器为您构建站点。 您还可以在本地或其他服务器上自定义自己的构建过程。

如果使用自定义生成过程或 Jekyll 以外的静态站点生成器，可以编写 GitHub Actions 来生成和发布站点。

### 使用限制

GitHub Pages 站点受到以下使用限制的约束：

*   GitHub Pages 源存储库的建议限制为 1 GB。
*   发布的 GitHub Pages 站点不得超过 1 GB。
*   GitHub Pages 站点的软带宽限制为每月 100 GB。
*   GitHub Pages 站点的软限制为每小时 10 次生成。 如果使用自定义 GitHub Actions 工作流生成和发布站点，则此限制不适用
*   为了为所有 GitHub Pages 站点提供一致的服务质量，可能会实施速率限制。 这些速率限制无意干扰 GitHub Pages 的合法使用。 如果你的请求触发了速率限制，你将收到相应响应，其中包含 HTTP 状态代码 `429` 以及信息性 HTML 正文。

## 关于Hexo

Hexo 是一个快速、简洁且高效的博客框架。Hexo 使用 [Markdown](http://daringfireball.net/projects/markdown/)（或其他渲染引擎）解析文章，在几秒内，即可利用靓丽的主题生成静态网页。

详细信息可阅读官方文档：<https://hexo.io/zh-cn/docs/>

### 主题

我比较喜欢简洁的主题，这里选用我比较心水的一个主题，类wiki风格，非常的简洁和好用

<https://github.com/zthxxx/hexo-theme-Wikitten/blob/master/README_zh-CN.md>

<https://github.com/Norcy/wiki/tree/HexoBackup/themes/Wikitten>

### 插件

hexo插件推荐：<https://blog.csdn.net/qq_43701912/article/details/107310923>



## 一些使用心得

### 如何发布文章

1.  使用github.dev，在仓库页面按下键盘 `.` 进入，或者仓库地址 `.com` 改为 `.dev` 进入 ,是一个在线vscode编辑器
2.  本地修改新增md文件后push

### &#x20;参考资料
- [GitHub Pages + Hexo搭建个人博客网站，史上最全教程](https://blog.csdn.net/bbsyi/article/details/119101852)
- [GitHub Pages Docs](https://docs.github.com/cn/pages/getting-started-with-github-pages/about-github-pages)
- [Hexo官方文档](https://hexo.io/zh-cn/docs/)
- [Wikitten](https://github.com/zthxxx/hexo-theme-Wikitten)