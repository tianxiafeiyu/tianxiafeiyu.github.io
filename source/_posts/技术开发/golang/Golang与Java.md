转载自 https://blog.csdn.net/pbrlovejava/article/details/108920137

## 一、Golang概述
### 1.1 Golang基本介绍
Go语言（或 Golang）起源于 2007 年，并在 2009 年正式对外发布。Go 是非常年轻的一门语言，它的主要目标是“兼具 Python 等动态语言的开发速度和 C/C++ 等编译型语言的性能与安全性”。

Go语言的推出，旨在不损失应用程序性能的情况下降低代码的复杂性，具有“部署简单、并发性好、语言设计良好、执行性能好”等优势，目前国内诸多 IT 公司均已采用Go语言开发项目。

Go语言有时候被描述为“C 类似语言”，或者是“21 世纪的C语言”。Go 从C语言继承了相似的表达式语法、控制流结构、基础数据类型、调用参数传值、指针等很多思想，还有C语言一直所看中的编译后机器码的运行效率以及和现有操作系统的无缝适配。

因为Go语言没有类和继承的概念，所以它和 Java 或 C++ 看起来并不相同。但是它通过接口（interface）的概念来实现多态性。Go语言有一个清晰易懂的轻量级类型系统，在类型之间也没有层级之说。因此可以说Go语言是一门混合型的语言。

此外，很多重要的开源项目都是使用Go语言开发的，其中包括 Docker、Go-Ethereum、Thrraform 和 Kubernetes。

### 1.2 Golang使用场景
- 服务端开发（配合gin、gorm等库就能够完成高性能的后端服务）
- 容器开发（譬如Docker、K8s都是基于Golang开发的）
- 脚本开发（由于Golang自身部署简单，并且与操作系统API交互方便，所以还可替代Python作为脚本开发）
- 底层工具的开发（可代替C或者C++开发操作系统底层工具）

## 二、基本语法
### 2.1 编码规约
#### 1. 左右花括号需要符合上下换行风格
Golang是一门严格的工程语言，主要体现在编码风格及可见域规则上。在Java中，允许多种编码风格共存，譬如以下两种方法声明，对于Java来说都是允许的：
```
public String getString(Integer num) {
    return num.toString();
}

public String getString(Integer num) 
{
    return num.toString();
}
```
在Golang中，只允许出现一种换行风格，否则会报错，无法通过编译。
```
func getString(num int) string {
	return strconv.Itoa(num)
}
```

#### 2. 变量声明后必须使用，不使用需要使用“_“来代替
在Java中，变量可以声明了却不使用，而Golang中声明的变量必须被使用，否则需要使用_来替代掉变量名，表明该变量不会比使用到：
```
func getString(num int) string {
	temp := num // 没有使用者，无法编译
	_ := num	// 正常编译
	return strconv.Itoa(num)
}
```
#### 3. 可见域规则
Java对方法、变量及类的可见域规则是通过private、protected、public关键字来控制的，而Golang中控制可见域的方式只有一个，当字段首字母开头是大写时说明其是对外可见的、小写时只对包内成员可见。
```
package entity

type Person struct {
	Name string
	Age int
	id string
}

type student struct {
	detail Person
}

func test() {
	// 本包内可见
	person := &student{detail: Person{
		Name: "ARong",
		Age:  21,
		id:   "211",
	}}
	fmt.Println(person)
}
```
```
package main

import (
	"fmt"
	entity "others/scope"
)

func main() {
	// id字段不可见
	person := &entity.Person{
		Name: "ARong",
		Age:  21,
	}
	fmt.Println(person)
}
```
### 2.2 变量声明及初始化
#### 1. 变量声明及初始化的文法
在Java中，通常声明变量及初始化的文法为：
```Java
// Object:要声明的类型、v:变量名称、new Object()变量初始化
Object v = new Object();
```
而Golang使用var关键字来声明变量：
```
// var：变量定义、v1:变量名称、int:变量类型
var v1 int
var v2 string
var v3 [10]int  // 数组
var v4 []int // 数组切片
var v5 struct {
	f int
}
var v6 *int // 指针
var v7 map[string]int  // map，key为string类型，value为int类型
var v8 func(a int) int
var v9,v10 int //v9和v10都声明为int型
```
也可以采用“:=”自动推测变量类型:
```
var v1 int = 10 // 正确的使用方式1
var v2 = 10  // 正确的使用方式2，编译器可以自动推导出v2的类型
v3 := 10  // 正确的使用方式3，编译器可以自动推导出v3的类型
```
#### 2. 对于基本类型,声明即初始化；对于引用类型，声明则初始化为nil
在Java中，如果在方法内部声明一个变量但不初始化，在使用时会出现编译错误：
```
public void solve() {
    int num;
    Object object;
    System.out.println(num); // 编译错误
    System.out.println(object); // 编译错误
}
```
而在Golang中，对于基本类型来讲，声明即初始化;对于引用类型，声明则初始化为nil。这样可以极大地避免NPE的发生。
```
func main() {
	var num int
	var hashMap *map[string]int
	fmt.Println(num) // num = 0
	fmt.Println(hashMap) //  &hashMap== nil
}
```

