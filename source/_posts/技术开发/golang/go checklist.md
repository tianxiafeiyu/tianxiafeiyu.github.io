---
title: go checklist
date: 2022-12-15 23:13:57
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - go checklist
---
# go checklist

## 2. 介绍
本文档参考开源(Urber)编码规范整理，记录 Go 代码中的惯用约定、规范，其中许多是 Go 语言的通用准则，期望通过引入业界最佳实践来提升团队编码能力，规范编码习惯，提高代码质量。

其他扩展准则依赖于下面外部的指南：

- Effective Go
- Go Common Mistakes
- Go Code Review Comments


## 3. 规范实施方法
本规范作为Go语言编码的基本规范和准则，是代码自检和检视的参考文档，配合各部门编码checklist，共同看护编码质量。
本规范中未标明非强制的规范和准则，均为强制规范/准则。


## 4. 工程要求
#### 4.1. IDE 中集成下述工具插件

- 提交代码时，必须使用 gofmt 工具格式化代码。注意，gofmt 不识别空行，因为 gofmt 不能理解空行的意义。
- 提交代码前，必须使用 goimports 工具检查导入。
- 提交代码时，必须使用 golint 工具检查代码规范。
- 提交代码前，必须使用 go vet 工具静态分析代码实现
- 
可以在以下 Go 编辑器工具支持页面中找到更为详细的信息：

https://github.com/golang/go/wiki/IDEsAndTextEditorPlugins

## 5. 规范
### 5.1. 基本约定
#### 5.1.1. 文件、函数大小约定
单行长度尽量限制为 99个 字符 。

单个文件长度尽量不超过 500 行。

单个函数长度尽量不超过 50 行。

单个函数圈复杂度尽量不超过 10，禁止超过 15。

单个函数中嵌套尽量不超过 3 层。

这不是硬性限制，但是超过此限制需要向reviewer做适当解释。

#### 5.1.2. 缩进、括号和空格约定
缩进、括号和空格都使用 gofmt 工具处理。

强制使用 tab 缩进。

强制左大括号不换行。

强制所有的运算符和操作数之间要留空格。

#### 5.1.3. 一致性
本文中概述的一些标准都是客观性的评估，是根据场景、上下文、或者主观性的判断；

但是最重要的是，保持一致.

一致性的代码更容易维护、是更合理的、需要更少的学习成本、并且随着新的约定出现或者出现错误后更容易迁移、更新、修复 bug

相反，在一个代码库中包含多个完全不同或冲突的代码风格会导致维护成本开销、不确定性和认知偏差。所有这些都会直接导致速度降低、代码审查痛苦、而且增加 bug 数量。

将这些标准应用于代码库时，建议在 package（或更大）级别进行更改，子包级别的应用程序通过将多个样式引入到同一代码中，违反了上述关注点。

### 5.2. 分组规范
#### 5.2.1. 相似的声明放在一组
Go 语言支持将相似的声明放在一个组内。
- Bad
```
import "a"
import "b"
```

- Good
```
import (
  "a"
  "b"
)
```
这同样适用于常量、变量和类型声明：
- Bad
```
const a = 1
const b = 2

var a = 1
var b = 2

type Area float64
type Volume float64
```

- Good
```
const (
  a = 1
  b = 2
)

var (
  a = 1
  b = 2
)

type (
  Area float64
  Volume float64
)
```
仅将相关的声明放在一组。不要将不相关的声明放在一组。
- Bad
```
type Operation int

const (
  Add Operation = iota + 1
  Subtract
  Multiply
  EnvVar = "MY_ENV"
)
```

- Good
```
type Operation int

const (
  Add Operation = iota + 1
  Subtract
  Multiply
)

const EnvVar = "MY_ENV"
```

分组使用的位置没有限制，例如：你可以在函数内部使用它们：
- Bad
```
func f() string {
  red := color.New(0xff0000)
  green := color.New(0x00ff00)
  blue := color.New(0x0000ff)

  ...
}
```

- Good
```
func f() string {
  var (
    red   = color.New(0xff0000)
    green = color.New(0x00ff00)
    blue  = color.New(0x0000ff)
  )

  ...
}
```

例外：如果变量声明与其他变量相邻，则应将变量声明（尤其是函数内部的声明）分组在一起。对一起声明的变量执行此操作，即使它们不相关。
- Bad
```
func (c *client) request() {
  caller := c.name
  format := "json"
  timeout := 5*time.Second
  var err error
  // ...
}
```
- Good
```
func (c *client) request() {
  var (
    caller  = c.name
    format  = "json"
    timeout = 5*time.Second
    err error
  )
  
  // ...
}
```

#### 5.2.2. import 分组规范
导入应该分为三组：

- 标准库
- 内部库
- 其他库

默认情况下，这是 goimports 应用的分组。
- Bad
```
import (
  "fmt"
  "os"
  "go.sangfor.org/cloudtech/resourcecenter"
  "golang.org/x/sync/errgroup"
)
```

- Good
```
import (
  "fmt"
  "os"


  "go.sangfor.org/cloudtech/resourcecenter"

  "go.uber.org/atomic"
  "golang.org/x/sync/errgroup"
)
```

#### 5.2.3. 函数分组与顺序
函数应按粗略的调用顺序排序。

同一文件中的函数应按接收者分组。

因此，导出的函数应先出现在文件中，放在struct, const, var定义的后面。

在定义类型之后，但在接收者的其余方法之前，可能会出现一个 newXYZ()/NewXYZ()

由于函数是按接收者分组的，因此普通工具函数应在文件末尾出现。
- Bad
```
func (s *something) Cost() {
  return calcCost(s.weights)
}

type something struct{ ... }

func calcCost(n []int) int {...}

func (s *something) Stop() {...}

func newSomething() *something {
    return &something{}
}
```
- Good
```
type something struct{ ... }

func newSomething() *something {
    return &something{}
}

func (s *something) Cost() {
  return calcCost(s.weights)
}

func (s *something) Stop() {...}

func calcCost(n []int) int {...}
```
### 5.3. 命名规范
#### 5.3.1. 包名
当命名包时，请按下面规则选择一个名称：

- 全部小写。没有大写或下划线。
- 大多数使用命名导入的情况下，不需要重命名。
- 简短而简洁。请记住，在每个使用的地方都完整标识了该名称。
- 不用复数。例如net/url，而不是net/urls。
- 不要用“common”，“util”，“shared”或“lib”。这些是不好的，信息量不足的名称。
- 另请参阅 Go 包命名规则 和 Go 包样式指南.

#### 5.3.2. 文件名
文件名为全小写单词，使用 “_” 分词。Golang 通常具有以下几种代码文件类型：
- 业务代码文件
- 模型代码文件
- 测试代码文件
- 工具代码文件

#### 5.3.3. 函数名
遵循 Go 社区关于使用 [MixedCaps 作为函数名] 的约定。

函数、方法（结构体或者接口下属的函数称为方法）命名规则： 动词 + 名词。

若函数、方法为判断类型（返回值主要为 bool 类型），则名称应以 Has、Is、Can 或 Allow 等判断性动词开头：
```
func HasPrefix(name string, prefixes []string) bool { ... }
func IsEntry(name string, entries []string) bool { ... }
func CanManage(name string) bool { ... }
func AllowGitHook() bool { ... }
```
有一个例外，为了对相关的测试用例进行分组，函数名可能包含下划线，如：TestMyFunction_WhatIsBeingTested.

[MixedCaps 作为函数名]: https://golang.org/doc/effective_go.html#mixed-caps

#### 5.3.4. 结构体、接口名
结构体命名规则：名词或名词短语。

接口命名规则：以 ”er” 作为后缀，例如：Reader、Writer。接口实现的方法则去掉 “er”，例如：Read、Write。
```
type Reader interface { Read(p []byte) (n int, err error)
}

// 多个函数接口
type WriteFlusher interface { Write([]byte) (int, error) Flush() error
}
```

#### 5.3.5. 变量、常量名
变量命名遵循驼峰法。

常量使用全大写单词，使用 “_” 分词。

首字母根据访问控制原则使用大写或者小写。

