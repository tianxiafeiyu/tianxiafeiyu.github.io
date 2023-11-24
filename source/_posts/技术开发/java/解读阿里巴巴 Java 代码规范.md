---
title: 解读阿里巴巴 Java 代码规范
date: 2022-12-15 23:41:31
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 解读阿里巴巴 Java 代码规范
---
转载自 https://developer.ibm.com/zh/articles/deconding-code-specification-part-1/

## 前言
2017 年阿里云栖大会，阿里发布了针对 Java 程序员的《阿里巴巴 Java 开发手册（终极版）》，这篇文档作为阿里数千位 Java 程序员的经验积累呈现给公众，并随之发布了适用于 Eclipse 和 Intellim 的代码检查插件。为了能够深入了解 Java 程序员编码规范，也为了深入理解为什么阿里这样规定，是否规定有误，本文以阿里发布的这篇文档作为分析起源，扩大范围至业界其他公司的规范，例如谷歌、FaceBook、微软、百度、华为，并搜索网络上技术大牛发表的技术文章，深入理解每一条规范的设计背景和目标。

由于解读文章仅有两篇，所以按照阿里的篇幅权重分为上篇仅针对 Java 语言本身的编码规约，下篇包含日志管理、异常处理、单元测试、MySQL 规范、工程规范等方面内容进行解读。本文是上篇，主要针对编码规约部分进行解读，由于篇幅限制，仅挑选一小部分进行解读，如果需要全篇，请联系本文作者。

## 一、编码规约
### 命名风格
#### 1. 下划线或者美元符号
阿里强制规定代码中的命名均不能以下划线或美元符号开始，也不能以下划线或美元符号结束。

反例：`_name/__name/$Object/name_/name$/Object$`

**我的理解：**

Oracle 官网建议不要使用`$`或者`_`开始变量命名，并且建议在命名中完全不要使用”$”字符，原文是”The convention,however,is to always begin your variable names with a letter,not ‘$’ or ‘‘”。对于这一条，腾讯的看法是一样的，百度认为虽然类名可以支持使用”$”符号，但只在系统生成中使用（如匿名类、代理类），编码不能使用。

这类问题在 StackOverFlow 上有很多人提出，主流意见为人不需要过多关注，只需要关注原先的代码是否存在”_“，如果存在就继续保留，如果不存在则尽量避免使用。也有一位提出尽量不适用”“的原因是低分辨率的显示器，肉眼很难区分`_`（一个下划线）和`__`（两个下划线）。

我个人觉得可能是由于受 C 语言的编码规范所影响。因为在 C 语言里面，系统头文件里将宏名、变量名、内部函数名用开头，因为当你#include 系统头文件时，这些文件里的名字都有了定义，如果与你用的名字冲突，就可能引起各种奇怪的现象。综合各种信息，建议不要使用`_`、`$`、空格作为命名开始，以免不利于阅读或者产生奇怪的问题。

#### 2. 类命名
阿里强制规定类名使用 UpperCamelCase 风格，必须遵从驼峰形式，但以下情形例外：DO/BO/DTO/VO/AO。 

正例：`MarcoPolo/UserDO/XmlService/TcpUdpDeal/TarPromotion`

反例：`macroPolo/UserDo/XMLService/TCPUDPD/TAPromotion`

**我的理解：**

百度除了支持阿里的规范以外，规定虽然类型支持”$”符号，但只在系统生成中使用（如匿名类、代理类），编码中不能使用。

对于类名，俄罗斯 Java 专家 Yegor Bugayenko 给出的建议是尽量采用现实生活中实体的抽象，如果类的名字以”-er”结尾，这是不建议的命名方式。他指出针对这一条有一个例外，那就是工具类，例如 StringUtils、FileUtils、IOUtils。对于接口名称，不要使用 IRecord、IfaceEmployee、RedcordInterface，而是使用现实世界的实体命名。如清单 3 所示。

清单 3 示例
```
Class SimpleUser implements User{};
Class DefaultRecord implements Record{};
Class Suffixed implements Name{};
Class Validated implements Content{};
```

#### 3. 抽象类的命名
阿里强制规定抽象类命名使用 Abstratc 或 Base 开头。

**我的理解：**

Oracle 的抽象类和方法规范并没有要求必须采用 Abstract 或者 Base 开头命名，事实上官网上的示例没有这种命名规范要求，如清单 4 所示。

清单 4 示例：
```java
public abstract class GraphicObject{
    //declare fields
    //declare nonabstract methods
    abstract void draw();
}
```
我也查了一下 JDK，确实源码里很多类都是以这样的方式命名的，例如抽象类 java.util.AbstractList。

Stackoverflow 上对于这个问题的解释是，由于这些类不会被使用，一定会由其他的类继承并实现内部细节，所以需要明白地告诉读者这是一个抽象类，那以 Abstract 开头比较合适。