### 2.3 值类型及引用类型
Golang的类型系统与Java相差不大，但是需要注意的是Java中的数组是属于引用类型，而Golang中的数组属于值类型，当向方法中传递数组时，Java可以直接通过该传入的数组修改原数组内部值（浅拷贝），但Golang则会完全复制出一份副本来进行修改（深拷贝）：

- Java
```
public static void main(String[] args) {
    int[] array = {1, 2, 3};
    change(array);
    System.out.println(Arrays.toString(array)); // -1,2,3
}

private static void change(int[] array) {
    array[0] = -1;
}
```
- Golang
```
func main() {
	array := [...]int{1, 2, 3}
	change(array)
	fmt.Println(array) // 1,2,3
}

func change(array [3]int) {
	array[0] = -1
}
```
并且值得注意的是，在Golang中，只有同长度、同类型的数组才可视为“同一类型”，譬如 [2]int 和 [3]int 则会被视为不同的类型，这在参数传递的时候会造成编译错误。

所以在Golang中数组很少被直接使用，更多的是使用切片（基于数组指针）来代替数组。

在Golang中，只有切片、指针、channel、map及func属于引用类型，也就是在传递参数的时候，实质上复制的都是他们的指针，内部的修改会直接影响到外部：
```
func main() {
	slice := []int{1, 2, 3}
	changeSlice(slice)
	fmt.Println(slice) // -1,2,3

	mapper := map[string]int {
		"num": 0,
	}
	changeMap(mapper)
	fmt.Println(mapper) // num = -1

	array := [...]int{1, 2, 3}
	changePointer(&array)
	fmt.Println(array) // -1,2,3

	intChan := make(chan int, 1)
	intChan <- 1
	changeChannel(intChan)
	fmt.Println(<- intChan) // -1
}

func changeChannel(intChan chan int) {
	<- intChan
	intChan <- -1
}

func changePointer(array *[3]int) {
	array[0] = -1
}

func changeMap(mapper map[string]int) {
	mapper["num"] = -1
}

func changeSlice(array []int) {
	array[0] = -1
}
```
## 三、结构体、函数及指针
### 3.1 结构体声明及使用
在Golang中区别与Java最显著的一点是，Golang不存在“类”这个概念，组织数据实体的结构在Golang中被称为结构体。函数可以脱离“类”而存在，函数可以依赖于结构体来调用或者依赖于包名调用。

Golang中的结构体放弃了继承、实现等多态概念，结构体之间可使用组合来达到复用方法或者字段的效果。

要声明一个结构体只需使用 type + struct 关键字即可：
```
type Person struct {
	Name string
	Age  int
	id   string
}
```
要使用一个结构体也很简单，一般有以下几种方式去创建结构体：
```
personPoint := new(entity.Person) // 通过new方法创建结构体指针
person1 := entity.Person{} // 通过Person{}创建默认字段的结构体
person2 := entity.Person{ // 通过Person{Name:x,Age:x}创建结构体并初始化特定字段
	Name: "ARong",
	Age:  21,
}
fmt.Println(personPoint) // &{ 0 }
fmt.Println(person1)     // { 0 }
fmt.Println(person2)	 // {ARong 21 }
```
### 3.2 函数和方法的区别
使用Java的朋友应该很少使用“函数”这个词，因为对于Java来说，所有的“函数”都是基于“类”这个概念构建的，也就是只有在“类”中才会包含所谓的“函数”，这里的“函数”被称为“方法”。

而“函数”这个词源于面向过程的语言，所以在Golang中，“函数”和“方法”的最基本区别是：

**函数不基于结构体而是基于包名调用，方法基于结构体调用**。