对于常规缩略语，一旦选择了大写或小写的风格，就应当在整份代码中保持这种风格，不要首字母大写和缩写两种风格混用。以 URL 为例，如果选择了缩写 URL 这种风格，则应在整份代码中保持。错误：UrlArray，正确：urlArray 或 URLArray。再以 ID 为例，如果选择了缩写 ID 这种风格，错误：appleId，正确：appleID。
对于只在本文件中有效的顶级变量、常量，应该使用 “_” 前缀，避免在同一个包中的其他文件中意外使用错误的值。例如：
```
var (
  _defaultPort = 8080
  _defaultUser = "user"
)
```

#### 5.3.6. 导入别名
如果程序包名称与导入路径的最后一个元素不匹配，则必须使用导入别名。
```
import (
  "net/http"

  client "example.com/client-go"
  trace "example.com/trace/v2"
)
```
在所有其他情况下，除非导入之间有直接冲突，否则应避免导入别名。
- Bad
```
import (
  "fmt"
  "os"

  nettrace "golang.net/x/trace"
)
```

- Good
```
import (
  "fmt"
  "os"
  "runtime/trace"

  nettrace "golang.net/x/trace"
)
```
### 5.4. 注释规范
Golang 的 go doc 工具可以根据注释生成代码文档，所以注释的质量决定了代码文档的质量。

【强制】所有新增代码文件需添加版权声明
```
/* Copyright @2022 Sangfor Technologies. All rights reserved. */
```

### 5.4.1. 注释风格
统一使用中文注释，中西文之间严格使用空格分隔，严格使用中文标点符号。

注释应当是一个完整的句子，以句号结尾。

句子类型的注释首字母均需大写，短语类型的注释首字母需小写。

注释的单行长度不能超过 99 个字符。

#### 5.4.2. 包注释
每个包都应该有一个包注释。包注释应该包含：
```
包名，简介。
创建者(使用团队名，个人名只在提交记录中体现，不在代码中体现)。
创建时间。
```
对于 main 包，通常只有一行简短的注释用以说明包的用途，且以项目名称开头：
```
// gormc(Go Resource Management Service) 是资源分配服务.
package main
```

对于简单的非 main 包，也可用一行注释概括。

对于一个复杂项目的子包，一般情况下不需要包级别注释，除非是代表某个特定功能的模块。

对于相对功能复杂的非 main 包，一般都会增加一些使用示例或基本说明，且以 Package 开头：


```
/* 包regexp 实现了一个简单的正则匹配库. 基本使用语法: regexp: concatenation { '|' concatenation } concatenation: { closure } closure: term [ '*' | '+' | '?' ] term: '^' '$' '.' character '[' [ '^' ] character-ranges ']' '(' regexp ')' */
package regexp
```
对于特别复杂的包说明，一般使用 doc.go

文件用于编写包的描述，并提供与整个包相关的信息。

#### 5.4.3. 函数、方法注释
每个函数、方法（结构体或者接口下属的函数称为方法）都应该有注释说明，包括三个方面（顺序严格）：
- 函数、方法名，简要说明。
- 参数列表，每行一个参数。
- 返回值，每行一个返回值。
```
// NewtAttrModel，属性数据层操作类的工厂方法。
// 参数：
// ctx：上下文信息。
// 返回值：
// 属性操作类指针。
func NewAttrModel(ctx *common.Context) *AttrModel {}
```
如果一句话不足以说明全部问题，则可换行继续进行更加细致的描述：
```
// 复制函数将文件从源地址复制到目的地址.
// 失败场景下返回false或error.
```
若函数或方法为判断类型（返回值主要为 bool 类型），则注释以<函数名> returns true if 开头：
```
// HasPrefix 返回 true，如果输入的name参数包含指定的prefix.
func HasPrefix(name string, prefixes []string) bool { ...
```

#### 5.4.4. 结构体、接口注释
每个自定义的结构体、接口都应该有注释说明，放在实体定义的前一行，格式为：名称、说明。同时，结构体内的每个成员都要有说明，该说明放在成员变量的后面（注意对齐），例如：
```
// User，用户实例，定义了用户的基础信息。
type User struct{ 
  Username  string  // 用户名 
  Email string  // 邮箱
}
```

#### 5.4.5. 其它说明
当某个部分等待完成时，用 TODO(Your name): 开头的注释来提醒维护人员。

当某个部分存在已知问题进行需要修复或改进时，用 FIXME(Your name): 开头的注释来提醒维护人员。

当需要特别说明某个问题时，可用 NOTE(You name): 开头的注释。


### 5.5. 单元测试规范
#### 5.5.1. 测试命名和提交规范
单元测试都必须使用 GoConvey 编写，且覆盖率必须在 80% 以上。

业务代码文件和单元测试文件放在同一目录下。

单元测试文件名以 *_test.go 为后缀，例如：example_test.go。

测试用例的函数名称必须以 Test 开头，例如：Test_Logger。

如果为结构体的方法编写测试用例，则需要以 Text__的形式命名，例如：Test_Macaron_Run。

每个重要的函数都要同步编写测试用例。

测试用例和业务代码同步提交，方便进行回归测试。

#### 5.5.2. 表驱动测试
当测试逻辑是重复的时候，通过 subtests 使用 table 驱动的方式编写 case 代码看上去会更简洁。

- Bad
```
// func TestSplitHostPort(t *testing.T)

host, port, err := net.SplitHostPort("192.0.2.0:8000")
require.NoError(t, err)
assert.Equal(t, "192.0.2.0", host)
assert.Equal(t, "8000", port)

host, port, err = net.SplitHostPort("192.0.2.0:http")
require.NoError(t, err)
assert.Equal(t, "192.0.2.0", host)
assert.Equal(t, "http", port)

host, port, err = net.SplitHostPort(":8000")
require.NoError(t, err)
assert.Equal(t, "", host)
assert.Equal(t, "8000", port)

host, port, err = net.SplitHostPort("1:8")
require.NoError(t, err)
assert.Equal(t, "1", host)
assert.Equal(t, "8", port)
```
- Good
```
// func TestSplitHostPort(t *testing.T)

tests := []struct{
  give     string
  wantHost string
  wantPort string
}{
  {
    give:     "192.0.2.0:8000",
    wantHost: "192.0.2.0",
    wantPort: "8000",
  },
  {
    give:     "192.0.2.0:http",
    wantHost: "192.0.2.0",
    wantPort: "http",
  },
  {
    give:     ":8000",
    wantHost: "",
    wantPort: "8000",
  },
  {
    give:     "1:8",
    wantHost: "1",
    wantPort: "8",
  },
}

for _, tt := range tests {
  t.Run(tt.give, func(t *testing.T) {
    host, port, err := net.SplitHostPort(tt.give)
    require.NoError(t, err)
    assert.Equal(t, tt.wantHost, host)
    assert.Equal(t, tt.wantPort, port)
  })
}
```
很明显，使用 test table 的方式在代码逻辑扩展的时候，比如新增 test case，都会显得更加的清晰。

我们遵循这样的约定：将结构体切片称为tests。 每个测试用例称为tt。此外，我们鼓励使用give和want前缀说明每个测试用例的输入和输出值。
```
tests := []struct{
  give     string
  wantHost string
  wantPort string
}{
  // ...
}

for _, tt := range tests {
  // ...
}
```

### 5.6. 代码逻辑规范
#### 5.6.1. 变量声明规范
##### 5.6.1.1. 顶层变量声明规范
在顶层，使用标准var关键字。请勿指定类型，除非它与表达式的类型不同。

- Bad
```
var _s string = F()

func F() string { return "A" }
```

- Good
```
var _s = F()
// 由于 F 已经明确了返回一个字符串类型，因此我们没有必要显式指定_s 的类型
// 还是那种类型

func F() string { return "A" }
```
如果表达式的类型与所需的类型不完全匹配，请指定类型。
```
type myError struct{}

func (myError) Error() string { return "error" }

func F() myError { return myError{} }

var _e error = F()
// F 返回一个 myError 类型的实例，但是我们要 error 类型
```

##### 5.6.1.2. 未导出的顶层常量和变量，使用_作为前缀
在未导出的顶级vars和consts， 前面加上前缀_，以使它们在使用时明确表示它们是全局符号。

例外：未导出的错误值，应以err开头。

基本依据：顶级变量和常量具有包范围作用域。使用通用名称可能很容易在其他文件中意外使用错误的值。