JoshuaBloch的理解是支持以 Abstract 开头。我的理解是不要以 Base 开头命名，因为实际的基类也以 Base 开头居多，这样意义有多样性，不够直观。

### 常量定义
#### 1. 避免魔法值的使用
阿里强制规定不允许任何魔法值（未经定义的常量）直接出现在代码中。

反例：
```java
String key = "Id#taobao_" + tradeId；
cache.put(key,value);
```

**我的理解：**

魔法值确实让你很疑惑，比如你看下面这个例子：

int priceTable[] = new int[16];//这样定义错误；这个 16 究竟代表什么？

正确的定义方式是这样的：

static final int PRICE_TABLE_MAX = 16; //这样定义正确，通过使用完整英语单词的常量名明确定义

int price Table[] = new int[PRICE_TABLE_MAX];

魔法值会让代码的可读性大大降低，而且如果同样的数值多次出现时，容易出现不清楚这些数值是否代表同样的含义。另一方面，如果本来应该使用相同的数值，一旦用错，也难以发现。因此可以采用以下两点，极力避免使用魔法数值。
1. 不适用魔法数值，使用带名字的 Static final 或者 enum 值；
2. 原则上 0 不用于魔法值，这是因为 0 经常被用作数组的最小下标或者变量初始化的缺省值。

#### 2. 变量值范围
阿里推荐如果变量值仅在一个范围内变化，且带有名称之外的延伸属性，定义为枚举类。下面这个正例中的数字就是延伸信息，表示星期几。

正例：
```java
public Enum {MONDAY(1),TUESDAY(2),WEDNESDAY(3),THURSDAY(4),FRIDAY(5),SATURDAY(6),SUNDAY(7);}
```

**我的理解：**

对于固定并且编译时对象，如 Status、Type 等，应该采用 enum 而非自定义常量实现，enum 的好处是类型更清楚，不会再编译时混淆。这是一个建议性的试用推荐，枚举可以让开发者在 IDE 下使用更方便，也更安全。另外就是枚举类型是一种具有特殊约束的类类型，这些约束的存在使得枚举类本身更加简洁、安全、便捷。

### 代码格式
#### 1. 大括号的使用约定
阿里强制规定如果是大括号为空，则简洁地写成{}即可，不需要换行；如果是非空代码块则遵循如下原则：
1. 左大括号前不换行
2. 左大括号后换行
3. 右大括号前换行
4. 右大括号后还有 else 等代码则不换行表示终止的右大括号后必须换行

正例：
```java
try{
    // try to do...
}catch(Exception e){
    // do somthing...
}finally{
    // do somthing...
}
```

**我的理解：**

阿里的这条规定应该是参照了 SUN 公司 1997 年发布的代码规范（SUN 公司是 JAVA 的创始者），Google 也有类似的规定，大家都是遵循 K&R 风格（Kernighan 和 Ritchie），Kernighan 和 Ritchie 在《The C Programming Language》一书中推荐这种风格，JAVA 语言的大括号风格就是受到了 C 语言的编码风格影响。

注意，SUN 公司认为方法名和大括号之间不应该有空格。

#### 2. 单行字符数限制
阿里强制规定单行字符数限制不超过 120 个，超出需要换行，换行时遵循如下原则：
1. 第二行相对第一行缩进 4 个空格，从第三行开始，不再继续缩进，参考示例。
2. 运算符与下文一起换行。
3. 方法调用的点符号与下文一起换行。
4. 方法调用时，多个参数，需要换行时，在逗号后进行。
5. 在括号前不要换行，见反例。

正例：
```java
StringBuffer sb = new StringBuffer();
//超过 120 个字符的情况下，换行缩进 4 个空格，点号和方法名称一起换行
sb.append("zi").append("xin")...
    .append("huang")...
    .append("huang")...
    .append("huang")...
```

反例：
```java
StringBuffer sb = new StringBuffer();
//超过 120 个字符的情况下，不要在括号前换行
sb.append("zi").append("xin").append
("huang");
//参数很多的方法调用可能超过 120 个字符，不要在逗号前换行
method(args1,args2,args3,....,argsX);
```

**我的理解：**
SUN 公司 1997 年的规范中指出单行不要超过 80 个字符，对于文档里面的代码行，规定不要超过 70 个字符单行。当表达式不能在一行内显示的时候，遵循以下原则进行切分：
1. 在逗号后换行；
2. 在操作符号前换行；
3. 倾向于高级别的分割；
4. 尽量以描述完整作为换行标准；
5. 如果以下标准造成代码阅读困难，直接采用 8 个空格方式对第二行代码留出空白。

### OOP 规约

#### 1. 静态变量及方法调用
阿里强制规定代码中避免通过一个类的对象引用访问此类的静态变量或静态方法，无谓增加编译器解析成本，直接用类名来访问即可。