下面是一个例子，可以直观地看出方法和函数的区别：
- entity
```
package entity

import "fmt"

type Person struct {
	Name string
	Age  int
	id   string
}

// Person结构体/指针可调用的"方法"，属于Person结构体
func (p *Person) Solve() {
	fmt.Println(p)
}

// 任何地方都可调用的"函数"，不属于任何结构体，可通过entity.Solve调用
func Solve(p *Person) {
	fmt.Println(p)
}
```
- main
```
func main() {
	personPoint := new(entity.Person) // 通过new方法创建结构体指针

	entity.Solve(personPoint) // 函数调用
	
	personPoint.Solve() 	  // 方法调用
}
```
### 3.3 指针的使用
在Java中不存在显式的指针操作，而Golang中存在显式的指针操作，但是Golang的指针不像C那么复杂，不能进行指针运算。

下面从一个例子来看Java的隐式指针转化和Golang的显式指针转换：Java和Golang方法传参时传递的都是值类型，在Java中如果传递了引用类型（对象、数组等）会复制其指针进行传递， 而在Golang中必须要显式传递Person的指针，不然只是传递了该对象的一个副本。

**Golang使用 * 来定义和声明指针，通过&来取得对象的指针**。
```
func main() {
	p1 := entity.Person{
		Name: "ARong1",
		Age:  21,
	}
	changePerson(p1)
	fmt.Println(p1.Name) // ARong1
	changePersonByPointer(&p1)
	fmt.Println(p1.Name) // ARong2
}

func changePersonByPointer(person *entity.Person) {
	person.Name = "ARong2"
}

func changePerson(person entity.Person) {
	person.Name = "ARong2"
}
```
注意，如果结构体中需要组合其他结构体，那么建议采用指针的方式去声明，否则会出现更新丢失问题。

以下是Golang方法的一个隐式指针转换，结构体调用方法时，如果传递的是对象，那么会被自动转化为指针调用：
```

type Person struct {
	Name string
	Age  int
}

// Person结构体/指针可调用的"方法"，属于Person结构体
func (p *Person) Solve() {
	fmt.Println(p)
}


func main() {
	p := entity.Person{
		Name: "ARong",
		Age:  21,
	}
	
	pp := &p
	pp.Solve() // 显式
	
	p.Solve    // 隐式，自动将p转化为&p
}
```

## 四、面向对象
### 4.1 与Java面向对象的区别
Golang是一门具备面向对象编程风格的语言，但是却不具备Java等传统面向对象语言中“继承（extends）、实现（implements）”的关键字。

在Golang中，通过接口或结构体的组合来实现非严格的“继承”，通过非侵入式的接口来实现非严格的“多态”，通过结构体及包和函数实现了代码细节的“封装”，有了封装、继承与多态，就可以很好地通过OO思维实现与现实需求所对应的程序了。

### 4.2 结构体组合
假设有这么一个场景：动物（Animal）具备名字（Name）、年龄（Age）的基本特性，现在需要实现一个Dog类型，且Dog类型需要具备Animal所需的所有特性，并且自身具备犬吠（bark()）的方法，使用Java和Golang来实现该场景会有什么区别呢？

首先来看看最熟悉的Java要如何写，很简单，使用抽象类描述Animal作为所有动物的超类，Dog extends Animal：
- Java
```
public abstract class Animal {
    protected String name;
    protected int age;
}

public class Dog extends Animal {
    public void bark() {
        System.out.println(age + "岁的" + name + "在汪汪汪...");
    }
}

public class Test {
    public static void main(String[] args) {
        Dog dog = new Dog();
        dog.name = "tom";
        dog.age = 2;
        dog.bark(); // 2岁的tom在汪汪汪...
    }
}
```
在Golang中，可以这样通过结构体的组合来实现继承：

- Golang
```
package oom

type Animal struct {
	Name string
	Age int
}

type Dog struct {
	*Animal
}

func (d *Dog) Bark() {
	fmt.Printf("%d岁的%s在汪汪汪...", d.Age, d.Name)
}

// ----------
package main

func main() {
	dog := &oom.Dog{&oom.Animal{
		Name: "tom",
		Age:  2,
	}}
	dog.Bark() // 2岁的tom在汪汪汪...
}
```
但是这种方式实现的继承是有缺陷的，也就是不具备多态的性质，Dog属于Animal，但是Dog并不是Animal，在方法中定义了Animal参数，Dog是无法作为该参数传入的。

**Golang使用了非侵入式接口来实现“多态”**。