- Bad
```
// foo.go

const (
  defaultPort = 8080
  defaultUser = "user"
)

// bar.go

func Bar() {
  defaultPort := 9090
  ...
  fmt.Println("Default port", defaultPort)

  // We will not see a compile error if the first line of
  // Bar() is deleted.
}
```

- Good
```
// foo.go

const (
  _defaultPort = 8080
  _defaultUser = "user"
)
```
Exception:未导出的错误值可以使用不带下划线的前缀 err。 参见错误命名。

##### 5.6.1.3. 本地变量声明
如果将变量明确设置为某个值，则应使用短变量声明形式 (:=)。
```
var s = "foo"
s := "foo"
```
但是，在某些情况下，var 使用关键字时默认值会更清晰。例如，声明空切片。

- Bad
```
func f(list []int) {
  filtered := []int{}
  for _, v := range list {
    if v > 10 {
      filtered = append(filtered, v)
    }
  }
}
```

- Good
```
func f(list []int) {
  var filtered []int
  for _, v := range list {
    if v > 10 {
      filtered = append(filtered, v)
    }
  }
}
```

##### 5.6.1.4. 缩小变量作用域
如果有可能，尽量缩小变量作用范围。除非它与 减少嵌套的规则冲突。
- Bad
```
err := ioutil.WriteFile(name, data, 0644)
if err != nil {
 return err
}
```
- Good
```
if err := ioutil.WriteFile(name, data, 0644); err != nil {
 return err
}
```
如果需要在 if 之外使用函数调用的结果，则不应尝试缩小范围。
- Bad
```
if data, err := ioutil.ReadFile(name); err == nil {
  err = cfg.Decode(data)
  if err != nil {
    return err
  }

  fmt.Println(cfg)
  return nil
} else {
  return err
}
```
- Good
```
data, err := ioutil.ReadFile(name)
if err != nil {
   return err
}

if err := cfg.Decode(data); err != nil {
  return err
}

fmt.Println(cfg)
return nil
```

#### 5.6.2. 函数定义规范
### 5.6.2.1. 避免参数语义不明确 (Avoid Naked Parameters)
函数调用中的意义不明确的参数可能会损害可读性。当参数名称的含义不明显时，请为参数添加 C 样式注释 (`/* ... */`)
- Bad
```
// func printInfo(name string, isLocal, done bool)

printInfo("foo", true, true)
```
- Good
```
// func printInfo(name string, isLocal, done bool)

printInfo("foo", true /* isLocal */, true /* done */)
```
对于上面的示例代码，还有一种更好的处理方式是将上面的 bool 类型换成自定义类型。将来，该参数可以支持不仅仅局限于两个状态（true/false）。
```
type Region int

const (
  UnknownRegion Region = iota
  Local
)

type Status int

const (
  StatusReady Status= iota + 1
  StatusDone
  // Maybe we will have a StatusInProgress in the future.
)

func printInfo(name string, region Region, status Status)
```

##### 5.6.2.2. 避免使用 init()
尽可能避免使用init()。当init()是不可避免或可取的，代码应先尝试：

无论程序环境或调用如何，都要完全确定。

避免依赖于其他init()函数的顺序或副作用。虽然init()顺序是明确的，但代码可以更改，因此init()函数之间的关系可能会使代码变得脆弱和容易出错。

避免访问或操作全局或环境状态，如机器信息、环境变量、工作目录、程序参数/输入等。

避免I/O，包括文件系统、网络和系统调用。

不能满足这些要求的代码可能属于要作为main()调用的一部分（或程序生命周期中的其他地方），
或者作为main()本身的一部分写入。特别是，打算由其他程序使用的库应该特别注意完全确定性，
而不是执行“init magic”。

- Bad
```
type Foo struct {
    // ...
}
var _defaultFoo Foo
func init() {
    _defaultFoo = Foo{
        // ...
    }
}
```
- Good
```
var _defaultFoo = Foo{
    // ...
}
// or，为了更好的可测试性：
var _defaultFoo = defaultFoo()
func defaultFoo() Foo {
    return Foo{
        // ...
    }
}
```
- Bad
```
type Config struct {
    // ...
}
var _config Config
func init() {
    // Bad: 基于当前目录
    cwd, _ := os.Getwd()
    // Bad: I/O
    raw, _ := ioutil.ReadFile(
        path.Join(cwd, "config", "config.yaml"),
    )
    yaml.Unmarshal(raw, &_config)
}
```
- Good
```
type Config struct {
    // ...
}
func loadConfig() Config {
    cwd, err := os.Getwd()
    // handle err
    raw, err := ioutil.ReadFile(
        path.Join(cwd, "config", "config.yaml"),
    )
    // handle err
    var config Config
    yaml.Unmarshal(raw, &config)
    return config
}
```
考虑到上述情况，在某些情况下，init()可能更可取或是必要的，可能包括：

- 不能表示为单个赋值的复杂表达式。

- 可插入的钩子，如database/sql、编码类型注册表等。

- 对 Google Cloud Functions 和其他形式的确定性预计算的优化。

#### 5.6.3. 结构体类型定义规范
##### 5.6.3.1. 使用字段名初始化结构
初始化结构时，几乎应该始终指定字段名。目前由 go vet 强制执行。
- Bad
```
k := User{"John", "Doe", true}
```

- Good
```
k := User{
    FirstName: "John",
    LastName: "Doe",
    Admin: true,
}
```
例外：当有 3 个或更少的字段时，测试表中的字段名may可以省略。
```
tests := []struct{
  op Operation
  want string
}{
  {Add, "add"},
  {Subtract, "subtract"},
}
```

##### 5.6.3.2. 省略结构中的零值字段
初始化具有字段名的结构时，除非提供有意义的上下文，否则忽略值为零值的字段。
也就是，让我们自动将这些设置为零值
- Bad
``` 
user := User{
  FirstName: "John",
  LastName: "Doe",
  MiddleName: "",
  Admin: false,
}
```
- Good
```
user := User{
  FirstName: "John",
  LastName: "Doe",
}
```
这有助于通过省略该上下文中的默认值来减少阅读的障碍。只指定有意义的值。

在字段名提供有意义上下文的地方包含零值。例如，表驱动测试 中的测试用例可以指定全部字段的名称，即使它们是零值的。
```
tests := []struct{
  give string
  want int
}{
  {give: "0", want: 0},
  // ...
}
```

##### 5.6.3.3. 对零值结构使用 var
如果在声明中省略了结构的所有字段，请使用 var 声明结构。
- Bad
```
user := User{}
```

- Good
```
var user User
```
这将零值结构与那些具有类似于为 初始化 Maps 创建的，区别于非零值字段的结构区分开来，
并与我们更喜欢的 声明空切片 方式相匹配。

##### 5.6.3.4. 初始化 Struct 引用
在初始化结构引用时，请使用&T{}代替new(T)，以使其与结构体初始化一致。
- Bad
```
sval := T{Name: "foo"}

// inconsistent
sptr := new(T)
sptr.Name = "bar"
```
- Good
```
sval := T{Name: "foo"}

sptr := &T{Name: "bar"}
```

##### 5.6.3.5. 结构体中的嵌入
嵌入式类型（例如 mutex）应位于结构体内的字段列表的顶部，并且必须有一个空行将嵌入式字段与常规字段分隔开。
- Bad
```
type Client struct {
  version int
  http.Client
}
```
- Good
```
type Client struct {
  http.Client

  version int
}
```
内嵌应该提供切实的好处，比如以语义上合适的方式添加或增强功能。

它应该在对用户没有任何不利影响的情况下使用。（另请参见：避免在公共结构中嵌入类型）。

例外：即使在未导出类型中，Mutex 也不应该作为内嵌字段。另请参见：零值 Mutex 是有效的。

嵌入 不应该:
- 纯粹是为了美观或方便。
- 使外部类型更难构造或使用。
- 影响外部类型的零值。如果外部类型有一个有用的零值，则在嵌入内部类型之后应该仍然有一个有用的零值。
- 作为嵌入内部类型的副作用，从外部类型公开不相关的函数或字段。
- 公开未导出的类型。
- 影响外部类型的复制形式。
- 更改外部类型的 API 或类型语义。
- 嵌入内部类型的非规范形式。
- 公开外部类型的实现详细信息。
- 允许用户观察或控制类型内部。
- 通过包装的方式改变内部函数的一般行为，这种包装方式会给用户带来一些意料之外情况。