**我的理解：**

谷歌公司在代码规范中指出必须直接使用类名对静态成员进行引用。并同时举例说明，如清单 9 所示。

清单 9 示例：
```java
Foo aFoo = …;
Foo.aStaticMethod();//good
aFoo.aStaticMethod();//bad
somethingThatYieldsAFoo().aStaticMethod();//very bad
```
SUN 公司 1997 年发布的代码规范也做了类似的要求。

为什么需要这样做呢？因为被 static 修饰过的变量或者方法都是随着类的初始化产生的，在堆内存中有一块专门的区域用来存放，后续直接用类名访问即可，避免编译成本的增加和实例对象存放空间的浪费。

StackOverflow 上也有人提出了相同的疑问，网友较为精辟的回复是"**这是由于生命周期决定的，静态方法或者静态变量不是以实例为基准的，而是以类为基准，所以直接用类访问，否则违背了设计初衷**"。那为什么还保留了实例的访问方式呢？可能是因为允许应用方无污染修改吧。

#### 2. 可变参数编程
阿里强制规定相同参数类型、相同业务类型，才可以使用 Java 的可变参数，避免使用 Object，并且要求可变参数必须放置在参数列表的最后（提倡同学们尽量不用可变参数编程）。

**我的理解：**
我们先来了解可变参数的使用方式：

1. 在方法中定义可变参数后，我们可以像操作数组一样操作该参数。
2. 如果该方法除了可变参数还有其他的参数，可变参数必须放到最后。
3. 拥有可变参数的方法可以被重载，在被调用时，如果能匹配到参数定长的方法则优先调用参数定长的方法。
4. **可变参数可以兼容数组参数，但数组参数暂时无法兼容可变参数**。

至于为什么可变参数需要被放在最后一个，这是因为参数个数不定，所以当其后还有相同类型参数时，编译器无法区分传入的参数属于前一个可变参数还是后边的参数，所以只能让可变参数位于最后一项。

可变参数编程有一些好处，例如反射、过程建设、格式化等。对于阿里同学提出的尽量不使用可变参数编程，我猜测的原因是不太可控，比如 Java8 推出 Lambda 表达式之后，可变参数编程遇到了实际的实现困难。

### 并发处理
#### 1. 单例模式需要保证线程安全
阿里强制要求获取单例对象需要保证线程安全，其中的方法也要保证线程安全，并进一步说明资源驱动类、工具类、单例工厂类都需要注意。

**我的理解：**

对于这一条规范是通识化规定，我这里进一步讲讲如何做好针对单例对象的线程安全，主要有以下几种方式：

**1. 方法中申明 synchronized 关键字**
 
出现非线程安全问题，是由于多个线程可以同时进入 getInstance()方法，那么只需要对该方法进行 synchronized 锁同步即可，如清单 15 所示。
 
```java
 // 清单 15 synchronized 关键字方式
 
 public class MySingleton{
     private static MySingleton instance = null;
     private MySingleton(){}
     public synchronized static MySingleton getInstance(){
         try{
             if(instance != null){//懒汉式
             }else{
             //创建实例之前可能会有一些准备性的耗时工作
             Thread.sleep(500);
             Instance = new MySingleton();
             }
         }catch(InterruptedException e){
            e.printStackTrace();
         }
         return instance;
     }
} 
```
从执行结果上来看，多线程访问的问题已经解决了，返回的是一个实例。但是这种实现方式的运行效率很低。我们接下来采用同步方法块实现。
 
**2. 2. 同步方法块实现**

```java
public class MySingleton { 
    private static MySingleton instance = null; 
    private MySingleton(){} 
    
    public static MySingleton getInstance() { 
        try { 
            synchronized (MySingleton.class) {          
                if(instance != null){//懒汉式   
                }else{      
                    //创建实例之前可能会有一些准备性的耗时工作 
                    Thread.sleep(300); 
                    instance = new MySingleton(); 
                } 
            }        
        } catch (InterruptedException e) { 
            e.printStackTrace(); 
        } 
        return instance; 
    } 
}
```
这里的实现能够保证多线程并发下的线程安全性，但是这样的实现将全部的代码都被锁上了，同样的效率很低下。

**3. 针对某些重要的代码来进行单独的同步:**

针对某些重要的代码进行单独的同步，而不是全部进行同步，可以极大的提高执行效率。
```java
public class MySingleton { 
    private static MySingleton instance = null; 
    private MySingleton(){} 
    
    public static MySingleton getInstance() { 
        try { 
            if(instance != null){//懒汉式                    
            }else{  
                //创建实例之前可能会有一些准备性的耗时工作 
                Thread.sleep(300); 
                synchronized (MySingleton.class) { 
                instance = new MySingleton(); 
                } 
            } 
        }catch (InterruptedException e) { 
            e.printStackTrace(); 
        } 
        return instance; 
    } 
}
```
从运行结果来看，这样的方法进行代码块同步，代码的运行效率是能够得到提升，但是却没能保住线程的安全性。看来还得进一步考虑如何解决此问题。

