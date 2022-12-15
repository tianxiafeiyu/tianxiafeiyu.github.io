---
title: go流程控制
---

# switch
## java switch与go switch

 - | Java | Golang
---|---|---
变量expression |byte、short、int 、 char和String | 任何类型
break 语句 | 如果当前匹配成功的 case 语句块没有 break 语句，则从当前 case 开始，后续所有 case 的值都会输出，如果后续的 case 语句块有 break 语句则会跳出判断。default不需要break | switch 默认情况下 case 最后自带 break 语句，匹配成功后就不会执行其他 case，如果我们需要执行后面的 case，可以使用 fallthrough
Type Switch | 无 | switch 语句还可以被用于 type-switch 来判断某个 interface 变量中实际存储的变量类型

Java
```
switch(expression){
    case value :
       //语句
       break; //可选
    case value :
       //语句
       break; //可选
    //你可以有任意数量的case语句
    default : //可选
       //语句
}
```

Go
```
switch expression{
    case val1:
        ...
    case val2:
        ...
        fallthrough
    default:
        ...
}
```

## go switch 默认值的坑
```
package main

import "fmt"

func ff() bool {
	return false
}

func main() {
	// switch 默认为true
	switch {
	case true:
		fmt.Println("默认true")
	case false:
		fmt.Println("默认为fasle")
	}
	}

	// switch 支持初始化语句
	switch f := ff(); f {
	case true:
		fmt.Println("true")
	case false:
		fmt.Println("fasle")
	}

	// switch 只有初始化语句 条件默认为true
	switch ff(); {
	case true:
		fmt.Println("默认为true")
	case false:
		fmt.Println("默认为fasle")
	}
}

//默认true
//fasle
//默认为true
```

# for
Go里面最强大的一个控制逻辑就是for，它即可以用来循环读取数据，又可以当作while来控制逻辑，还能迭代操作。它的语法如下：
```
for expression1; expression2; expression3 {
    //...
}
```
expression1、expression2和expression3都是表达式，其中expression1和expression3是变量声明或者函数调用返回值之类的，expression2是用来条件判断，expression1在循环开始之前调用，expression3在每轮循环结束之时调用。

例子：
```
package main
import "fmt"

func main(){
    sum := 0;
    for index:=0; index < 10 ; index++ {
        sum += index
    }
    fmt.Println("sum is equal to ", sum)
}
// 输出：
// sum is equal to 45
```
有些时候需要进行多个赋值操作，由于Go里面没有,操作符，那么可以使用平行赋值i, j = i+1, j-1

有些时候如果我们忽略expression1和expression3：
```
sum := 1
for ; sum < 1000;  {
    sum += sum
}
```
其中;也可以省略，那么就变成如下的代码了，是不是似曾相识？对，这就是while的功能。
```
sum := 1
for sum < 1000 {
    sum += sum
}
```
在循环里面有两个关键操作break和continue ,break操作是跳出当前循环，continue是跳过本次循环。当嵌套过深的时候，break可以配合标签使用，即跳转至标签所指定的位置，详细参考如下例子：
```
for index := 10; index>0; index-- {
    if index == 5{
        break // 或者continue
    }
    fmt.Println(index)
}
// break打印出来10、9、8、7、6
// continue打印出来10、9、8、7、6、4、3、2、1
```
break和continue还可以跟着标号，用来跳到多重循环中的外层循环

for配合range可以用于读取slice和map的数据：
```
for k,v:=range map {
    fmt.Println("map's key:",k)
    fmt.Println("map's val:",v)
}
```
由于 Go 支持 “多值返回”, 而对于“声明而未被调用”的变量, 编译器会报错, 在这种情况下, 可以使用_来丢弃不需要的返回值 例如
```
for _, v := range map{
    fmt.Println("map's val:", v)
}
```

## for range槽点
https://juejin.cn/post/6844903474019172360

# if
if也许是各种编程语言中最常见的了，它的语法概括起来就是:如果满足条件就做某事，否则做另一件事。

Go里面if条件判断语句中不需要括号，如下代码所示
```
if x > 10 {
    fmt.Println("x is greater than 10")
} else {
    fmt.Println("x is less than 10")
}
```
Go的if还有一个强大的地方就是条件判断语句里面允许声明一个变量，这个变量的作用域只能在该条件逻辑块内，其他地方就不起作用了，如下所示
```
// 计算获取值x,然后根据x返回的大小，判断是否大于10。
if x := computedValue(); x > 10 {
    fmt.Println("x is greater than 10")
} else {
    fmt.Println("x is less than 10")
}
//这个地方如果这样调用就编译出错了，因为x是条件里面的变量
fmt.Println(x)
```
多个条件的时候如下所示：
```
if integer == 3 {
    fmt.Println("The integer is equal to 3")
} else if integer < 3 {
    fmt.Println("The integer is less than 3")
} else {
    fmt.Println("The integer is greater than 3")
}
```

# select 
go里面提供了一个关键字select,通过select可以监听channel上的数据流动

select的用法与switch语言非常类似,由select开始一个新的选择块,每个选择块条件由case语句来描述

与switch语句可以选择任何可使用相等比较的条件相比,select有比较多的限制,其中最大的一条限制就是每个case语句里必须是一个IO操作
```
for {
    select {
        case <-chan1:
            //.....
        case chan2<-1:
            //....
        default:
            //都没成功,进入......
    }
}
```

## 注意
1. 监听的case中,没有满足条件的就阻塞，存在多个满足条件的就任选一个执行（用一种伪随机的算法在这些分支中选择一个并执行）
2. select本身不带循环,需要外层的for
3. default通常不用,会产生忙轮询
4. break只能跳出select中的一个case
    - 加入了默认分支，那么无论涉及通道操作的表达式是否有阻塞，select语句都不会被阻塞。如果那几个表达式都阻塞了，或者说都没有满足求值的条件，那么默认分支就会被选中并执行。

    - 如果没有加入默认分支，那么一旦所有的case表达式都没有满足求值条件，那么select语句就会被阻塞。直到至少有一个case表达式满足条件为止。
    
## 定时轮询
加入timetricker防止超时
```
func (pc *ProcessCache) Clean() {
	ticker := time.NewTicker(10 * time.Minute)
	for {
		select {
		case <-ticker.C:
			pc.clean()
		}
	}
}
```


# goto
Go有goto语句——请明智地使用它。用goto跳转到必须在当前函数内定义的标签。例如假设这样一个循环：
```
func myFunc() {
    i := 0
Here:   //这行的第一个词，以冒号结束作为标签
    println(i)
    i++
    goto Here   //跳转到Here去
}
// 标签名是大小写敏感的。
```