### 4.3 非侵入式接口
Go语言的接口并不是其他语言（C++、Java、C#等）中所提供的接口概念。
在Go语言出现之前，接口主要作为不同组件之间的契约存在。对契约的实现是强制的，你必须声明你的确实现了该接口。为了实现一个接口，你需要从该接口继承：
```
interface IFoo {
    void Bar();
}

class Foo implements IFoo { // Java文法
// ...
}

class Foo : public IFoo { // C++文法
// ...
}

IFoo foo = new Foo;
```
这类接口我们称为侵入式接口。“侵入式”的主要表现在于实现类需要明确声明自己实现了某个接口。这种强制性的接口继承是面向对象编程思想发展过程中一个遭受相当多置疑的特性。

**Golang的非侵入式接口不需要通过任何关键字声明类型与接口之间的实现关系，只要一个类型实现了接口的所有方法，那么这个类型就是这个接口的实现类型**。

假设现在有一个Factory接口，该接口中定义了Produce()方法及Consume()方法，CafeFactory结构体作为其实现类型，那么可以通过以下代码实现：
```
package oom

type Factory interface {
	Produce() bool
	Consume() bool
}

type CafeFactory struct {
	ProductName string
}

func (c *CafeFactory) Produce() bool {
	fmt.Printf("CafeFactory生产%s成功", c.ProductName)
	return true
}

func (c *CafeFactory) Consume() bool {
	fmt.Printf("CafeFactory消费%s成功", c.ProductName)
	return true
}

// --------------
package main

func main() {
	factory := &oom.CafeFactory{"Cafe"}
	doProduce(factory)
	doConsume(factory)
}


func doProduce(factory oom.Factory) bool {
	return factory.Produce()
}

func doConsume(factory oom.Factory) bool {
	return factory.Consume()
}
```
可以看到，只要CafeFactory实现了所有的Factory方法，那么它就是一个Factory了，而不需要使用implements关键字去显式声明它们之间的实现关系。

Golang的非侵入式接口有许多好处：

1.在Go中，类型的继承树并无意义，我们只需要知道这个类型实现了哪些方法，每个方法是啥含义就足够了

2.实现类型的时候，只需要关心自己应该提供哪些方法，不用再纠结接口需要拆得多细才合理。接口由使用方按需定义，而不用事前规划

3.不用为了实现一个接口而导入一个包，因为多引用一个外部的包，就意味着更多的耦合。接口由使用方按自身需求来定义，使用方无需关心是否有其他模块定义过类似的接口

一句话总结非侵入式接口的好处就是简单、高效、按需实现。

### 4.4 interface{} 空接口
interface{} 空接口是任意类型的接口，所有的类型都是空接口的实现类型。因为Golang对于实现类型的要求是实现了接口的所有方法，而空接口不存在方法，所以任意类型都可以充当空接口。有点类似Java的Object。

以下是一个使用空接口充当参数的类型判断例子：
```
func getType(key interface{}) string {
	switch key.(type) {
		case int:
			return "this is a integer"
		case string:
			return "this is a string"
		default:
			return "unknown"
	}
}
```

## 五、异常处理
### 5.1 与Java异常处理的区别
在Java中通过`try..catch..finally`的方式进行异常处理，有可能出现异常的代码会被`try`块给包裹起来，在`catch`中捕获相关的异常并进行处理，最后通过`finally`块来统一执行最后的结束操作（释放资源、释放锁）。

而Golang中的异常处理（更贴切地说是错误处理）方式比Java的简单太多，所有可能出现异常的方法或者代码直接把错误当作第二个响应值进行返回，程序中对返回值进行判断，非空则进行处理并且立即中断程序的执行，避免错误的传播。
```
value, err := func(param)

if err != nil {
    // 返回了异常，进行处理
    fmt.Printf("Error %s in pack1.Func1 with parameter %v", err.Error(), param1)
    return err
}

// func执行正确，继续执行后续代码
Process(value)
```
Golang引入了一个关于错误处理的标准模式，即error接口，该接口的定义如下：
```
type error interface {
	Error() string
}
```
对于大多数函数，如果要返回错误，大致上都可以定义为如下模式，将 error 作为多种返回值中的最后一个，但这并非是强制要求：
```
unc main() {
	if res, err := compute(1, 2, "x"); err != nil {
		panic(err)
	} else {
		fmt.Println(res)
	}
}

func compute(a, b int, c string)(res int, err error) {
	switch c {
	case "+" :
		return a + b, nil
	case "-":
		return a - b, nil
	case "*":
		return a * b, nil
	case "/":
		return a / b, nil
	default:
		return -1, fmt.Errorf("操作符不合法")
	}
}
```
当然了，Golang中也可以像Java一样灵活地自定义错误类型，定义PathError结构体，并且实现Error接口后，该结构体就是一个错误类型了：
- PathError
```
type PathError struct {
	Op string
	Path string
	Err error
}

func (e *PathError) Error() string {
	return e.Op + " " + e.Path + ": " + e.Err.Error()
}
```
- main
```
func GetStat(name string) (fi FileInfo, err error) {
    var stat syscall.Stat_t
    err = syscall.Stat(name, &stat)
    if err != nil {
        // 返回PathError错误类型
        return nil, &PathError {"stat", name, err}
    }
    // 程序正常，返回nil
    return fileInfoFromStat(&stat, name), nil
}
```
这种异常处理方式是Golang的一大特色，外界对这种异常处理方式有褒有贬：