**4. 双检查锁机制（Double Check Locking）**

为了达到线程安全，又能提高代码执行效率，我们这里可以采用 DCL 的双检查锁机制来完成。

```java
public class MySingleton { 
    //使用 volatile 关键字保其可见性 
    volatile private static MySingleton instance = null; 
    private MySingleton(){} 
    
    public static MySingleton getInstance() { 
        try { 
            if(instance != null){//懒汉式 
            }else{ 
                //创建实例之前可能会有一些准备性的耗时工作  
                Thread.sleep(300); 
                synchronized (MySingleton.class) { 
                    if(instance == null){//二次检查  
                        instance = new MySingleton(); 
                    } 
                } 
            } 
        } catch (InterruptedException e) { 
            e.printStackTrace(); 
        } 
        return instance; 
    } 
}
```
这里在声明变量时使用了 volatile 关键字来保证其线程间的可见性；在同步代码块中使用二次检查，以保证其不被重复实例化。集合其二者，这种实现方式既保证了其高效性，也保证了其线程安全性。

**5. 静态内置类方式**

DCL 解决了多线程并发下的线程安全问题，其实使用其他方式也可以达到同样的效果

```java
public class MySingleton {          
    //内部类 
    private static class MySingletonHandler{ 
        private static MySingleton instance = new MySingleton(); 
    } 
    
    private MySingleton(){} 
    
    public static MySingleton getInstance() { 
        return MySingletonHandler.instance; 
    } 
}
```

**6. 序列化与反序列化方式**

静态内部类虽然保证了单例在多线程并发下的线程安全性，但是在遇到序列化对象时，默认的方式运行得到的结果就是多例的。

```java
import java.io.Serializable; 
public class MySingleton implements Serializable { 
    private static final long serialVersionUID = 1L; 
    
    //内部类  
    private static class MySingletonHandler{ 
        private static MySingleton instance = new MySingleton(); 
    } 
    
    private MySingleton(){} 
    
    public static MySingleton getInstance() { 
        return MySingletonHandler.instance; 
    } 
}
```

**7. 使用枚举数据类型方式**

枚举 enum 和静态代码块的特性相似，在使用枚举时，构造方法会被自动调用，利用这一特性也可以实现单例。

```java
public enum EnumFactory{ 
    singletonFactory;
    
    private MySingleton instance; 
    
    private EnumFactory(){//枚举类的构造方法在类加载是被实例化
        instance = new MySingleton(); 
    } 
    
    public MySingleton getInstance(){ 
        return instance; 
    } 
} 
    
class MySingleton{//需要获实现单例的类，比如数据库连接 Connection  
    public MySingleton(){} 
}
```
这样写枚举类被完全暴露了，据说违反了"职责单一原则"，我们可以按照下面的代码改造。

```java
public class ClassFactory{ 
    private enum MyEnumSingleton{ 
        singletonFactory; 
        private MySingleton instance; 
        
        private MyEnumSingleton(){//枚举类的构造方法在类加载是被实例化 
            instance = new MySingleton(); 
        } 
        
        public MySingleton getInstance(){ 
            return instance; 
        } 
    } 
    
    public static MySingleton getInstance(){ 
        return MyEnumSingleton.singletonFactory.getInstance(); 
    } 
} 

class MySingleton{//需要获实现单例的类，比如数据库连接 Connection  
 public MySingleton(){} 
}
```

> 不太理解这种写法，为什么不直接把单例类改成枚举呢？？（2020.11.12）

```java
public enum MySingleton{ 
    instance;
    
    private MySingleton(){
    
    } 
} 
```

### 控制语句

#### 1. Switch 语句的使用
阿里强制规定在一个 switch 块内，每个 case 要么通过 break/return 等来终止，要么注释说明程序将继续执行到哪一个 case 为止；在一个 switch 块内，都必须包含一个 default 语句并且放在最后，即使它什么代码也没有。

**我的理解：**

首先理解前半部分，"每个 case 要么通过 break/return 等来终止，要么注释说明程序将继续执行到哪一个 case 为止"。因为这样可以比较清楚地表达程序员的意图，有效防止无故遗漏的 break 语句。default 语句里面也应该有 break/return。

### 集合处理

#### 1. 集合转数组处理
阿里强制规定使用集合转数组的方法，必须使用集合的 toArray(T[] arrays)，传入的是类型完全一样的数组，大小就是 list.size()。使用 toArray 带参方法，入参分配的数组空间不够大时，toArray 方法内部将重新分配内存空间，并返回新数组地址；如果数组元素大于实际所需，下标为[list.size()]的数组元素将被置为 null，其它数组元素保持原值，因此最好将方法入参数组大小定义与集合元素个数一致。正例如清单 25 所示。