简单地说，有意识地和有目的地嵌入。
一种很好的测试体验是，"是否所有这些导出的内部方法/字段都将直接添加到外部类型？"，
如果答案是some或no，不要嵌入内部类型，而是使用字段。

- Bad
```
type A struct {
    // Bad: A.Lock() and A.Unlock() 现在可用
    // 不提供任何功能性好处，并允许用户控制有关 A 的内部细节。
    sync.Mutex
}


type Book struct {
    // Bad: 指针更改零值的有用性
    io.ReadWriter
    // other fields
}
// later
var b Book
b.Read(...)  // panic: nil pointer
b.String()   // panic: nil pointer
b.Write(...) // panic: nil pointer


type Client struct {
    sync.Mutex
    sync.WaitGroup
    bytes.Buffer
    url.URL
}
```

- Good
```
type countingWriteCloser struct {
    // Good: Write() 在外层提供用于特定目的，
    // 并且委托工作到内部类型的 Write() 中。
    io.WriteCloser
    count int
}
func (w *countingWriteCloser) Write(bs []byte) (int, error) {
    w.count += len(bs)
    return w.WriteCloser.Write(bs)
}


type Book struct {
    // Good: 有用的零值
    bytes.Buffer
    // other fields
}
// later
var b Book
b.Read(...)  // ok
b.String()   // ok
b.Write(...) // ok


type Client struct {
    mtx sync.Mutex
    wg  sync.WaitGroup
    buf bytes.Buffer
    url url.URL
}
```
#### 5.6.4. 接口定义规范
您几乎不需要指向接口类型的指针。您应该将接口作为值进行传递，在这样的传递过程中，实质上传递的底层数据仍然可以是指针。

接口实质上在底层用两个字段表示：
- 一个指向某些特定类型信息的指针。您可以将其视为"type"。
- 数据指针。如果存储的数据是指针，则直接存储。如果存储的数据是一个值，则存储指向该值的指针。

如果希望接口方法修改基础数据，则必须使用指针传递 (将对象指针赋值给接口变量)。
```
type F interface {
  f()
}

type S1 struct{}

func (s S1) f() {}

type S2 struct{}

func (s *S2) f() {}

// f1.f() 无法修改底层数据
// f2.f() 可以修改底层数据，给接口变量 f2 赋值时使用的是对象指针
var f1 F = S1{}
var f2 F = &S2{}
```

#### 5.6.5. Map/Slice 类型定义规范
##### 5.6.5.1. Map 类型定义规范
对于空 map 请使用 make(..) 初始化， 并且 map 是通过编程方式填充的。

这使得 map 初始化在表现上不同于声明，并且它还可以方便地在 make 后添加大小提示。
- Bad
```
var (
  // m1 读写安全;
  // m2 在写入时会 panic
  m1 = map[T1]T2{}
  m2 map[T1]T2
)
// 声明和初始化看起来非常相似的。
```

- Good
```
var (
  // m1 读写安全;
  // m2 在写入时会 panic
  m1 = make(map[T1]T2)
  m2 map[T1]T2
)
// 声明和初始化看起来差别非常大。
```

在尽可能的情况下，请在初始化时提供 map 容量大小，详细请看 指定 Map 容量提示。

另外，如果 map 包含固定的元素列表，则使用 map literals(map 初始化列表) 初始化映射。
- Bad
```
m := make(map[T1]T2, 3)
m[k1] = v1
m[k2] = v2
m[k3] = v3
```
- Good
```
m := map[T1]T2{
  k1: v1,
  k2: v2,
  k3: v3,
}
```
基本准则是：在初始化时使用 map 初始化列表 来添加一组固定的元素。否则使用 make (如果可以，请尽量指定 map 容量)。

##### 5.6.5.2. nil 是一个有效的 slice
nil 是一个有效的长度为 0 的 slice，这意味着，

1) 您不应明确返回长度为零的切片。应该返回nil 来代替。
- Bad
```
if x == "" {
  return []int{}
}
```
- Good
```
if x == "" {
  return nil
}
```
2) 要检查切片是否为空，请始终使用len(s) == 0。而非 nil。
- Bad
```
func isEmpty(s []string) bool {
  return s == nil
}
```
- Good
```
func isEmpty(s []string) bool {
  return len(s) == 0
}
```
3) 零值切片（用var声明的切片）可立即使用，无需调用make()创建。
- Bad
```
nums := []int{}
// or, nums := make([]int)

if add1 {
  nums = append(nums, 1)
}

if add2 {
  nums = append(nums, 2)
}
```
- Good
```
var nums []int

if add1 {
  nums = append(nums, 1)
}

if add2 {
  nums = append(nums, 2)
}
```
记住，虽然 nil 切片是有效的切片，但它不等于长度为 0 的切片（一个为 nil，另一个不是），并且在不同的情况下（例如序列化），这两个切片的处理方式可能不同。

#### 5.6.6. 字符串类型定义规范
##### 5.6.6.1. 声明 Printf-style String 时，将其设置为 const 常量
在函数外声明Printf-style 函数的格式字符串，请将其设置为const常量。

这有助于go vet对格式字符串执行静态分析。
- Bad
```
msg := "unexpected values %v, %v\n"
fmt.Printf(msg, 1, 2)
```
- Good
```
const msg = "unexpected values %v, %v\n"
fmt.Printf(msg, 1, 2)
```
##### 5.6.6.2. 使用原始字符串字符，避免转义
Go 支持使用 原始字符串字符，也就是 " ` " 来表示原生字符串，在需要转义的场景下，我们应该尽量使用这种方案来替换。

可以跨越多行并包含引号。使用这些字符串可以避免更难阅读的手工转义的字符串。
- Bad
```
wantError := "unknown name:\"test\""
```
- Good
```
wantError := `unknown error:"test"`
```
#### 5.6.6.3. 命名 Printf 样式的函数
声明Printf-style 函数时，请确保go vet可以检测到它并检查格式字符串。

这意味着您应尽可能使用预定义的Printf-style 函数名称。go vet将默认检查这些。有关更多信息，请参见 Printf 系列。

如果不能使用预定义的名称，请以 f 结束选择的名称：Wrapf，而不是Wrap。go vet可以要求检查特定的 Printf 样式名称，但名称必须以f结尾。

$ go vet -printfuncs=wrapf,statusf
另请参阅 go vet: Printf family check.

## 6. 指导原则
### 6.1. 减少嵌套
代码应通过尽可能先处理错误情况/特殊情况并尽早返回或继续循环来减少嵌套（不超过3 层嵌套）。减少嵌套多个级别的代码的代码量。
- Bad
```
for _, v := range data {
  if v.F1 == 1 {
    v = process(v)
    if err := v.Call(); err == nil {
      v.Send()
    } else {
      return err
    }
  } else {
    log.Printf("Invalid v: %v", v)
  }
}
```
- Good
```
for _, v := range data {
  if v.F1 != 1 {
    log.Printf("Invalid v: %v", v)
    continue
  }

  v = process(v)
  if err := v.Call(); err != nil {
    return err
  }
  v.Send()
}
```

### 6.2. 替换不必要的 else
如果在 if 的两个分支中都设置了变量，则可以将其替换为单个 if。

- Bad
```
var a int
if b {
  a = 100
} else {
  a = 10
}
```
- Good
```
a := 10
if b {
  a = 100
}
```

### 6.3. Interface 合理性验证
在编译时验证接口的符合性。这包括：

- 将实现特定接口的导出类型作为接口 API 的一部分进行检查
- 实现同一接口的 (导出和非导出) 类型属于实现类型的集合
- 任何违反接口合理性检查的场景，都会终止编译，并通知给用户

补充：上面 3 条是编译器对接口的检查机制，
大体意思是错误使用接口会在编译期报错。
所以可以利用这个机制让部分问题在编译期暴露。

