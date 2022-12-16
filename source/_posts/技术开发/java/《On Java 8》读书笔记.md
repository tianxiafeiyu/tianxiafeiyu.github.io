---
title: 《On Java 8》读书笔记
date: 2022-12-15 23:12:09
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 《On Java 8》读书笔记
---
# 《On Java 8》读书笔记

### 1. java 8 接口可以有默认方法和静态方法

增加默认方法的极具说服力的理由是它允许在不破坏已使用接口的代码的情况下，在接口中增加新的方法。默认方法有时也被称为守卫方法或虚拟扩展方法。



默认方法的最佳实践是 java 8 的 stream api。



接口使用了默认方法，继承了这个接口的类可以不用实现接口中的默认方法。如：

```java
// interfaces/AnInterface.java
interface AnInterface {
    void firstMethod();
    void secondMethod();
}
```

类实现接口

```java
// interfaces/AnImplementation.java
public class AnImplementation implements AnInterface {
    public void firstMethod() {
        System.out.println("firstMethod");
    }
    
    public void secondMethod() {
        System.out.println("secondMethod");
    }
    
    public static void main(String[] args) {
        AnInterface i = new AnImplementation();
        i.firstMethod();
        i.secondMethod();
    }
}
```

如果我们在 AnInterface 中增加一个新方法 newMethod()，而在 AnImplementation 中没有实现它，编译器就会报错。如果我们使用关键字 default 为 newMethod() 方法提供默认的实现，那么所有与接口有关的代码能正常工作，不受影响，而且这些代码还可以调用新的方法 newMethod()：

```java
// interfaces/InterfaceWithDefault.java
interface InterfaceWithDefault {
    void firstMethod();
    void secondMethod();
    
    default void newMethod() {
        System.out.println("newMethod");
    }
}
```

只要修改接口，不用修改实现类。

```java
// interfaces/Implementation2.java
public class Implementation2 implements InterfaceWithDefault {
    @Override
    public void firstMethod() {
        System.out.println("firstMethod");
    }
    
    @Override
    public void secondMethod() {
        System.out.println("secondMethod")
    }
    
    public static void main(String[] args) {
        InterfaceWithDefault i = new Implementation2();
        i.firstMethod();
        i.secondMethod();
        i.newMethod();
    }
}
```



### 2. java 8 多继承

类可以实现多个接口，由于默认方法的加入，java class 有了多继承的特性，如果一个类实现的接口中有重复的方法签名相同（方法签名包括方法名和参数类型）的默认方法，类就需要覆写冲突的方法，或者重新实现方法。



### 3. 数组是保存一组对象最有效的方式



### 4. 关于集合类（Collection ）的写法

```java
List<Apple> apples = new LinkedList<>();
LinkedList<Apple> apples = new LinkedList<>();
```

请注意， ArrayList 已经被向上转型为了 List接口，这是大多数情况下的写法。但是如果需要用到具体的集合类的功能特性时，就不能将它们向上转型为更通用的接口。



### 5. 优化是一个很棘手的问题，最好的策略就是置之不顾，直到发现必须要去担心它了（尽管去理解这些问题总是一个很好的主意）



### 6 . 集合类中迭代器（Iterators）的理解

迭代器是一个对象，它在一个序列中移动并选择该序列中的每个对象，而客户端程序员不知道或不关心该序列的底层结构。另外，迭代器通常被称为轻量级对象（lightweight object）：创建它的代价小。ava 的 Iterator 只能单向移动。这个 Iterator 只能用来：

1. 使用 iterator() 方法要求集合返回一个 Iterator。 Iterator 将准备好返回序列中的第一个元素。
2. 使用 next() 方法获得序列中的下一个元素。
3. 使用 hasNext() 方法检查序列中是否还有元素。
4. 使用 remove() 方法将迭代器最近返回的那个元素删除。

有了 Iterator ，就不必再为集合中元素的数量操心了。这是由 hasNext() 和 next() 关心的事情。也可以不用考虑到集合的确切类型。迭代器能够将遍历序列的操作与该序列的底层结构分离，统一了对集合的访问方式。

用法示例：

```java
// collections/CrossCollectionIteration.java
import typeinfo.pets.*;
import java.util.*;

public class CrossCollectionIteration {
  public static void display(Iterator<Pet> it) {
    while(it.hasNext()) {
      Pet p = it.next();
      System.out.print(p.id() + ":" + p + " ");
    }
    System.out.println();
  }
  public static void main(String[] args) {
    List<Pet> pets = Pets.list(8);
    LinkedList<Pet> petsLL = new LinkedList<>(pets);
    HashSet<Pet> petsHS = new HashSet<>(pets);
    TreeSet<Pet> petsTS = new TreeSet<>(pets);
    display(pets.iterator());
    display(petsLL.iterator());
    display(petsHS.iterator());
    display(petsTS.iterator());
  }
}
/* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug
7:Manx
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug
7:Manx
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug
7:Manx
5:Cymric 2:Cymric 7:Manx 1:Manx 3:Mutt 6:Pug 4:Pug
0:Rat
*/
```