清单 25 正例：
```java
List<String> list = new ArrayList<String>(2);
list.add("guan");
list.add("bao");
String[] array = new String[list.size()];
array = list.toArray(array);
```

### 注释规约

#### 1. 方法注释要求
阿里强制要求方法内部单行注释，在被注释语句上方另起一行，使用//注释。方法内部多行注释使用/**/注释，注意与代码对照。

**我的理解：**

百度规定方法注释采用标准的 Javadoc 注释规范，注释中必须提供方法说明、参数说明及返回值和异常说明。腾讯规定采用 JavaDoc 文档注释，在方法定义之前应该对其进行注释，包括方法的描述、输入、输出以及返回值说明、抛出异常说明、参考链接等。

### 其他

#### 1. 数据结构初始化大小

阿里推荐任何数据结构的构造或初始化，都应指定大小，避免数据结构暂时无限增长吃光内存。

**我的理解：**

首先明确一点，阿里这里指的大小具体是指数据结构的最大长度。大部分 Java 集合类在构造时指定的大小都是初始尺寸（initial Capacity），而不是尺寸上限（Capacity），只有几种队列除外，例如 ArrayBlockingQueue、LinkedBlockingQueue，它们在构造时可以指定队列的最大长度。阿里推荐的目的是为了合理规划内存，避免出现 OOM（Out of Memory）异常。

### 异常处理

#### 1. 不要捕获 RuntimeException
阿里强制规定 Java 类库中的 RuntimeException 可以通过预先检查进行规避，而不应该通过 catch 来处理，例如 IndexOutOfBoundsException、NullPointerException 等。

**我的理解：**

RuntimeException，也被称为运行时异常，通常是由于代码中的 bug 引起的，正确的处理方式是去检查代码，通过添加数据长度判断，判断对象是否为空等方法区规避，而不是靠捕获来规避这种异常。

#### 2. 事务中的异常需要回滚
阿里强制规定有 try 块放到了事务代码中，catch 异常后，如果需要回滚事务，一定要注意手动回滚事务。

**我的理解：**

try catch 代码块中对异常的处理，可能会遗漏事务的一致性，当事务控制不使用其他框架管理时，事务需要手动回滚。实际使用如果引入第三方的框架对事务进行管理，比如 Spring，则根据第三方框架的实际实现情况，确定是否有必要手动回滚。当第三方事务管理框架本身就会对于异常进行抛出时需要做事务回滚。例如 Spring 在@Transactional 的 annotation 注解下，会默认开启运行时异常事务回滚。

#### 3. 不能在 finally 块中使用 return
阿里强制要求 finally 块中不使用 return，因为执行完该 return 后方法结束执行，不会再执行 try 块中的 return 语句。


**我的理解：**

在try-catch-finally中, 当return遇到finally，return对finally无效，即:
1.在try catch块里return的时候，finally也会被执行。
2.finally里的return语句会把try catch块里的return语句效果给覆盖掉。

return语句并不一定都是函数的出口，执行return时，只是把return后面的值复制了一份到返回值变量里去了。所以在finally有return时，会覆盖掉try-catch中的return。

finally语句是不是总会被执行？

答案是否。以下情况finally语句不会执行：
1. try语句没有被执行到，如在try语句之前return就返回了，这样finally语句就不会执行。这也说明了finally语句被执行的必要而非充分条件是：相应的try语句一定被执行到。
2. 在try块|catch块中有System.exit(0);这样的语句。System.exit(0)是终止Java虚拟机JVM的，连JVM都停止了，所有都结束了，当然finally语句也不会被执行到。

### 日志规约

#### 1. 不可直接使用日志系统
阿里强制规定应用中不可直接使用日志系统（Log4j、Logback）中的 API，而应依赖使用日志框架 SLF4J 中的 API，使用门面模式的日志框架，有利于维护和各个类的日志处理方式统一。

**我的理解：**

SLF4J 即简单日志门面模式，不是具体的日志解决方案，它只服务于各种各样的日志系统。在使用 SLF4J 时不需要指定哪个具体的日志系统，只需要将使用到的具体日志系统的配置文件放到类路径下去。

正例代码：
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
public class HelloWorld{
    private static final Logger logger = LoggerFactory.getLogger(HelloWorld.class);

    public static void main(String[] args){
        logger.info("please use SLF4J,rather than logback or log4j");
    }
}
```

反例代码：
```java
import org.apache.log4j.Logger;
public class HelloWorld{
    private static final Logger logger = LoggerFactory.getLogger(HelloWorld.class);
    