- Bad
```
// 如果 Handler 没有实现 http.Handler，会在运行时报错
type Handler struct {
  // ...
}
func (h *Handler) ServeHTTP(
  w http.ResponseWriter,
  r *http.Request,
) {
  ...
}
```
- Good
```
type Handler struct {
  // ...
}
// 用于触发编译期的接口的合理性检查机制
// 如果 Handler 没有实现 http.Handler，会在编译期报错
var _ http.Handler = (*Handler)(nil)
func (h *Handler) ServeHTTP(
  w http.ResponseWriter,
  r *http.Request,
) {
  // ...
}
```
如果 *Handler 与 http.Handler 的接口不匹配，
那么语句 var _ http.Handler = (*Handler)(nil) 将无法编译通过。

赋值的右边应该是断言类型的零值。
对于指针类型（如 *Handler）、切片和映射，这是 nil；
对于结构类型，这是空结构。
```
type LogHandler struct {
  h   http.Handler
  log *zap.Logger
}
var _ http.Handler = LogHandler{}
func (h LogHandler) ServeHTTP(
  w http.ResponseWriter,
  r *http.Request,
) {
  // ...
}
```

### 6.4. 接收器 (receiver) 与接口
使用值接收器的方法既可以通过值调用，也可以通过指针调用。

带指针接收器的方法只能通过指针或 addressable values 调用。

例如：

```
type S struct {
  data string
}

func (s S) Read() string {
  return s.data
}

func (s *S) Write(str string) {
  s.data = str
}

sVals := map[int]S{1: {"A"}}

// 你只能通过值调用 Read
sVals[1].Read()

// 这不能编译通过：
// sVals[1].Write("test")

sPtrs := map[int]*S{1: {"A"}}

// 通过指针既可以调用 Read，也可以调用 Write 方法
sPtrs[1].Read()
sPtrs[1].Write("test")
```
类似的，即使方法有了值接收器，也同样可以用指针接收器来满足接口。
```
type F interface {
  f()
}

type S1 struct{}

func (s S1) f() {}

type S2 struct{}

func (s *S2) f() {}

s1Val := S1{}
s1Ptr := &S1{}
s2Val := S2{}
s2Ptr := &S2{}

var i F
i = s1Val
i = s1Ptr
i = s2Ptr

// 下面代码无法通过编译。因为 s2Val 是一个值，而 S2 的 f 方法中没有使用值接收器
// i = s2Val
```

Effective Go 中有一段关于 pointers vs. values 的精彩讲解。

补充：

- 一个类型可以有值接收器方法集和指针接收器方法集
    - 值接收器方法集是指针接收器方法集的子集，反之不是
- 规则
    - 值对象只可以使用值接收器方法集
    - 指针对象可以使用 值接收器方法集 + 指针接收器方法集
- 接口的匹配 (或者叫实现)
    - 类型实现了接口的所有方法，叫匹配
    - 具体的讲，要么是类型的值方法集匹配接口，要么是指针方法集匹配接口

具体的匹配分两种：

- 值方法集和接口匹配
    - 给接口变量赋值的不管是值还是指针对象，都 ok，因为都包含值方法集
- 指针方法集和接口匹配
    - 只能将指针对象赋值给接口变量，因为只有指针方法集和接口匹配
    - 如果将值对象赋值给接口变量，会在编译期报错 (会触发接口合理性检查机制)

为啥 i = s2Val 会报错，因为值方法集和接口不匹配。

### 6.5. 零值 Mutex 是有效的
零值 sync.Mutex 和 sync.RWMutex 是有效的。所以指向 mutex 的指针基本是不必要的。
- Bad
```
mu := new(sync.Mutex)
mu.Lock()
```
- Good
```
var mu sync.Mutex
mu.Lock()
```
如果你使用结构体指针，mutex 应该作为结构体的非指针字段。即使该结构体不被导出，也不要直接把 mutex 嵌入到结构体中。
- Bad
```
type SMap struct {
  sync.Mutex

  data map[string]string
}

func NewSMap() *SMap {
  return &SMap{
    data: make(map[string]string),
  }
}

func (m *SMap) Get(k string) string {
  m.Lock()
  defer m.Unlock()

  return m.data[k]
}

// Mutex 字段， Lock 和 Unlock 方法是 SMap 导出的 API 中不刻意说明的一部分。
```

- Good
```
type SMap struct {
  mu sync.Mutex

  data map[string]string
}

func NewSMap() *SMap {
  return &SMap{
    data: make(map[string]string),
  }
}

func (m *SMap) Get(k string) string {
  m.mu.Lock()
  defer m.mu.Unlock()

  return m.data[k]
}

// mutex 及其方法是 SMap 的实现细节，对其调用者不可见。
```

### 6.6. 在边界处拷贝 Slices 和 Maps
slices 和 maps 包含了指向底层数据的指针，因此在需要复制它们时要特别注意。

#### 6.6.1. 接收 Slices 和 Maps
请记住，当 map 或 slice 作为函数参数传入时，如果您存储了对它们的引用，则用户可以对其进行修改。
- Bad
```
func (d *Driver) SetTrips(trips []Trip) {
  d.trips = trips
}

trips := ...
d1.SetTrips(trips)

// 你是要修改 d1.trips 吗？
trips[0] = ...
```
- Good
```
func (d *Driver) SetTrips(trips []Trip) {
  d.trips = make([]Trip, len(trips))
  copy(d.trips, trips)
}

trips := ...
d1.SetTrips(trips)

// 这里我们修改 trips[0]，但不会影响到 d1.trips
trips[0] = ...
```

#### 6.6.2. 返回 slices 或 maps
同样，请注意用户对暴露内部状态的 map 或 slice 的修改。
- Bad
```
type Stats struct {
  mu sync.Mutex

  counters map[string]int
}

// Snapshot 返回当前状态。
func (s *Stats) Snapshot() map[string]int {
  s.mu.Lock()
  defer s.mu.Unlock()

  return s.counters
}

// snapshot 不再受互斥锁保护
// 因此对 snapshot 的任何访问都将受到数据竞争的影响
// 影响 stats.counters
snapshot := stats.Snapshot()
```
- Good
```
type Stats struct {
  mu sync.Mutex

  counters map[string]int
}

func (s *Stats) Snapshot() map[string]int {
  s.mu.Lock()
  defer s.mu.Unlock()

  result := make(map[string]int, len(s.counters))
  for k, v := range s.counters {
    result[k] = v
  }
  return result
}

// snapshot 现在是一个拷贝
snapshot := stats.Snapshot()
```

### 6.7. 使用 defer 释放资源
使用 defer 释放资源，诸如文件和锁。
- Bad
```
p.Lock()
if p.count < 10 {
  p.Unlock()
  return p.count
}

p.count++
newCount := p.count
p.Unlock()

return newCount

// 当有多个 return 分支时，很容易遗忘 unlock
```
- Good
```
p.Lock()
defer p.Unlock()

if p.count < 10 {
  return p.count
}

p.count++
return p.count

// 更可读
```
Defer 的开销非常小，只有在您可以证明函数执行时间处于纳秒级的程度时，才应避免这样做。使用 defer 提升可读性是值得的，因为使用它们的成本微不足道。尤其适用于那些不仅仅是简单内存访问的较大的方法，在这些方法中其他计算的资源消耗远超过 defer。

### 6.8. Channel 的 size 要么是 1，要么是无缓冲的
channel 通常 size 应为 1 或是无缓冲的。默认情况下，channel 是无缓冲的，其 size 为零。任何其他尺寸都必须经过严格的审查。我们需要考虑如何确定大小，考虑是什么阻止了 channel 在高负载下和阻塞写时的写入，以及当这种情况发生时系统逻辑有哪些变化。(翻译解释：按照原文意思是需要界定通道边界，竞态条件，以及逻辑上下文梳理)
- Bad
```
// 应该足以满足任何情况！
c := make(chan int, 64)
```
- Good
```
// 大小：1
c := make(chan int, 1) // 或者
// 无缓冲 channel，大小为 0
c := make(chan int)
```

