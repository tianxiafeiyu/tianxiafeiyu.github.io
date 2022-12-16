---
title: GraphQL 入门
date: 2022-12-15 23:10:53
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - GraphQL 入门
---
## GraphQL 入门
GraphQL 是一个用于 API 的查询语言，是一个使用基于类型系统来执行查询的服务端运行时（类型系统由你的数据定义）。GraphQL 并没有和任何特定数据库或者存储引擎绑定，而是依靠你现有的代码和数据支撑。

一个 GraphQL 服务是通过定义类型和类型上的字段来创建的，然后给每个类型上的每个字段提供解析函数。例如，一个 GraphQL 服务告诉我们当前登录用户是 me，这个用户的名称可能像这样：
```
type Query {
  me: User
}

type User {
  id: ID
  name: String
}
```
一并的还有每个类型上字段的解析函数：

```
function Query_me(request) {
  return request.auth.user;
}

function User_name(user) {
  return user.getName();
}
```

一旦一个 GraphQL 服务运行起来（通常在 web 服务的一个 URL 上），它就能接收 GraphQL 查询，并验证和执行。接收到的查询首先会被检查确保它只引用了已定义的类型和字段，然后运行指定的解析函数来生成结果。

例如：
```
{
  me {
    name
  }
}
```
返回结果：
```
{
  "me": {
    "name": "Luke Skywalker"
  }
}
```

## GraphQL 的查询和变更

#### 字段（Fields）
简单而言，GraphQL 是关于请求对象上的特定字段。我们以一个非常简单的查询以及其结果为例：
```
{
  hero {
    name
  }
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2"
    }
  }
}
```
查询和其结果拥有几乎一样的结构。这是 GraphQL 最重要的特性，因为这样一来，你就总是能得到你想要的数据，而服务器也准确地知道客户端请求的字段。

`name` 字段返回 `String` 类型，在这个示例中是《星球大战》主角的名字是：`"R2-D2"`。

前一例子中，我们请求了我们主角的名字，返回了一个字符串类型（String），但是字段也能指代对象类型（Object）。这个时候，你可以对这个对象的字段进行次级选择（sub-selection）。GraphQL 查询能够遍历相关对象及其字段，使得客户端可以一次请求查询大量相关数据，而不像传统 REST 架构中那样需要多次往返查询。
```
{
  hero {
    name
    # 查询可以有备注！
    friends {
      name
    }
  }
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```
这个例子中，friends 返回了一个数组的项目，GraphQL 查询会同等看待单个项目或者一个列表的项目，然而我们可以通过 schema 所指示的内容来预测将会得到哪一种。

#### 参数（Arguments）
即使我们能做的仅仅是遍历对象及其字段，GraphQL 就已经是一个非常有用的数据查询语言了。但是当你加入给字段传递参数的能力时，事情会变得更加有趣。

```
{
  human(id: "1000") {
    name
    height
  }
}
```
```
{
  "data": {
    "human": {
      "name": "Luke Skywalker",
      "height": 1.72
    }
  }
}
```
参数可以是多种不同的类型。上面例子中，我们使用了一个枚举类型，其代表了一个有限选项集合（本例中为长度单位，即是 METER 或者 FOOT）。GraphQL 自带一套默认类型，但是 GraphQL 服务器可以声明一套自己的定制类型，只要能序列化成你的传输格式即可。