    public static void main(String[] args){
        logger.info("please use SLF4J,rather than logback or log4j");
    }
}
```

#### 2. 日志文件保留时间
阿里强制规定日志文件至少保存 15 天，因为有些异常具备以"周"为频次发生的特点。

**我的理解：**

日志保留时间推荐 15 天以上，但是保留时间也不宜过长，一般不超过 21 天，否则造成硬盘空间的浪费。对于一些长周期性执行的逻辑，可以根据实际情况调整该保存时间，同时也需要保证日志能够监控到关键的应用。

对于长周期执行的逻辑，可以使用特定的 appender，并使用不同的日志清理规则，如时间、大小等。如一月执行一次的定时任务，可以将日志输出到新的日志文件，然后通过大小限定的规则进行清理，并不一定要使用时间清理的逻辑。

### 安全规约

#### 1. 权限控制校验
阿里强制要求对于隶属于用户个人的页面或者功能必须进行权限控制校验。

**我的理解：**

涉及到对于数据的增删改查，必须有权限的控制和校验，要有一个黑白名单的控制，不能依赖于前台页面的简单控制，后台要有对于完整的权限控制的实现。这样就能尽可能地防治数据的错误修改。

#### 2. 用户传入参数校验
阿里强制要求用户请求传入的任何参数必须做有效校验。

**我的理解：**

对于用户输入的任何参数，前端页面上都必须要做一定的有效性校验，并且在数据发送至服务器的时候在页面上给出验证结果提示，那么在用户请求传入的任务参数，后台同样也要对其有效性进行验证，防止前端页面未能过滤或者暂时无法验证的错误参数。忽略参数的验证会导致的问题很多，page size 过大会导致内存溢出、SQL 溢出等，只有验证才能尽可能地减少这些问题的出现，进而减少错误的排查几率。

所以说在前端已经做了参数校验的情况下，后端也有必要做参数校验。

### 单元测试

#### 1. 单元测试应该自动执行
阿里强制单元测试应该是全自动执行的，并且非交互式的。测试框架通常是定期执行的，执行过程必须完全自动化才有意义。输出结果需要人工检查的测试不是一个号的单元测试。单元测试中不准使用 System.out 来进行人肉验证，必须使用 assert 来验证。

**我的理解：**

这条原则比较容易理解。单元测试是整个系统的最小测试单元，针对的是一个类中一个方法的测试，如果这些测试的结果需要人工校验是否正确，那么对于验证人来说是一项痛苦而且耗时的工作。另外，单元测试作为系统最基本的保障，需要在修改代码、编译、打包过程中都会运行测试用例，保障基本功能，自动化的测试是必要条件。其实自动化测试不仅是单元测试特有的，包括集成测试、系统测试等，都在慢慢地转向自动化测试，以降低测试的人力成本。

#### 2. 单元测试应该是独立的
阿里强制保持单元测试的独立性。为了保证单元测试稳定可靠且便于维护，单元测试用例之间决不能互相调用，也不能依赖执行的先后次序。

反例：method2 需要依赖 method1 的执行，将执行结果作为 method2 的输入。

**我的理解：**

单元测试作为系统的最小测试单元，主要目的是尽可能早地测试编写的代码，降低后续集成测试期间的测试成本，以及在运行测试用例的时候能够快速地定位到对应的代码段并解决相关问题。

我们假设这么一个场景，method1 方法被 10 个其他 method 方法调用，如果 10 个 method 方法的测试用例都需要依赖 method1，那么当 methdo1 被修改导致运行出错的情况下，会导致 method1 以及依赖它的 10 个 method 的所有测试用例报错，这样就需要排查这 11 个方法到底哪里出了问题，这与单元测试的初衷不符，也会大大的增加排查工作量，所以单元测试必须是独立的，不会因为受到外部修改（这里的修改包括了依赖方法的修改以及外部环境的修改），编写单元测试时遇到的这类依赖可以使用 mock 来模拟输入和期望的返回，这样所以来的方法内部逻辑的变更就不会影响到外部的实现。

#### 3. BCDE 原则
阿里推荐编写单元测试代码遵守 BCDE 原则，以保证被测试模块的交付质量。

**我的理解：**

BCDE 原则逐一解释如下：

B（Border）：确保参数边界值均被覆盖。

例如：对于数字，测试负数、0、正数、最小值、最大值、NaN（非数字）、无穷大值等。对于字符串，测试空字符串、单字符、非 ASCII 字符串、多字节字符串等。对于集合类型，测试空、第一个元素、最后一个元素等。对于日期，测试 1 月 1 日、2 月 29 日、12 月 31 日等。被测试的类本身也会暗示一些特定情况下的边界值。对于边界情况的测试一定要详尽。

C（Connect）：确保输入和输出的正确关联性。

例如，测试某个时间判断的方法 boolean inTimeZone(Long timeStamp)，该方法根据输入的时间戳判断该事件是否存在于某个时间段内，返回 boolean 类型。如果测试输入的测试数据为 Long 类型的时间戳，对于输出的判断应该是对于 boolean 类型的处理。如果测试输入的测试数据为非 Long 类型数据，对于输出的判断应该是报错信息是否正确。

D（Design）：任务程序的开发包括单元测试都应该遵循设计文档。

E（Error）：单元测试包括对各种方法的异常测试，测试程序对异常的响应能力。

除了这些解释之外，《单元测试之道（Java 版）》这本书里面提到了关于边界测试的 **CORRECT** 原则：

一致性（Conformance）：值是否符合预期格式（正常的数据），列出所有可能不一致的数据，进行验证。

有序性（Ordering）：传入的参数的顺序不同的结果是否正确，对排序算法会产生影响，或者是对类的属性赋值顺序不同会不会产生错误。

区间性（Range）：参数的取值范围是否在某个合理的区间范围内。

引用/耦合性（Reference）：程序依赖外部的一些条件是否已满足。前置条件：系统必须处于什么状态下，该方法才能运行。后置条件，你的方法将会保证哪些状态发生改变。

存在性（Existence）：参数是否真的存在，引用为 Null，String 为空，数值为 0 或者物理介质不存在时，程序是否能正常运行。

基数性（Cardinality）：考虑以"0-1-N 原则"，当数值分别为 0、1、N 时，可能出现的结果，其中 N 为最大值。

时间性（Time）：相对时间指的是函数执行的依赖顺序，绝对时间指的是超时问题、并发问题。

### 数据库表设计

#### 1. 建表的是与否规则
阿里强制要求如果遇到需要表达是与否的概念时，必须使用 is_xxx 的方法命令，数据类型是 unsigned tinyint，1 表示是，0 表示否。

说明：任务字段如果为非负数，必须是 unsigned。

正例：表达逻辑删除的字段名 is_deleted，1 表示删除，0 表示未删除。

**我的理解：**

命名使用 is_xxx 第一个好处是比较清晰的，第二个好处是使用者根据命名就可以知道这个字段的取值范围，也方便做参数验证。

类型使用 unsigned 的好处是如果只存整数，unsigned 类型有更大的取值范围，可以节约磁盘和内存使用。

对于表的名字，MySQL 社区有自己推荐的命名规范：

表包含多个英文单词时，需要用下划线进行单词分割，这一点类似于 Java 类名的命名规范，例如 master_schedule、security_user_permission；
由于 InnoDB 存储引擎本身是针对操作系统的可插拔设计的，所以原则上所有的表名组成全部由小写字母组成；
不允许出现空格，需要分割一律采用下划线；
名字不允许出现数字，仅包含英文字母；
名字需要总长度少于 64 个字符。

#### 2. 数据类型精度考量
阿里强制要求存放小数时使用 decimal，禁止使用 float 和 double。

说明：float 和 double 在存储的时候，存在精度损失的问题，很可能在值的比较时，得到不正确的结果。如果存储的数据范围超过 decimal 的范围，建议将数据拆成整数和小数分开存储。

**我的理解：**

我们先来看看各个精度的范围。

Float：浮点型，4 字节数 32 位，表示数据范围-3.4E38~3.4E38

Double：双精度型，8 字节数 64 位，表示数据范围-1.7E308~1.7E308

Decimal：数字型，16 字节数 128 位，不存在精度损失，常用于银行账目计算

在精确计算中使用浮点数是非常危险的，在对精度要求高的情况下，比如银行账目就需要使用 Decimal 存储数据。

实际上，所有涉及到数据存储的类型定义，都会涉及数据精度损失问题。Java 的数据类型也存在 float 和 double 精度损失情况，阿里没有指出这条规约，就全文来说，这是一个比较严重的规约缺失。

Joshua Bloch（著名的 Effective Java 书作者）认为，float 和 double 这两个原生的数据类型本身是为了科学和工程计算设计的，它们本质上都采用单精度算法，也就是说在较宽的范围内快速获得精准数据值。但是，需要注意的是，这两个原生类型都不保证也不会提供很精确的值。单精度和双精度类型特别不适用于货币计算，因为不可能准确地表示 0.1（或者任何其他十的负幂）。

我们再来看一个实际的例子。假设你有 1 块钱，现在每次购买蛋糕的价格都会递增 0.10 元，为我们一共可以买几块蛋糕。口算一下，应该是 4 块（因为 0.1+0.2+0.3+0.4=1.0），我们写个程序验证看看，如下所示。
```java
//错误的方式
double funds1 = 1.00;
int itemsBought = 0;
for(double price = .10;funds>=price;price+=.10){
 funds1 -=price;
 itemsBought++;
}
 System.out.println(itemsBought+" items boughts.");
 System.out.println("Changes:"+funds1);
 // 3 items boughts.
