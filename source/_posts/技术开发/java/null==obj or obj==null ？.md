在比较操作中，有人提倡常量前置的写法，但是读起来就会怪怪的。

据说在 c++ 中，`if(obj = null)`是可以通过编译的，但是在运行时会报错，为了防止这种情况发生，所以提倡常量前置的写法。

但是在 Java 中 `if(obj = null)`是在编译时会报错的，所以不存在这一隐患。时候判断常量前置真的没有必要了呢？其实有两面性，有好有坏，具体要看个人和规范的要求。

#### 好处：

1. 可以避免`if(obj = null)`类似错误
2. 类似`"str".equals(obj)`的写法可以避免空指针错误

#### 坏处：

1. 影响代码可读性
2. 使得代码存在隐患。出现了预料之外的空指针，应该积极去处理，而不是掩盖

#### 特例

Boolean 类情况：

```
public class Test{
    public static void main(String[] args){
        Boolean obj = Boolean.FALSE;
        if(null = obj){     // 编译器报错
            //...
        }
    }
}
public class Test{
    public static void main(String[] args){
        Boolean obj = Boolean.FALSE;
        if(obj = null){     // 编译器不报错，运行时报错
            //...
        }
    }
}
```

这个算是 Java 中的特例，值得注意

反正我是喜欢常量前置的