[更多的 GraphQL 类型系统请点击这里](https://graphql.cn/learn/schema)

#### 别名（Aliases）
如果你眼睛够锐利，你可能已经发现，即便结果中的字段与查询中的字段能够匹配，但是因为他们并不包含参数，你就没法通过不同参数来查询相同字段。这便是为何你需要别名 —— 这可以让你重命名结果中的字段为任意你想到的名字。

```
{
  empireHero: hero(episode: EMPIRE) {
    name
  }
  jediHero: hero(episode: JEDI) {
    name
  }
}
```
```
{
  "data": {
    "empireHero": {
      "name": "Luke Skywalker"
    },
    "jediHero": {
      "name": "R2-D2"
    }
  }
}
```
上例中，两个 hero 字段将会存在冲突，但是因为我们可以将其另取一个别名，我们也就可以在一次请求中得到两个结果。

#### 片段（Fragments）
假设我们的 app 有比较复杂的页面，将正反派主角及其友军分为两拨。你立马就能想到对应的查询会变得复杂，因为我们需要将一些字段重复至少一次 —— 两方各一次以作比较。

这就是为何 GraphQL 包含了称作片段的可复用单元。片段使你能够组织一组字段，然后在需要它们的的地方引入。下面例子展示了如何使用片段解决上述场景：

```
{
  leftComparison: hero(episode: EMPIRE) {
    ...comparisonFields
  }
  rightComparison: hero(episode: JEDI) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  appearsIn
  friends {
    name
  }
}
```
```
{
  "data": {
    "leftComparison": {
      "name": "Luke Skywalker",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ],
      "friends": [
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        },
        {
          "name": "C-3PO"
        },
        {
          "name": "R2-D2"
        }
      ]
    },
    "rightComparison": {
      "name": "R2-D2",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ],
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```
你可以看到上面的查询如何漂亮地重复了字段。片段的概念经常用于将复杂的应用数据需求分割成小块，特别是你要将大量不同片段的 UI 组件组合成一个初始数据获取的时候。

在片段内使用变量 

片段可以访问查询或变更中声明的变量。详见 [变量](https://graphql.cn/learn/queries/#variables)。

```
query HeroComparison($first: Int = 3) {
  leftComparison: hero(episode: EMPIRE) {
    ...comparisonFields
  }
  rightComparison: hero(episode: JEDI) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  friendsConnection(first: $first) {
    totalCount
    edges {
      node {
        name
      }
    }
  }
}
```
```
{
  "data": {
    "leftComparison": {
      "name": "Luke Skywalker",
      "friendsConnection": {
        "totalCount": 4,
        "edges": [
          {
            "node": {
              "name": "Han Solo"
            }
          },
          {
            "node": {
              "name": "Leia Organa"
            }
          },
          {
            "node": {
              "name": "C-3PO"
            }
          }
        ]
      }
    },
    "rightComparison": {
      "name": "R2-D2",
      "friendsConnection": {
        "totalCount": 3,
        "edges": [
          {
            "node": {
              "name": "Luke Skywalker"
            }
          },
          {
            "node": {
              "name": "Han Solo"
            }
          },
          {
            "node": {
              "name": "Leia Organa"
            }
          }
        ]
      }
    }
  }
}
```

#### 变量（Variables）

目前为止，我们将参数写在了查询字符串内。但是在很多应用中，字段的参数可能是动态的：例如，可能是一个"下拉菜单"让你选择感兴趣的《星球大战》续集，或者是一个搜索区，或者是一组过滤器。

将这些动态参数直接传进查询字符串并不是好主意，因为这样我们的客户端就得动态地在运行时操作这些查询字符串了，再把它序列化成 GraphQL 专用的格式。其实，GraphQL 拥有一级方法将动态值提取到查询之外，然后作为分离的字典传进去。这些动态值即称为变量。

使用变量之前，我们得做三件事：
1. 使用 `$variableName` 替代查询中的静态值。
2. 声明 `$variableName` 为查询接受的变量之一。
3. 将 `variableName: value` 通过传输专用（通常是 JSON）的分离的变量字典中。

全部做完之后就像这个样子：
```
# { "graphiql": true, "variables": { "episode": JEDI } }
query HeroNameAndFriends($episode: Episode) {
  hero(episode: $episode) {
    name
    friends {
      name
    }
  }
}
```
这样一来，我们的客户端代码就只需要传入不同的变量，而不用构建一个全新的查询了。这事实上也是一个良好实践，意味着查询的参数将是动态的 —— 我们决不能使用用户提供的值来字符串插值以构建查询。

#### 变量定义（Variable definitions）
变量定义看上去像是上述查询中的 ($episode: Episode)。其工作方式跟类型语言中函数的参数定义一样。它以列出所有变量，变量前缀必须为 $，后跟其类型，本例中为 Episode。

所有声明的变量都必须是标量、枚举型或者输入对象类型。所以如果想要传递一个复杂对象到一个字段上，你必须知道服务器上其匹配的类型。可以从Schema页面了解更多关于输入对象类型的信息。

变量定义可以是可选的或者必要的。上例中，Episode 后并没有 !，因此其是可选的。但是如果你传递变量的字段要求非空参数，那变量一定是必要的。

如果想要进一步了解变量定义的句法，可以学习 GraphQL 的 schema 语言。schema 语言在 Schema 中有细述。

#### 默认变量（Default variables）
可以通过在查询中的类型定义后面附带默认值的方式，将默认值赋给变量。
```
query HeroNameAndFriends($episode: Episode = "JEDI") {
  hero(episode: $episode) {
    name
    friends {
      name
    }
  }
}
```
当所有变量都有默认值的时候，你可以不传变量直接调用查询。如果任何变量作为变量字典的部分传递了，它将覆盖其默认值。

#### 指令（Directives）
我们上面讨论的变量使得我们可以避免手动字符串插值构建动态查询。传递变量给参数解决了一大堆这样的问题，但是我们可能也需要一个方式使用变量动态地改变我们查询的结构。譬如我们假设有个 UI 组件，其有概括视图和详情视图，后者比前者拥有更多的字段。

我们来构建一个这种组件的查询：
```
query Hero($episode: Episode, $withFriends: Boolean!) {
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}

variables:
{
  "episode": "JEDI",
  "withFriends": false
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2"
    }
  }
}
```
尝试修改上面的变量，传递 true 给 withFriends，看看结果的变化。

我们用了 GraphQL 中一种称作指令的新特性。一个指令可以附着在字段或者片段包含的字段上，然后以任何服务端期待的方式来改变查询的执行。GraphQL 的核心规范包含两个指令，其必须被任何规范兼容的 GraphQL 服务器实现所支持：
- @include(if: Boolean) 仅在参数为 true 时，包含此字段。
- @skip(if: Boolean) 如果参数为 true，跳过此字段。

指令在你不得不通过字符串操作来增减查询的字段时解救你。服务端实现也可以定义新的指令来添加新的特性。

#### 变更（Mutations）
GraphQL 的大部分讨论集中在数据获取，但是任何完整的数据平台也都需要一个改变服务端数据的方法。

REST 中，任何请求都可能最后导致一些服务端副作用，但是约定上建议不要使用 GET 请求来修改数据。GraphQL 也是类似 —— 技术上而言，任何查询都可以被实现为导致数据写入。然而，建一个约定来规范任何导致写入的操作都应该显式通过变更（mutation）来发送。

就如同查询一样，如果任何变更字段返回一个对象类型，你也能请求其嵌套字段。获取一个对象变更后的新状态也是十分有用的。我们来看看一个变更例子：
```
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
  createReview(episode: $ep, review: $review) {
    stars
    commentary
  }
}

variables:
{
  "ep": "JEDI",
  "review": {
    "stars": 5,
    "commentary": "This is a great movie!"
  }
}
```
```
{
  "data": {
    "createReview": {
      "stars": 5,
      "commentary": "This is a great movie!"
    }
  }
}
```
注意 `createReview` 字段如何返回了新建的 `review` 的 `stars` 和 `commentary` 字段。这在变更已有数据时特别有用，例如，当一个字段自增的时候，我们可以在一个请求中变更并查询这个字段的新值。

你也可能注意到，这个例子中，我们传递的 review 变量并非标量。它是一个输入对象类型，一种特殊的对象类型，可以作为参数传递。你可以在 Schema 页面上了解到更多关于输入类型的信息。

##### 变更中的多个字段（Multiple fields in mutations）
一个变更也能包含多个字段，一如查询。查询和变更之间名称之外的一个重要区别是：

查询字段时，是并行执行，而变更字段时，是线性执行，一个接着一个。

这意味着如果我们一个请求中发送了两个 incrementCredits 变更，第一个保证在第二个之前执行，以确保我们不会出现竞态。

#### 内联片段（Inline Fragments） 
跟许多类型系统一样，GraphQL schema 也具备定义接口和联合类型的能力。在 [schema 指南中可了解更多](https://graphql.cn/learn/schema/#interfaces)。

如果你查询的字段返回的是接口或者联合类型，那么你可能需要使用内联片段来取出下层具体类型的数据：

```
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    ... on Droid {
      primaryFunction
    }
    ... on Human {
      height
    }
  }
}

variables:
{
    "ep": "JEDI"
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "primaryFunction": "Astromech"
    }
  }
}
```
这个查询中，`hero` 字段返回 `Character` 类型，取决于 `episode` 参数，其可能是 `Human` 或者 `Droid` 类型。在直接选择的情况下，你只能请求 `Character` 上存在的字段，譬如 `name`。

如果要请求具体类型上的字段，你需要使用一个类型条件内联片段。因为第一个片段标注为 `... on Droid`，`primaryFunction` 仅在 `hero` 返回的 `Character` 为 `Droid` 类型时才会执行。同理适用于 `Human` 类型的 `height` 字段。

具名片段也可以用于同样的情况，因为具名片段总是附带了一个类型。

#### 元字段（Meta fields） 
某些情况下，你并不知道你将从 GraphQL 服务获得什么类型，这时候你就需要一些方法在客户端来决定如何处理这些数据。GraphQL 允许你在查询的任何位置请求 __typename，一个元字段，以获得那个位置的对象类型名称。

```
{
  search(text: "an") {
    __typename
    ... on Human {
      name
    }
    ... on Droid {
      name
    }
    ... on Starship {
      name
    }
  }
}
```
```
{
  "data": {
    "search": [
      {
        "__typename": "Human",
        "name": "Han Solo"
      },
      {
        "__typename": "Human",
        "name": "Leia Organa"
      },
      {
        "__typename": "Starship",
        "name": "TIE Advanced x1"
      }
    ]
  }
}
```
上面的查询中，search 返回了一个联合类型，其可能是三种选项之一。没有 __typename 字段的情况下，几乎不可能在客户端分辨开这三个不同的类型。

GraphQL 服务提供了不少元字段，剩下的部分用于描述 内省 系统。

## Schema 和类型
在本节中，，你将学到关于 GraphQL 类型系统中所有你需要了解的知识，以及类型系统如何描述可以查询的数据。因为 GraphQL 可以运行在任何后端框架或者编程语言之上，我们将摒除实现上的细节而仅仅专注于其概念。

####  类型系统（Type System）
如果你之前见到过 GraphQL 查询，你就知道 GraphQL 查询语言基本上就是关于选择对象上的字段。因此，例如在下列查询中：
```
{
  hero {
    name
    appearsIn
  }
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ]
    }
  }
}
```
1. 我们以一个特殊的对象 "root" 开始
1. 选择其上的 hero 字段
1. 对于 hero 返回的对象，我们选择 name 和 appearsIn 字段

因为一个 GraphQL 查询的结构和结果非常相似，因此即便不知道服务器的情况，你也能预测查询会返回什么结果。但是一个关于我们所需要的数据的确切描述依然很有意义，我们能选择什么字段？服务器会返回哪种对象？这些对象下有哪些字段可用？这便是引入 schema 的原因。

每一个 GraphQL 服务都会定义一套类型，用以描述你可能从那个服务查询到的数据。每当查询到来，服务器就会根据 schema 验证并执行查询。

#### 类型语言（Type Language）
GraphQL 服务可以用任何语言编写，因为我们并不依赖于任何特定语言的句法句式（譬如 JavaScript）来与 GraphQL schema 沟通，我们定义了自己的简单语言，称之为 “GraphQL schema language” —— 它和 GraphQL 的查询语言很相似，让我们能够和 GraphQL schema 之间可以无语言差异地沟通。

#### 对象类型和字段（Object Types and Fields）
一个 GraphQL schema 中的最基本的组件是对象类型，它就表示你可以从服务上获取到什么类型的对象，以及这个对象有什么字段。使用 GraphQL schema language，我们可以这样表示它：
```
type Character {
  name: String!
  appearsIn: [Episode!]!
}
```
虽然这语言可读性相当好，但我们还是一起看看其用语，以便我们可以有些共通的词汇：
- Character 是一个 GraphQL 对象类型，表示其是一个拥有一些字段的类型。你的 schema 中的大多数类型都会是对象类型。
- name 和 appearsIn 是 Character 类型上的字段。这意味着在一个操作 Character 类型的 GraphQL 查询中的任何部分，都只能出现 name 和 appearsIn 字段。
- String 是内置的标量类型之一 —— 标量类型是解析到单个标量对象的类型，无法在查询中对它进行次级选择。后面我们将细述标量类型。
- String! 表示这个字段是非空的，GraphQL 服务保证当你查询这个字段后总会给你返回一个值。在类型语言里面，我们用一个感叹号来表示这个特性。
- [Episode!]! 表示一个 Episode 数组。因为它也是非空的，所以当你查询 appearsIn 字段的时候，你也总能得到一个数组（零个或者多个元素）。且由于 Episode! 也是非空的，你总是可以预期到数组中的每个项目都是一个 Episode 对象。

现在你知道一个 GraphQL 对象类型看上去是怎样，也知道如何阅读基础的 GraphQL 类型语言了。

#### 参数（Arguments）
GraphQL 对象类型上的每一个字段都可能有零个或者多个参数，例如下面的 length 字段
```
type Starship {
  id: ID!
  name: String!
  length(unit: LengthUnit = METER): Float
}
```
所有参数都是具名的，不像 JavaScript 或者 Python 之类的语言，函数接受一个有序参数列表，而在 GraphQL 中，所有参数必须具名传递。本例中，length 字段定义了一个参数，unit。

参数可能是必选或者可选的，当一个参数是可选的，我们可以定义一个默认值 —— 如果 unit 参数没有传递，那么它将会被默认设置为 METER。

#### 查询和变更类型（The Query and Mutation Types）
你的 schema 中大部分的类型都是普通对象类型，但是一个 schema 内有两个特殊类型：
```
schema {
  query: Query
  mutation: Mutation
}
```
每一个 GraphQL 服务都有一个 query 类型，可能有一个 mutation 类型。这两个类型和常规对象类型无差，但是它们之所以特殊，是因为它们定义了每一个 GraphQL 查询的入口。因此如果你看到一个像这样的查询：
```
query {
  hero {
    name
  }
  droid(id: "2000") {
    name
  }
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2"
    },
    "droid": {
      "name": "C-3PO"
    }
  }
}
```
那表示这个 GraphQL 服务需要一个 Query 类型，且其上有 hero 和 droid 字段：
```
type Query {
  hero(episode: Episode): Character
  droid(id: ID!): Droid
}
```
变更也是类似的工作方式 —— 你在 Mutation 类型上定义一些字段，然后这些字段将作为 mutation 根字段使用，接着你就能在你的查询中调用。

有必要记住的是，除了作为 schema 的入口，Query 和 Mutation 类型与其它 GraphQL 对象类型别无二致，它们的字段也是一样的工作方式。

#### 标量类型（Scalar Types）
一个对象类型有自己的名字和字段，而某些时候，这些字段必然会解析到具体数据。这就是标量类型的来源：它们表示对应 GraphQL 查询的叶子节点。

下列查询中，name 和 appearsIn 字段将解析到标量类型：
```
{
  hero {
    name
    appearsIn
  }
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ]
    }
  }
}
```
我们知道这些字段没有任何次级字段 —— 因为让它们是查询的叶子节点。

GraphQL 自带一组默认标量类型：
- Int：有符号 32 位整数。
- Float：有符号双精度浮点值。
- String：UTF‐8 字符序列。
- Boolean：true 或者 false。
- ID：ID 标量类型表示一个唯一标识符，通常用以重新获取对象或者作为缓存中的键。ID 类型使用和 String 一样的方式序列化；然而将其定义为 ID 意味着并不需要人类可读型。

大部分的 GraphQL 服务实现中，都有自定义标量类型的方式。例如，我们可以定义一个 Date 类型：
```
scalar Date
```
然后就取决于我们的实现中如何定义将其序列化、反序列化和验证。例如，你可以指定 Date 类型应该总是被序列化成整型时间戳，而客户端应该知道去要求任何 date 字段都是这个格式。

#### 枚举类型（Enumeration Types）
也称作枚举（enum），枚举类型是一种特殊的标量，它限制在一个特殊的可选值集合内。这让你能够：
1. 验证这个类型的任何参数是可选值的的某一个
1. 与类型系统沟通，一个字段总是一个有限值集合的其中一个值。

下面是一个用 GraphQL schema 语言表示的 enum 定义：
```
enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}
```
这表示无论我们在 schema 的哪处使用了 Episode，都可以肯定它返回的是 NEWHOPE、EMPIRE 和 JEDI 之一。

注意，各种语言实现的 GraphQL 服务会有其独特的枚举处理方式。对于将枚举作为一等公民的语言，它的实现就可以利用这个特性；而对于像 JavaScript 这样没有枚举支持的语言，这些枚举值可能就被内部映射成整数值。当然，这些细节都不会泄漏到客户端，客户端会根据字符串名称来操作枚举值。

#### 列表和非空（Lists and Non-Null）
对象类型、标量以及枚举是 GraphQL 中你唯一可以定义的类型种类。但是当你在 schema 的其他部分使用这些类型时，或者在你的查询变量声明处使用时，你可以给它们应用额外的类型修饰符来影响这些值的验证。我们先来看一个例子：
```
type Character {
  name: String!
  appearsIn: [Episode]!
}
```
此处我们使用了一个 String 类型，并通过在类型名后面添加一个感叹号!将其标注为非空。这表示我们的服务器对于这个字段，总是会返回一个非空值，如果它结果得到了一个空值，那么事实上将会触发一个 GraphQL 执行错误，以让客户端知道发生了错误。

非空类型修饰符也可以用于定义字段上的参数，如果这个参数上传递了一个空值（不管通过 GraphQL 字符串还是变量），那么会导致服务器返回一个验证错误。
```
query DroidById($id: ID!) {
  droid(id: $id) {
    name
  }
}

variables:
{
  "id": null
}
```
```
{
  "errors": [
    {
      "message": "Variable \"$id\" of required type \"ID!\" was not provided.",
      "locations": [
        {
          "line": 1,
          "column": 17
        }
      ]
    }
  ]
}
```
列表的运作方式也类似：我们也可以使用一个类型修饰符来标记一个类型为 List，表示这个字段会返回这个类型的数组。在 GraphQL schema 语言中，我们通过将类型包在方括号（[ 和 ]）中的方式来标记列表。列表对于参数也是一样的运作方式，验证的步骤会要求对应值为数组。

非空和列表修饰符可以组合使用。例如你可以要求一个非空字符串的数组：
```
myField: [String!]
```
这表示数组本身可以为空，但是其不能有任何空值成员。用 JSON 举例如下：
```
myField: null // 有效
myField: [] // 有效
myField: ['a', 'b'] // 有效
myField: ['a', null, 'b'] // 错误
```
然后，我们来定义一个不可为空的字符串数组：
```
myField: [String]!
```
这表示数组本身不能为空，但是其可以包含空值成员：
```
myField: null // 错误
myField: [] // 有效
myField: ['a', 'b'] // 有效
myField: ['a', null, 'b'] // 有效
```
你可以根据需求嵌套任意层非空和列表修饰符。

#### 接口（Interfaces）
跟许多类型系统一样，GraphQL 支持接口。一个接口是一个抽象类型，它包含某些字段，而对象类型必须包含这些字段，才能算实现了这个接口。

例如，你可以用一个 Character 接口用以表示《星球大战》三部曲中的任何角色：
```
interface Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
}
```
这意味着任何实现 Character 的类型都要具有这些字段，并有对应参数和返回类型。

例如，这里有一些可能实现了 Character 的类型：
```
type Human implements Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  starships: [Starship]
  totalCredits: Int
}

type Droid implements Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  primaryFunction: String
}
```
可见这两个类型都具备 Character 接口的所有字段，但也引入了其他的字段 totalCredits、starships 和 primaryFunction，这都属于特定的类型的角色。

当你要返回一个对象或者一组对象，特别是一组不同的类型时，接口就显得特别有用。

注意下面例子的查询会产生错误：
```
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    primaryFunction
  }
}

variables:
{
  "ep": "JEDI"
}
```
```
{
  "errors": [
    {
      "message": "Cannot query field \"primaryFunction\" on type \"Character\". Did you mean to use an inline fragment on \"Droid\"?",
      "locations": [
        {
          "line": 4,
          "column": 5
        }
      ]
    }
  ]
}
```
hero 字段返回 Character 类型，取决于 episode 参数，它可能是 Human 或者 Droid 类型。上面的查询中，你只能查询 Character 接口中存在的字段，而其中并不包含 primaryFunction。

如果要查询一个只存在于特定对象类型上的字段，你需要使用内联片段：
```
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    ... on Droid {
      primaryFunction
    }
  }
}

variables:
{
  "ep": "JEDI"
}
```
```
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "primaryFunction": "Astromech"
    }
  }
}
```
你可以在查询指南的 [内联片段](https://graphql.cn/learn/queries/#inline-fragments) 章节了解更多相关信息。

#### 联合类型（Union Types）
联合类型和接口十分相似，但是它并不指定类型之间的任何共同字段。
```
union SearchResult = Human | Droid | Starship
```
在我们的schema中，任何返回一个 SearchResult 类型的地方，都可能得到一个 Human、Droid 或者 Starship。注意，联合类型的成员需要是具体对象类型；你不能使用接口或者其他联合类型来创造一个联合类型。

这时候，如果你需要查询一个返回 SearchResult 联合类型的字段，那么你得使用条件片段才能查询任意字段。
```
{
  search(text: "an") {
    __typename
    ... on Human {
      name
      height
    }
    ... on Droid {
      name
      primaryFunction
    }
    ... on Starship {
      name
      length
    }
  }
}
```
```
{
  "data": {
    "search": [
      {
        "__typename": "Human",
        "name": "Han Solo",
        "height": 1.8
      },
      {
        "__typename": "Human",
        "name": "Leia Organa",
        "height": 1.5
      },
      {
        "__typename": "Starship",
        "name": "TIE Advanced x1",
        "length": 9.2
      }
    ]
  }
}
```
_typename 字段解析为 String，它允许你在客户端区分不同的数据类型。

此外，在这种情况下，由于 Human 和 Droid 共享一个公共接口（Character），你可以在一个地方查询它们的公共字段，而不必在多个类型中重复相同的字段：
```
{
  search(text: "an") {
    __typename
    ... on Character {
      name
    }
    ... on Human {
      height
    }
    ... on Droid {
      primaryFunction
    }
    ... on Starship {
      name
      length
    }
  }
}
```
注意 name 仍然需要指定在 Starship 上，否则它不会出现在结果中，因为 Starship 并不是一个 Character！

#### 输入类型（Input Types）
目前为止，我们只讨论过将例如枚举和字符串等标量值作为参数传递给字段，但是你也能很容易地传递复杂对象。这在变更（mutation）中特别有用，因为有时候你需要传递一整个对象作为新建对象。在 GraphQL schema language 中，输入对象看上去和常规对象一模一样，除了关键字是 input 而不是 type：
```
input ReviewInput {
  stars: Int!
  commentary: String
}
```
你可以像这样在变更（mutation）中使用输入对象类型：
```
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
  createReview(episode: $ep, review: $review) {
    stars
    commentary
  }
}

variables:
{
  "ep": "JEDI",
  "review": {
    "stars": 5,
    "commentary": "This is a great movie!"
  }
}
```
```
{
  "data": {
    "createReview": {
      "stars": 5,
      "commentary": "This is a great movie!"
    }
  }
}
```
输入对象类型上的字段本身也可以指代输入对象类型，但是你不能在你的 schema 混淆输入和输出类型。输入对象类型的字段当然也不能拥有参数。