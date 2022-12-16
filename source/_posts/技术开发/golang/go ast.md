---
title: go ast
date: 2022-12-15 23:19:22
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - go ast
---
## 抽象语法树

抽象语法树（abstract syntax code，AST）是源代码的抽象语法结构的树状表示，树上的每个节点都表示源代码中的一种结构。简单理解,就是把我们写的代码按照一定的规则转换成一种树形结构。

在传统的编译语言的流程中,程序的一段源代码在执行之前会经历三个步骤,统称为"编译":

*   分词/词法分析

这个过程会将由字符组成的字符串分解成有意义的代码块,这些代码块统称为词法单元(token).

举个例子: let a = 1, 这段程序通常会被分解成为下面这些词法单元: let 、a、=、1 ，空格是否被当成词法单元，取决于空格在这门语言中的意义。

*   解析/语法分析

这个过程是将词法单元流转换成一个由元素嵌套所组成的代表了程序语法结构的树,这个树被称为"抽象语法树"（abstract syntax code，AST）

*   代码生成

将AST转换成可执行代码的过程被称为代码生成.

![go ast](https://note.youdao.com/yws/api/personal/file/CC292A272DC3434F80398765B2969C30?method=download\&shareKey=b0bbf4724c53dce5a1698c4d5fd02d11)

### 名词解释

#### 1.普通Node,不是特定语法结构,属于某个语法结构的一部分

*   Comment 表示一行注释 // 或者 / /

*   CommentGroup 表示多行注释

*   Field 表示结构体中的一个定义或者变量,或者函数签名当中的参数或者返回值

*   FieldList 表示以”{}”或者”()”包围的Filed列表

#### 2.Expression & Types (表达式和类型)

*   BadExpr 包含语法错误的表达式的占位符，不能创建正确的表达式节点

*   Ident 比如包名,函数名,变量名

*   Ellipsis 省略号表达式,比如参数列表的最后一个可以写成 arg...

*   BasicLit 基本类型,数字或者字符串

*   FuncLit 函数定义

*   CompositeLit 构造类型,比如{1,2,3,4}

*   ParenExpr 括号表达式,被括号包裹的表达式

*   SelectorExpr 选择结构,类似于a.b的结构

*   IndexExpr 下标结构,类似这样的结构 expr\[expr]

*   SliceExpr 切片表达式,类似这样 expr\[low\:mid\:high]

*   TypeAssertExpr 类型断言类似于 X.(type)

*   CallExpr 调用类型,类似于 expr()

*   StarExpr 表达式,类似于 \*X

*   UnaryExpr 一元表达式

*   BinaryExpr 二元表达式

*   KeyValueExp 键值表达式 key\:value

*   ArrayType 数组或切片类型

*   StructType 结构体类型

*   FuncType 函数类型

*   InterfaceType 接口类型

*   MapType map类型

*   ChanType 管道类型

#### 3.Statements （语句，一段代码）

*   BadStmt 包含语法错误的语句的占位符，其中不能创建正确的语句节点

*   DeclStmt 在语句列表里的申明

*   EmptyStmt 空语句

*   LabeledStmt 标签语句类似于 indent\:stmt

*   ExprStmt 包含单独的表达式语句(例如：fmt.Printf())

*   SendStmt chan发送语句

*   IncDecStmt 自增或者自减语句

*   AssignStmt 表示赋值或短变量声明

*   GoStmt Go语句

*   DeferStmt 延迟语句

*   ReturnStmt return 语句

*   BranchStmt 分支语句 例如break continue

*   BlockStmt 块语句 {} 包裹

*   IfStmt If 语句

*   CaseClause case 语句

*   SwitchStmt switch 语句

*   TypeSwitchStmt 类型switch 语句 switch x:=y.(type)

*   CommClause 发送或者接受的case语句,类似于 case x <-:

*   SelectStmt select 语句

*   ForStmt for 循环语句

*   RangeStmt range 语句

#### 4.Declarations 声明

*   ImportSpec 导包声明

*   ValueSpec 常量或变量声明（ConstSpec 或 VarSpec 生成）

*   TypeSpec 类型声明

*   BadDecl 包含语法错误的声明的占位符，其中不能创建正确的声明节点。

*   GenDecl 一般申明(和Spec相关,比如 import “a”,var a,type a)

*   FuncDecl 函数申明

#### 5.Files and Packages

*   File 代表一个源文件节点,包含了顶级元素.

*   Package 代表一个包,包含了很多文件.

### ast体验

一个在线的go源码转ast网站： <https://yuroyoro.github.io/goast-viewer/index.html>

源码

*   foo.go

<!---->

    package main

    import (
    	"fmt"
    )

    var test = "hello go"

    func main() {
    	fmt.Printf("Hello, Golang\n")
    }

ast

    0  *ast.File {
    1  .  Doc: nil
    2  .  Package: foo:1:1
    3  .  Name: *ast.Ident {
    4  .  .  NamePos: foo:1:9
    5  .  .  Name: "main"
    6  .  .  Obj: nil
    7  .  }
    8  .  Decls: []ast.Decl (len = 3) {
    9  .  .  0: *ast.GenDecl {
    10  .  .  .  Doc: nil
    11  .  .  .  TokPos: foo:3:1
    12  .  .  .  Tok: import
    13  .  .  .  Lparen: foo:3:8
    14  .  .  .  Specs: []ast.Spec (len = 1) {
    15  .  .  .  .  0: *ast.ImportSpec {
    16  .  .  .  .  .  Doc: nil
    17  .  .  .  .  .  Name: nil
    18  .  .  .  .  .  Path: *ast.BasicLit {
    19  .  .  .  .  .  .  ValuePos: foo:4:2
    20  .  .  .  .  .  .  Kind: STRING
    21  .  .  .  .  .  .  Value: "\"fmt\""
    22  .  .  .  .  .  }
    23  .  .  .  .  .  Comment: nil
    24  .  .  .  .  .  EndPos: -
    25  .  .  .  .  }
    26  .  .  .  }
    27  .  .  .  Rparen: foo:5:1
    28  .  .  }
    29  .  .  1: *ast.GenDecl {
    30  .  .  .  Doc: nil
    31  .  .  .  TokPos: foo:7:1
    32  .  .  .  Tok: var
    33  .  .  .  Lparen: -
    34  .  .  .  Specs: []ast.Spec (len = 1) {
    35  .  .  .  .  0: *ast.ValueSpec {
    36  .  .  .  .  .  Doc: nil
    37  .  .  .  .  .  Names: []*ast.Ident (len = 1) {
    38  .  .  .  .  .  .  0: *ast.Ident {
    39  .  .  .  .  .  .  .  NamePos: foo:7:5
    40  .  .  .  .  .  .  .  Name: "test"
    41  .  .  .  .  .  .  .  Obj: *ast.Object {
    42  .  .  .  .  .  .  .  .  Kind: var
    43  .  .  .  .  .  .  .  .  Name: "test"
    44  .  .  .  .  .  .  .  .  Decl: *(obj @ 35)
    45  .  .  .  .  .  .  .  .  Data: 0
    46  .  .  .  .  .  .  .  .  Type: nil
    47  .  .  .  .  .  .  .  }
    48  .  .  .  .  .  .  }
    49  .  .  .  .  .  }
    50  .  .  .  .  .  Type: nil
    51  .  .  .  .  .  Values: []ast.Expr (len = 1) {
    52  .  .  .  .  .  .  0: *ast.BasicLit {
    53  .  .  .  .  .  .  .  ValuePos: foo:7:12
    54  .  .  .  .  .  .  .  Kind: STRING
    55  .  .  .  .  .  .  .  Value: "\"hello go\""
    56  .  .  .  .  .  .  }
    57  .  .  .  .  .  }
    58  .  .  .  .  .  Comment: nil
    59  .  .  .  .  }
    60  .  .  .  }
    61  .  .  .  Rparen: -
    62  .  .  }
    63  .  .  2: *ast.FuncDecl {
    64  .  .  .  Doc: nil
    65  .  .  .  Recv: nil
    66  .  .  .  Name: *ast.Ident {
    67  .  .  .  .  NamePos: foo:9:6
    68  .  .  .  .  Name: "main"
    69  .  .  .  .  Obj: *ast.Object {
    70  .  .  .  .  .  Kind: func
    71  .  .  .  .  .  Name: "main"
    72  .  .  .  .  .  Decl: *(obj @ 63)
    73  .  .  .  .  .  Data: nil
    74  .  .  .  .  .  Type: nil
    75  .  .  .  .  }
    76  .  .  .  }
    77  .  .  .  Type: *ast.FuncType {
    78  .  .  .  .  Func: foo:9:1
    79  .  .  .  .  Params: *ast.FieldList {
    80  .  .  .  .  .  Opening: foo:9:10
    81  .  .  .  .  .  List: nil
    82  .  .  .  .  .  Closing: foo:9:11
    83  .  .  .  .  }
    84  .  .  .  .  Results: nil
    85  .  .  .  }
    86  .  .  .  Body: *ast.BlockStmt {
    87  .  .  .  .  Lbrace: foo:9:13
    88  .  .  .  .  List: []ast.Stmt (len = 1) {
    89  .  .  .  .  .  0: *ast.ExprStmt {
    90  .  .  .  .  .  .  X: *ast.CallExpr {
    91  .  .  .  .  .  .  .  Fun: *ast.SelectorExpr {
    92  .  .  .  .  .  .  .  .  X: *ast.Ident {
    93  .  .  .  .  .  .  .  .  .  NamePos: foo:10:2
    94  .  .  .  .  .  .  .  .  .  Name: "fmt"
    95  .  .  .  .  .  .  .  .  .  Obj: nil
    96  .  .  .  .  .  .  .  .  }
    97  .  .  .  .  .  .  .  .  Sel: *ast.Ident {
    98  .  .  .  .  .  .  .  .  .  NamePos: foo:10:6
    99  .  .  .  .  .  .  .  .  .  Name: "Printf"
    100  .  .  .  .  .  .  .  .  .  Obj: nil
    101  .  .  .  .  .  .  .  .  }
    102  .  .  .  .  .  .  .  }
    103  .  .  .  .  .  .  .  Lparen: foo:10:12
    104  .  .  .  .  .  .  .  Args: []ast.Expr (len = 1) {
    105  .  .  .  .  .  .  .  .  0: *ast.BasicLit {
    106  .  .  .  .  .  .  .  .  .  ValuePos: foo:10:13
    107  .  .  .  .  .  .  .  .  .  Kind: STRING
    108  .  .  .  .  .  .  .  .  .  Value: "\"Hello, Golang\\n\""
    109  .  .  .  .  .  .  .  .  }
    110  .  .  .  .  .  .  .  }
    111  .  .  .  .  .  .  .  Ellipsis: -
    112  .  .  .  .  .  .  .  Rparen: foo:10:30
    113  .  .  .  .  .  .  }
    114  .  .  .  .  .  }
    115  .  .  .  .  }
    116  .  .  .  .  Rbrace: foo:11:1
    117  .  .  .  }
    118  .  .  }
    119  .  }
    120  .  Scope: *ast.Scope {
    121  .  .  Outer: nil
    122  .  .  Objects: map[string]*ast.Object (len = 2) {
    123  .  .  .  "main": *(obj @ 69)
    124  .  .  .  "test": *(obj @ 41)
    125  .  .  }
    126  .  }
    127  .  Imports: []*ast.ImportSpec (len = 1) {
    128  .  .  0: *(obj @ 15)
    129  .  }
    130  .  Unresolved: []*ast.Ident (len = 1) {
    131  .  .  0: *(obj @ 92)
    132  .  }
    133  .  Comments: nil
    134  }

### 用法示例

打印代码中的所有字符串

    func extractString() error {
    	fset := token.NewFileSet()
    	astFile, err := parser.ParseFile(fset, "main.go", nil, parser.ParseComments|parser.AllErrors)
    	if err != nil {
    		return err
    	}

    	ast.Inspect(astFile, func(n ast.Node) bool {
    		switch x := n.(type) {
    		case *ast.BasicLit:
    			s, _ := strconv.Unquote(x.Value)
    			if len(s) > 0 && x.Kind == token.STRING {
    				fmt.Println(s)
    			}
    		}
    		return true
    	})

    	return nil
    }