// Changes:0.3999999999999999
 
 
 //正确的方式
 final BigDecimal TEN_CENTS = new BigDecimal(".10");
 itemsBought = 0;
 BigDecimal funds2 = new BigDecimal("1.00");
for(BigDecimal price = TEN_CENTS;funds2.compareTo(price)>0;price =
 price.add(TEN_CENTS)){
 fund2 = fund2.substract(price);
 itemsBought++;
 }
 System.out.println(itemsBought+" items boughts.");
 System.out.println("Changes:"+funds2);
// 4 items boughts.
// Changes:0.00
```
这里我们可以看到使用了 BigDecimal 解决了问题，实际上 int、long 也可以解决这类问题。采用 BigDecimal 有一个缺点，就是使用过程中没有原始数据这么方便，效率也不高。如果采用 int 方式，最好不要在有小数点的场景下使用，可以在 100、10 这样业务场景下选择使用。

#### 3. 使用 Char
阿里强制要求如果存储的字符串长度几乎相等，使用 Char 定长字符串类型。

**我的理解：**

从性能上分析，character(n)通常是最慢的，在大多数情况下，应该使用 text 或者 character varying。

### 工程结构

#### 1. 服务间依赖关系
阿里推荐默认上层依赖于下层，箭头关系表示可直接依赖，如：Controller层可以依赖于 Web 层，也可以直接依赖于 Service 层。

**我的理解：**

《软件架构模式》一书中介绍了分层架构思想：

分层架构是一种很常见的架构模式，它也被叫做 N 层架构。这种架构是大多数 Java EE 应用的实际标准。许多传统 IT 公司的组织架构和分层模式十分的相似，所以它很自然地成为大多数应用的架构模式。

分层架构模式里的组件被分成几个平行的层次，每一层都代表了应用的一个功能（展示逻辑或者业务逻辑）。尽管分层架构没有规定自身要分成几层几种，大多数的结构都分成四个层次，即展示层、业务层、持久层和数据库层。业务层和持久层有时候可以合并成单独的一个业务层，尤其是持久层的逻辑绑定在业务层的组件当中。因此，有一些小的应用可能只有三层，一些有着更复杂的业务的大应用可能有五层甚至更多的层。

分层架构中的每一层都有着特定的角色和职能。举个例子，展示层负责所有的界面展示以及交互逻辑，业务层负责处理请求对应的业务。架构里的层次是具体工作的高度抽象，它们都是为了实现某种特定的业务请求。比如说展示层并不关心如何得到用户数据，它只需在屏幕上以特定的格式展示信息。业务层并不关心要展示在屏幕上的用户数据格式，也不关心这些用户数据从哪里来，它只需要从持久层得到数据，执行与数据有关的相应业务逻辑，然后把这些信息传递给展示层。

分层架构的一个突出特性地组件间关注点分离。一个层中的组件只会处理本层的逻辑。比如说，展示层的组件只会处理展示逻辑，业务层中的组件只会去处理业务逻辑。因为有了组件分离设计方式，让我们更容易构造有效的角色和强力的模型，这样应用变得更好开发、测试、管理和维护。

#### 2. 高并发服务器 time_wait
阿里推荐高并发服务器建议调小 TCP 协议的 time_wait 超时时间。

说明：操作系统默认 240 秒后才会关闭处于 time_wait 状态的连接，在高并发访问下，服务器端会因为处于 time_wait 的连接数太多，可能无法建立新的连接，所以需要在服务器上调小此等待值。

正例：在 Linux 服务器上通过变更/etc/sysctl.conf 文件去修改该缺省值（秒）：net.ipv4.tcp_fin_timeout=30

**我的理解：**

服务器在处理完客户端的连接后，主动关闭，就会有 time_wait 状态。TCP 连接是双向的，所以在关闭连接的时候，两个方向各自都需要关闭。先发 FIN 包的一方执行的是主动关闭，后发 FIN 包的一方执行的是被动关闭。主动关闭的一方会进入 time_wait 状态，并且在此状态停留两倍的 MSL 时长。

主动关闭的一方收到被动关闭的一方发出的 FIN 包后，回应 ACK 包，同时进入 time_wait 状态，但是因为网络原因，主动关闭的一方发送的这个 ACK 包很可能延迟，从而触发被动连接一方重传 FIN 包。极端情况下，这一去一回就是两倍的 MSL 时长。如果主动关闭的一方跳过 time_wait 直接进入 closed，或者在 time_wait 停留的时长不足两倍的 MSL，那么当被动关闭的一方早于先发出的延迟包达到后，就可能出现类似下面的问题：

1. 旧的 TCP 连接已经不存在了，系统此时只能返回 RST 包

2. 新的 TCP 连接被建立起来了，延迟包可能干扰新的连接

不管是哪种情况都会让 TCP 不再可靠，所以 time_wait 状态有存在的必要性。

修改 net.ipv4.tcp_fin_timeout 也就是修改了 MSL 参数。