优点：代码清晰，所有的异常都需要被考虑到，出现异常后马上就需要处理

缺点：代码冗余，所有的异常都需要通过if err != nil {}去做判断和处理，不能够做到统一捕捉和处理

### 5.2 逗号 ok 模式
在使用Golang编写代码的过程中，许多方法经常在一个表达式返回2个参数时使用这种模式：,ok，第一个参数是一个值或者nil，第二个参数是true/false或者一个错误error。在一个需要赋值的if条件语句中，使用这种模式去检测第二个参数值会让代码显得优雅简洁。这种模式在Golang编码规范中非常重要。这也是Golang自身的函数多返回值特性的体现。

### 5.3 defer、panic及recover
defer、pannic及recover是Golang错误处理中常用的关键字，它们各自的用途为:

#### 1. defer

defer的作用是延迟执行某段代码，一般用于关闭资源或者执行必须执行的收尾操作，无论是否出现错误defer代码段都会执行，类似于Java中的finally代码块的作用：
```
     func CopyFile(dst, src string) (w int64, err error) {
        srcFile, err := os.Open(src)
        if err != nil {
            return
        }
        // 延迟关闭srcFile
        defer srcFile.Close()
        dstFile, err := os.Create(dstName)
        if err != nil {
            return
        }
        // 延迟关闭dstFile
        defer dstFile.Close()
        return io.Copy(dstFile, srcFile)
    }
```
defer也可以执行函数或者是匿名函数:
```
defer func() {
	// 清理工作
} ()

// 这是传递参数给匿名函数时的写法
var i := 1
defer func(i int) {
	// 做你复杂的清理工作
} (i)
```
需要注意的是，defer使用一个栈来维护需要执行的代码，所以defer函数所执行的顺序是和defer声明的顺序相反的。
```
defer fmt.Println(1)
defer fmt.Println(2)
defer fmt.Println(3)
// 执行结果
// 3
// 2
// 1
```

#### 2. panic
panic的作用是抛出错误，制造系统运行时恐慌，当在一个函数执行过程中调用panic()函数时，正常的函数执行流程将立即终止，但函数中之前使用defer关键字延迟执行的语句将正常展开执行，之后该函数将返回到调用函数，并导致逐层向上执行 panic流程，直至所属的goroutine中所有正在执行的函数被终止。

panic和Java中的throw关键字类似，用于抛出错误，阻止程序执行。

以下是基本使用方法:
```
panic(404)
panic("network broken")
panic(Error("file not exists"))
```

#### 3. recover
recover的作用是捕捉panic抛出的错误并进行处理，需要联合defer来使用，类似于Java中的catch代码块：
```
func main() {
      fmt.Println("main begin")
      // 必须要先声明defer，否则不能捕获到panic异常
      defer func() { 
        fmt.Println("defer begin")
        if err := recover(); err != nil {
            // 这里的err其实就是panic传入的内容
            fmt.Println(err) 
        }
         fmt.Println("defer end")
      }()
      f()
      // f中出现错误，这里开始下面代码不会再执行
      fmt.Println("main end") 
}

func f() {
   fmt.Println("f begin")
   panic("error")
   //这里开始下面代码不会再执行
   fmt.Println("f end") 
}
```
最后的执行结果为:
```
main begin
f begin
defer begin
error
defer end
```
**利用recover处理panic指令，defer必须在panic之前声明，否则当panic时，recover无法捕获到panic。**

## 六、并发编程
### 6.1 CSP（MPG）并发模型介绍及对比
在Java中，通常借助于共享内存（全局变量）作为线程间通信的媒介，但在Golang中使用的是通道（channel）作为协程间通信的媒介，这也是Golang中强调的:

**不要通过共享内存通信，而通过通信来共享内存**

在Java中，使用共享内存来进行通信常会遇到线程不安全问题，所以我们经常需要进行大量的额外处理，方式包括加锁（同步化）、使用原子类、使用volatile提升可见性等等。

CSP是Communicating Sequential Processes 的缩写，中文为顺序通信进程。CSP的核心思想是多个线程之间通过Channel来通信（对应到golang中的chan结构），这里的Channel可以理解为操作系统中的管道或者是消息中间件(不同之处在于这个MQ是为不同协程间服务的，而不是进程)

说到了CSP就得提一下Golang自身的并发模型MPG，MPG中M指的是内核线程、P指的是上下文环境、G指的是协程，其中M与P一起构成了G可运行的环境，M和P是一一对应关系，通过P来动态地对不同的G做映射和控制，所以Golang中的协程是建立在某个线程之上的用户态线程。

### 6.2 Goroutine及Channel的使用
在Java中开启一个线程需要创建Thread实现类或Runnable实现类、重写run方法、通过t.start()开启线程执行特定任务，但在Golang中要开启一个Goroutine十分简单，只需使用go这个关键字即可。
```
// 开启协程执行一段代码
go fmt.Println("go")

// 开启协程执行函数
go SomeMethod(1, 1)

// 开启协程执行匿名函数
go func() {
    go fmt.Println("go")
}()
```
关于协程，有一些注意点:

1. main函数运行的协程为主协程，其他协程为主协程的守护协程，当主协程死亡其它协程也会死亡
2. 协程在执行完所需执行的方法及代码后会死亡，遇到panic导致程序结束时也会死亡

channel是Golang在语言级别提供的goroutine间的通信方式。我们可以使用channel在两个或多个goroutine之间传递消息,因此通过channel传递对象的过程和调用函数时的参数传递行为比较一致，比如也可以传递指针等。

channel是类型相关的。也就是说，一个channel只能传递一种类型的值，这个类型需要在声明channel时指定。

一般channel的声明形式为：
```
var chanName chan ElementType
```
与一般的变量声明不同的地方仅仅是在类型之前加了chan关键字。 ElementType 指定这个channel所能传递的元素类型。举个例子，我们声明一个传递类型为 int channel：
```
var ch chan int
```
或者，我们声明一个 map ，元素是 bool 型的channel:
```
var m map[string] chan bool
```
初始化一个channel也很简单，直接使用内置的函数 make() 即可：
```
ch := make(chan int)
```
在channel的用法中，最常见的包括写入和读出。将一个数据写入（发送）至channel的语法很直观，如下：
```
ch <- value
```
向channel写入数据通常会导致程序阻塞，直到有其他goroutine从这个channel中读取数据。从channel中读取数据的语法是
```
value := <-ch
```
如果channel之前没有写入数据，那么从channel中读取数据也会导致程序阻塞，直到channel中被写入数据为止。我们之后还会提到如何控制channel只接受写或者只允许读取，即单向channel。

channel有如下特性：

1. 读取、写入操作为原子操作，无需担心并发时的数据安全问题，channel内数据的写入对所有协程可见
2. channel中阻塞的协程是FIFO的，严格按照入队顺序读写数据
3. 对于非缓冲channel的读取和写入是同步发生的，写入会阻塞直到有读者，读取会阻塞直到有写者，类似于Java中的synchronousqueue；对于缓冲channel的读取和写入是异步的，写入时若队列已满则阻塞，直到有读者，读取时若队列为空则阻塞，直到有写者，类似于Java中的linkedblockingqueue
4. 对于为nil的channel的写入和读取都会永久阻塞

## 七、垃圾回收
### 7.1 Java的垃圾回收体系
Java基于JVM完成了垃圾收集的功能，其体系很庞大，包括了垃圾回收器（G1、CMS、Serial、ParNew等）、垃圾回收算法(标记-清除、标记-整理、复制、分代收集)、可达性算法(可达性分析、引用计数法)、引用类型、JVM内存模型等内容。

### 7.2 Golang三色标记法
三色标记法，主要流程如下：

1. 所有对象最开始都是白色
2. 从root开始找到所有可达对象，标记为灰色，放入待处理队列
3. 遍历灰色对象队列，将其引用对象标记为灰色放入待处理队列，自身标记为黑色
4. 处理完灰色对象队列，执行清扫工作