ListIterator 是一个更强大的 Iterator 子类型，它只能由各种 List 类生成。 Iterator 只能向前移动，而 ListIterator 可以双向移动。它还可以生成相对于迭代器在列表中指向的当前位置的后一个和前一个元素的索引，并且可以使用 set() 方法替换它访问过的最近一个元素。



### 7. Java8 中的堆栈声明为

```java
Deque<String> stack = new ArrayDeque<>();
```

之所以是 Deque 而不是Stack，这是因为 Java 1.0 中附带了一个 Stack 类，结果设计得很糟糕（为了向后兼容，后续保留了这个类）。Java 6 添加了 ArrayDeque。



### 8. 队列

LinkedList 实现了 Queue 接口，并且提供了一些方法以支持队列行为，因此 LinkedList 可以用作 Queue 的一种实现。 通过将 LinkedList 向上转换为 Queue 。

```
Queue<Integer> queue = new LinkedList<>();
```



### 9. for-in 语法糖

Java 5 引入了一个名为 Iterable 的接口，该接口包含一个能够生成 Iterator 的 iterator() 方法。for-in 使用此 Iterable 接口来遍历序列。因此，如果创建了任何实现了 Iterable 的类，都可以将它用于 for-in 语句中。

```java
// collections/IterableClass.java
// Anything Iterable works with for-in
import java.util.*;

public class IterableClass implements Iterable<String> {
  protected String[] words = ("And that is how " +
    "we know the Earth to be banana-shaped."
    ).split(" ");
  @Override
  public Iterator<String> iterator() {
    return new Iterator<String>() {
      private int index = 0;
      @Override
      public boolean hasNext() {
        return index < words.length;
      }
      @Override
      public String next() { return words[index++]; }
      @Override
      public void remove() { // Not implemented
        throw new UnsupportedOperationException();
      }
    };
  }
  public static void main(String[] args) {
    for(String s : new IterableClass())
      System.out.print(s + " ");
  }
}
/* Output:
And that is how we know the Earth to be banana-shaped.
*/
```

### 10. 不要在新代码中使用遗留类 Vector ，Hashtable 和 Stack 。

### 11. Lambda 表达式

```java
static Body bod = h -> h + " No Parens!"; // [1]

  static Body bod2 = (h) -> h + " More details"; // [2]

  static Description desc = () -> "Short info"; // [3]

  static Multi mult = (h, n) -> h + n; // [4]

  static Description moreLines = () -> { // [5]
    System.out.println("moreLines()");
    return "from moreLines()";
  };
```

Lambda 表达式基本语法：

- 1. 参数。
  2. 接着 ->，可视为“产出”。
  3. -> 之后的内容都是方法体。

- 当只用一个参数，可以不需要括号 ()。 然而，这是一个特例。
- 正常情况使用括号 () 包裹参数。 为了保持一致性，也可以使用括号 () 包裹单个参数，虽然这种情况并不常见。
- 如果没有参数，则必须使用括号 () 表示空参数列表。
- 对于多个参数，将参数列表放在括号 () 中。
- 到目前为止，所有 Lambda 表达式方法体都是单行。 该表达式的结果自动成为 Lambda 表达式的返回值，在此处使用 return 关键字是非法的。 这是 Lambda 表达式缩写用于描述功能的语法的另一种方式。
-  如果在 Lambda 表达式中确实需要多行，则必须将这些行放在花括号中。 在这种情况下，就 需要使用 return。Lambda 表达式通常比匿名内部类产生更易读的代码，尽可能使用它们。



Fibonacci 序列改为使用递归 Lambda 表达式来实现：

```java
interface IntCall {
  int call(int arg);
}

public class RecursiveFibonacci {
  IntCall fib;

  RecursiveFibonacci() {
    fib = n -> n == 0 ? 0 :
               n == 1 ? 1 :
               fib.call(n - 1) + fib.call(n - 2);
  }
  
  int fibonacci(int n) { return fib.call(n); }

  public static void main(String[] args) {
    RecursiveFibonacci rf = new RecursiveFibonacci();
    for(int i = 0; i <= 10; i++)
      System.out.println(rf.fibonacci(i));
  }
}
```

### 12. 流操作

流操作的类型有三种：创建流，修改流元素（中间操作， Intermediate Operations），消费流元素（终端操作， Terminal Operations），收集流元素（通常是到集合中）。

### 13. 异常处理

finally 子句永远会执行，即使前面有 return 语句。由于 Java 有垃圾回收机制，所以 finally 语句主要是用来恢复内存之外的资源回到初始状态，需要清理的资源包括：已经打开的文件或网络连接，在屏幕上画的图形，甚至可以是外部世界的某个开关。

### 14. 永恒真理

[你永远不能保证你的代码是正确的，你只能证明它是错的。](https://lingcoder.github.io/OnJava8/#/book/16-Validating-Your-Code?id=你永远不能保证你的代码是正确的，你只能证明它是错的。)