### 6.9. 枚举从 1 开始
在 Go 中引入枚举的标准方法是声明一个自定义类型和一个使用了 iota 的 const 组。由于变量的默认值为 0，因此通常应以非零值开头枚举。
- Bad
```
type Operation int

const (
  Add Operation = iota
  Subtract
  Multiply
)

// Add=0, Subtract=1, Multiply=2
```
- Good
```
type Operation int

const (
  Add Operation = iota + 1
  Subtract
  Multiply
)

// Add=1, Subtract=2, Multiply=3
```
在某些情况下，使用零值是有意义的（枚举从零开始），例如，当零值是理想的默认行为时。
```
type LogOutput int

const (
  LogToStdout LogOutput = iota
  LogToFile
  LogToRemote
)

// LogToStdout=0, LogToFile=1, LogToRemote=2
```

### 6.10. 使用 time 处理时间
时间处理很复杂。关于时间的错误假设通常包括以下几点。

- 一天有 24 小时
- 一小时有 60 分钟
- 一周有七天
- 一年 365 天
- 还有更多

例如，1 表示在一个时间点上加上 24 小时并不总是产生一个新的日历日。

因此，在处理时间时始终使用 "time" 包，因为它有助于以更安全、更准确的方式处理这些不正确的假设。

#### 6.10.1. 使用 time.Time 表达瞬时时间
在处理时间的瞬间时使用 time.Time，在比较、添加或减去时间时使用 time.Time 中的方法。
- Bad
```
func isActive(now, start, stop int) bool {
  return start <= now && now < stop
}
```
- Good
```
func isActive(now, start, stop time.Time) bool {
  return (start.Before(now) || start.Equal(now)) && now.Before(stop)
}
```

#### 6.10.2. 使用 time.Duration 表达时间段
在处理时间段时使用 time.Duration .
- Bad
```
func poll(delay int) {
  for {
    // ...
    time.Sleep(time.Duration(delay) * time.Millisecond)
  }
}
poll(10) // 是几秒钟还是几毫秒？
```
- Good
```
func poll(delay time.Duration) {
  for {
    // ...
    time.Sleep(delay)
  }
}
poll(10*time.Second)
```
回到第一个例子，在一个时间瞬间加上 24 小时，我们用于添加时间的方法取决于意图。如果我们想要下一个日历日 (当前天的下一天) 的同一个时间点，我们应该使用 Time.AddDate。但是，如果我们想保证某一时刻比前一时刻晚 24 小时，我们应该使用 Time.Add。
```
newDay := t.AddDate(0 /* years */, 0 /* months */, 1 /* days */)
maybeNewDay := t.Add(24 * time.Hour)
```

#### 6.10.3. 对外部系统使用 time.Time 和 time.Duration
尽可能在与外部系统的交互中使用 time.Duration 和 time.Time 例如 :

- Command-line 标志: flag 通过 time.ParseDuration 支持 time.Duration
- 
- JSON: encoding/json 通过其 UnmarshalJSON method 方法支持将 time.Time 编码为 RFC 3339 字符串
- 
- SQL: database/sql 支持将 DATETIME 或 TIMESTAMP 列转换为 time.Time，如果底层驱动程序支持则返回
- 
- YAML: gopkg.in/yaml.v2 支持将 time.Time 作为 RFC 3339 字符串，并通过 time.ParseDuration 支持 time.Duration。

当不能在这些交互中使用 time.Duration 时，请使用 int 或 float64，并在字段名称中包含单位。

例如，由于 encoding/json 不支持 time.Duration，因此该单位包含在字段的名称中。
- Bad
```
// {"interval": 2}
type Config struct {
  Interval int `json:"interval"`
}
```
- Good
```
// {"intervalMillis": 2000}
type Config struct {
  IntervalMillis int `json:"intervalMillis"`
}
```
当在这些交互中不能使用 time.Time 时，除非达成一致，否则使用 string 和 RFC 3339 中定义的格式时间戳。默认情况下，Time.UnmarshalText 使用此格式，并可通过 time.RFC3339 在 Time.Format 和 time.Parse 中使用。

尽管这在实践中并不成问题，但请记住，"time" 包不支持解析闰秒时间戳（8728），也不在计算中考虑闰秒（15190）。如果您比较两个时间瞬间，则差异将不包括这两个瞬间之间可能发生的闰秒。

### 6.11. Errors
#### 6.11.1. 错误类型
声明错误的选项很少。

在选择最适合您的用例的选项之前，请考虑以下事项。

- 调用者是否需要匹配错误以便他们可以处理它？  
  如果是，我们必须通过声明顶级错误变量或自定义类型来支持 errors.Is 或 errors.As 函数。

- 错误消息是否为静态字符串，还是需要上下文信息的动态字符串？   
  如果是静态字符串，我们可以使用 errors.New，但对于后者，我们必须使用 fmt.Errorf 或自定义错误类型。

- 我们是否正在传递由下游函数返回的新错误？  
  如果是这样，请参阅错误包装部分。

错误匹配？|错误消息|指导
-- | -- | --
No |static	| errors.New
No |dynamic	| fmt.Errorf
Yes |static	| top-level var with errors.New
Yes |dynamic| custom error type

例如，
使用 errors.New 表示带有静态字符串的错误。
如果调用者需要匹配并处理此错误，则将此错误导出为变量以支持将其与 errors.Is 匹配。
- 无错误匹配
```
// package foo

func Open() error {
  return errors.New("could not open")
}

// package bar

if err := foo.Open(); err != nil {
  // Can't handle the error.
  panic("unknown error")
}
```
- 错误匹配
```
// package foo

var ErrCouldNotOpen = errors.New("could not open")

func Open() error {
  return ErrCouldNotOpen
}

// package bar

if err := foo.Open(); err != nil {
  if errors.Is(err, foo.ErrCouldNotOpen) {
    // handle the error
  } else {
    panic("unknown error")
  }
}
```
对于动态字符串的错误，
如果调用者不需要匹配它，则使用 fmt.Errorf，
如果调用者确实需要匹配它，则自定义 error。
- 无错误匹配
```
// package foo

func Open(file string) error {
  return fmt.Errorf("file %q not found", file)
}

// package bar

if err := foo.Open("testfile.txt"); err != nil {
  // Can't handle the error.
  panic("unknown error")
}
```
- 错误匹配
```
// package foo

type NotFoundError struct {
  File string
}

func (e *NotFoundError) Error() string {
  return fmt.Sprintf("file %q not found", e.File)
}

func Open(file string) error {
  return &NotFoundError{File: file}
}


// package bar

if err := foo.Open("testfile.txt"); err != nil {
  var notFound *NotFoundError
  if errors.As(err, &notFound) {
    // handle the error
  } else {
    panic("unknown error")
  }
}
```
请注意，如果您从包中导出错误变量或类型，
它们将成为包的公共 API 的一部分。

#### 6.11.2. 错误包装
如果调用失败，有三种主要的错误调用选项：

- 按原样返回原始错误
- add context with fmt.Errorf and the %w verb
- 使用fmt.Errorf和%w
- 使用 fmt.Errorf 和 %v

如果没有要添加的其他上下文，则按原样返回原始错误。  
这将保留原始错误类型和消息。  
这非常适合底层错误消息有足够的信息来追踪它来自哪里的错误。  

否则，尽可能在错误消息中添加上下文  
这样就不会出现诸如“连接被拒绝”之类的模糊错误，  
您会收到更多有用的错误，例如“呼叫服务 foo：连接被拒绝”。  

使用 fmt.Errorf 为你的错误添加上下文，  
根据调用者是否应该能够匹配和提取根本原因，在 %w 或 %v 动词之间进行选择。  

- 如果调用者应该可以访问底层错误，请使用 %w。  
  对于大多数包装错误，这是一个很好的默认值，  
  但请注意，调用者可能会开始依赖此行为。因此，对于包装错误是已知var或类型的情况，请将其作为函数契约的一部分进行记录和测试。
- 使用 %v 来混淆底层错误。  
  调用者将无法匹配它，但如果需要，您可以在将来切换到 %w。  
  在为返回的错误添加上下文时，通过避免使用"failed to"之类的短语来保持上下文简洁，当错误通过堆栈向上渗透时，它会一层一层被堆积起来：  

```
s, err := store.New()
if err != nil {
    return fmt.Errorf(
        "failed to create new store: %w", err)
}

// failed to x: failed to y: failed to create new store: the error
```

```
s, err := store.New()
if err != nil {
    return fmt.Errorf(
        "new store: %w", err)
}

// x: y: new store: the error
```
然而，一旦错误被发送到另一个系统，应该清楚消息是一个错误（例如err 标签或日志中的"Failed"前缀）。

另见 不要只检查错误，优雅地处理它们。

#### 6.11.3. 错误命名
对于存储为全局变量的错误值，  
根据是否导出，使用前缀 Err 或 err。  
请看指南 对于未导出的顶层常量和变量，使用_作为前缀。
```
var (
  // 导出以下两个错误，以便此包的用户可以将它们与 errors.Is 进行匹配。

  ErrBrokenLink = errors.New("link is broken")
  ErrCouldNotOpen = errors.New("could not open")

  // 这个错误没有被导出，因为我们不想让它成为我们公共 API 的一部分。 我们可能仍然在带有错误的包内使用它。

  errNotFound = errors.New("not found")
)
```
对于自定义错误类型，请改用后缀 Error。
```
// 同样，这个错误被导出，以便这个包的用户可以将它与 errors.As 匹配。

type NotFoundError struct {
  File string
}

func (e *NotFoundError) Error() string {
  return fmt.Sprintf("file %q not found", e.File)
}

// 并且这个错误没有被导出，因为我们不想让它成为公共 API 的一部分。 我们仍然可以在带有 errors.As 的包中使用它。
type resolveError struct {
  Path string
}

func (e *resolveError) Error() string {
  return fmt.Sprintf("resolve %q", e.Path)
}
```

### 6.12. 处理断言失败
类型断言 将会在检测到不正确的类型时，以单一返回值形式返回 panic。 因此，请始终使用“逗号 ok”习语。
- Bad
```
t := i.(string)
```
- Good
```
t, ok := i.(string)
if !ok {
  // 优雅地处理错误
}
```

### 6.13. 不要使用 panic
在生产环境中运行的代码必须避免出现 panic。panic 是 级联失败 的主要根源 。如果发生错误，该函数必须返回错误，并允许调用方决定如何处理它。
- Bad
```
func run(args []string) {
  if len(args) == 0 {
    panic("an argument is required")
  }
  // ...
}

func main() {
  run(os.Args[1:])
}
```
- Godd
```
func run(args []string) error {
  if len(args) == 0 {
    return errors.New("an argument is required")
  }
  // ...
  return nil
}

func main() {
  if err := run(os.Args[1:]); err != nil {
    fmt.Fprintln(os.Stderr, err)
    os.Exit(1)
  }
}
```
panic/recover 不是错误处理策略。仅当发生不可恢复的事情（例如：nil 引用）时，程序才必须 panic。程序初始化是一个例外：程序启动时应使程序中止的不良情况可能会引起 panic。


即使在测试代码中，也优先使用t.Fatal或者t.FailNow而不是 panic 来确保失败被标记。
- Bad
```
// func TestFoo(t *testing.T)

f, err := ioutil.TempFile("", "test")
if err != nil {
  panic("failed to set up test")
}
```
- Good
```
// func TestFoo(t *testing.T)

f, err := ioutil.TempFile("", "test")
if err != nil {
  t.Fatal("failed to set up test")
}
```

### 6.14. 使用 go.uber.org/atomic
使用 sync/atomic 包的原子操作对原始类型 (int32, int64等）进行操作，因为很容易忘记使用原子操作来读取或修改变量。

go.uber.org/atomic 通过隐藏基础类型为这些操作增加了类型安全性。此外，它包括一个方便的atomic.Bool类型。
- Bad
```
type foo struct {
  running int32  // atomic
}

func (f* foo) start() {
  if atomic.SwapInt32(&f.running, 1) == 1 {
     // already running…
     return
  }
  // start the Foo
}

func (f *foo) isRunning() bool {
  return f.running == 1  // race!
}
```
- Good
```
type foo struct {
  running atomic.Bool
}

func (f *foo) start() {
  if f.running.Swap(true) {
     // already running…
     return
  }
  // start the Foo
}

func (f *foo) isRunning() bool {
  return f.running.Load()
}
```

### 6.15. 避免可变全局变量
使用选择依赖注入方式避免改变全局变量。
既适用于函数指针又适用于其他值类型
- Bad
```
// sign.go
var _timeNow = time.Now
func sign(msg string) string {
  now := _timeNow()
  return signWithTime(msg, now)
}

// sign_test.go
func TestSign(t *testing.T) {
  oldTimeNow := _timeNow
  _timeNow = func() time.Time {
    return someFixedTime
  }
  defer func() { _timeNow = oldTimeNow }()
  assert.Equal(t, want, sign(give))
}
```
- Good
```
// sign.go
type signer struct {
  now func() time.Time
}
func newSigner() *signer {
  return &signer{
    now: time.Now,
  }
}
func (s *signer) Sign(msg string) string {
  now := s.now()
  return signWithTime(msg, now)
}

// sign_test.go
func TestSigner(t *testing.T) {
  s := newSigner()
  s.now = func() time.Time {
    return someFixedTime
  }
  assert.Equal(t, want, s.Sign(give))
}
```

### 6.16. 避免在公共结构中嵌入类型
这些嵌入的类型泄漏实现细节、禁止类型演化和模糊的文档。

假设您使用共享的 AbstractList 实现了多种列表类型，请避免在具体的列表实现中嵌入 AbstractList。  
相反，只需手动将方法写入具体的列表，该列表将委托给抽象列表。
```
type AbstractList struct {}
// 添加将实体添加到列表中。
func (l *AbstractList) Add(e Entity) {
  // ...
}
// 移除从列表中移除实体。
func (l *AbstractList) Remove(e Entity) {
  // ...
}
```
- Bad
```
// ConcreteList 是一个实体列表。
type ConcreteList struct {
  *AbstractList
}
```
- Good
```
// ConcreteList 是一个实体列表。
type ConcreteList struct {
  list *AbstractList
}
// 添加将实体添加到列表中。
func (l *ConcreteList) Add(e Entity) {
  l.list.Add(e)
}
// 移除从列表中移除实体。
func (l *ConcreteList) Remove(e Entity) {
  l.list.Remove(e)
}
```
Go 允许 类型嵌入 作为继承和组合之间的折衷。外部类型获取嵌入类型的方法的隐式副本。默认情况下，这些方法委托给嵌入实例的同一方法。

结构还获得与类型同名的字段。  
所以，如果嵌入的类型是 public，那么字段是 public。为了保持向后兼容性，外部类型的每个未来版本都必须保留嵌入类型。

很少需要嵌入类型。  
这是一种方便，可以帮助您避免编写冗长的委托方法。

即使嵌入兼容的抽象列表 interface，而不是结构体，这将为开发人员提供更大的灵活性来改变未来，但仍然泄露了具体列表使用抽象实现的细节。
- Bad
```
// AbstractList 是各种实体列表的通用实现。
type AbstractList interface {
  Add(Entity)
  Remove(Entity)
}
// ConcreteList 是一个实体列表。
type ConcreteList struct {
  AbstractList
}
```
- Good
```
// AbstractList 是各种实体列表的通用实现。
type AbstractList interface {
  Add(Entity)
  Remove(Entity)
}
// ConcreteList 是一个实体列表。
type ConcreteList struct {
  list AbstractList
}
// 添加将实体添加到列表中。
func (l *ConcreteList) Add(e Entity) {
  l.list.Add(e)
}
// 移除从列表中移除实体。
func (l *ConcreteList) Remove(e Entity) {
  l.list.Remove(e)
}
```
无论是使用嵌入结构还是嵌入接口，都会限制类型的演化。

- 向嵌入接口添加方法是一个破坏性的改变。
- 从嵌入结构体删除方法是一个破坏性改变。
- 删除嵌入类型是一个破坏性的改变。
- 即使使用满足相同接口的类型替换嵌入类型，也是一个破坏性的改变。

尽管编写这些委托方法是乏味的，但是额外的工作隐藏了实现细节，留下了更多的更改机会，还消除了在文档中发现完整列表接口的间接性操作。

直白点说，就是不希望结构体暴露不必要的实现（方法和属性），符号最小依赖原则

### 6.17. 避免使用内置名称
Go 语言规范 概述了几个内置的，
不应在 Go 项目中使用的 预先声明的标识符。

根据上下文的不同，将这些标识符作为名称重复使用，
将在当前作用域（或任何嵌套作用域）中隐藏原始标识符，或者混淆代码。
在最好的情况下，编译器会报错；在最坏的情况下，这样的代码可能会引入潜在的、难以恢复的错误。
- Bad
```
var error string
// `error` 作用域隐式覆盖

// or

func handleErrorMessage(error string) {
    // `error` 作用域隐式覆盖
}

type Foo struct {
    // 虽然这些字段在技术上不构成阴影，但`error`或`string`字符串的重映射现在是不明确的。
    error  error
    string string
}

func (f Foo) Error() error {
    // `error` 和 `f.error` 在视觉上是相似的
    return f.error
}

func (f Foo) String() string {
    // `string` and `f.string` 在视觉上是相似的
    return f.string
}
```
- Good
```
var errorMessage string
// `error` 指向内置的非覆盖

// or

func handleErrorMessage(msg string) {
    // `error` 指向内置的非覆盖
}

type Foo struct {
    // `error` and `string` 现在是明确的。
    err error
    str string
}

func (f Foo) Error() error {
    return f.err
}

func (f Foo) String() string {
    return f.str
}
```

注意，编译器在使用预先分隔的标识符时不会生成错误，
但是诸如go vet之类的工具会正确地指出这些和其他情况下的隐式问题。

### 6.18. 追加时优先指定切片容量
追加时优先指定切片容量

在尽可能的情况下，在初始化要追加的切片时为make()提供一个容量值。
- Bad
```
for n := 0; n < b.N; n++ {
  data := make([]int, 0)
  for k := 0; k < size; k++{
    data = append(data, k)
  }
}

// BenchmarkBad-4    100000000    2.48s
```
- Good
```
for n := 0; n < b.N; n++ {
  data := make([]int, 0, size)
  for k := 0; k < size; k++{
    data = append(data, k)
  }
}

// BenchmarkGood-4   100000000    0.21s
```

### 6.19. 主函数退出方式 (Exit)
Go 程序使用 os.Exit 或者 log.Fatal* 立即退出 (使用panic不是退出程序的好方法，请 不要使用 panic。)

仅在main() 中调用其中一个 os.Exit 或者 log.Fatal*。所有其他函数应将错误返回到信号失败中。
- Bad
```
func main() {
  body := readFile(path)
  fmt.Println(body)
}
func readFile(path string) string {
  f, err := os.Open(path)
  if err != nil {
    log.Fatal(err)
  }
  b, err := ioutil.ReadAll(f)
  if err != nil {
    log.Fatal(err)
  }
  return string(b)
}
```
- Good
```
func main() {
  body, err := readFile(path)
  if err != nil {
    log.Fatal(err)
  }
  fmt.Println(body)
}
func readFile(path string) (string, error) {
  f, err := os.Open(path)
  if err != nil {
    return "", err
  }
  b, err := ioutil.ReadAll(f)
  if err != nil {
    return "", err
  }
  return string(b), nil
}
```
原则上： 有多个退出入口的程序存在一些问题：

- 不明显的控制流：任何函数都可以退出程序，因此很难对控制流进行推理。
- 难以测试：退出程序的函数也将退出调用它的测试。这使得函数很难测试，并引入了跳过 go test 尚未运行的其他测试的风险。
- 跳过清理：当函数退出程序时，会跳过已经进入defer队列里的函数调用。这增加了跳过重要清理任务的风险。

##### 1.6.19.1. 一次性退出
如果可能的话，你的main（）函数中 最多一次 调用 os.Exit或者log.Fatal。如果有多个错误场景停止程序执行，请将该逻辑放在单独的函数下并从中返回错误。
这会缩短 main() 函数，并将所有关键业务逻辑放入一个单独的、可测试的函数中。
- Bad
```
package main
func main() {
  args := os.Args[1:]
  if len(args) != 1 {
    log.Fatal("missing file")
  }
  name := args[0]
  f, err := os.Open(name)
  if err != nil {
    log.Fatal(err)
  }
  defer f.Close()
  // 如果我们调用 log.Fatal 在这条线之后
  // f.Close 将会被执行。
  b, err := ioutil.ReadAll(f)
  if err != nil {
    log.Fatal(err)
  }
  // ...
}
```
- Good
```
package main
func main() {
  if err := run(); err != nil {
    log.Fatal(err)
  }
}
func run() error {
  args := os.Args[1:]
  if len(args) != 1 {
    return errors.New("missing file")
  }
  name := args[0]
  f, err := os.Open(name)
  if err != nil {
    return err
  }
  defer f.Close()
  b, err := ioutil.ReadAll(f)
  if err != nil {
    return err
  }
  // ...
}
```

## 7. 性能
性能方面的特定准则只适用于高频场景。普通场景下**【非强制】**

### 7.1. 优先使用 strconv 而不是 fmt
将原语转换为字符串或从字符串转换时，strconv速度比fmt快。
- Bad
```
for i := 0; i < b.N; i++ {
  s := fmt.Sprint(rand.Int())
}

// BenchmarkFmtSprint-4    143 ns/op    2 allocs/op
```
- Good
```
for i := 0; i < b.N; i++ {
  s := strconv.Itoa(rand.Int())
}

// BenchmarkStrconv-4    64.2 ns/op    1 allocs/op
```

### 7.2. 避免字符串到字节的转换
不要反复从固定字符串创建字节 slice。相反，请执行一次转换并捕获结果。
- Bad
```
for i := 0; i < b.N; i++ {
  w.Write([]byte("Hello world"))
}

// BenchmarkBad-4   50000000   22.2 ns/op
```
- Good
```
data := []byte("Hello world")
for i := 0; i < b.N; i++ {
  w.Write(data)
}

// BenchmarkGood-4  500000000   3.25 ns/op
```

### 7.3. 指定容器容量
尽可能指定容器容量，以便为容器预先分配内存。这将在添加元素时最小化后续分配（通过复制和调整容器大小）。

#### 7.3.1. 指定 Map 容量提示
在尽可能的情况下，在使用 make() 初始化的时候提供容量信息

make(map[T1]T2, hint)

向make()提供容量提示会在初始化时尝试调整 map 的大小，这将减少在将元素添加到 map 时为 map 重新分配内存。

注意，与 slices 不同。map capacity 提示并不保证完全的抢占式分配，而是用于估计所需的 hashmap bucket 的数量。
因此，在将元素添加到 map 时，甚至在指定 map 容量时，仍可能发生分配。
- Bad
```
m := make(map[string]os.FileInfo)

files, _ := ioutil.ReadDir("./files")
for _, f := range files {
    m[f.Name()] = f
}

// m 是在没有大小提示的情况下创建的； 在运行时可能会有更多分配。
```
- Good
```
files, _ := ioutil.ReadDir("./files")

m := make(map[string]os.FileInfo, len(files))
for _, f := range files {
    m[f.Name()] = f
}

// m 是有大小提示创建的；在运行时可能会有更少的分配。
```

#### 7.3.2. 指定切片容量
在尽可能的情况下，在使用make()初始化切片时提供容量信息，特别是在追加切片时。

make([]T, length, capacity)

与 maps 不同，slice capacity 不是一个提示：编译器将为提供给make()的 slice 的容量分配足够的内存，
这意味着后续的 append()`操作将导致零分配（直到 slice 的长度与容量匹配，在此之后，任何 append 都可能调整大小以容纳其他元素）。
- Bad
```
for n := 0; n < b.N; n++ {
  data := make([]int, 0)
  for k := 0; k < size; k++{
    data = append(data, k)
  }
}

// BenchmarkBad-4    100000000    2.48s
```
- Good
```
for n := 0; n < b.N; n++ {
  data := make([]int, 0, size)
  for k := 0; k < size; k++{
    data = append(data, k)
  }
}

// BenchmarkGood-4   100000000    0.21s
```

## 8. 代码检查工具
比任何 "blessed" linter 集更重要的是，lint 在一个代码库中始终保持一致。

要求至少使用以下 linters，因为它们有助于发现最常见的问题，并在不需要规定的情况下为代码质量建立一个高标准：

- errcheck 以确保错误得到处理

- goimports 格式化代码和管理 imports

- golint 指出常见的文体错误

- govet 分析代码中的常见错误
