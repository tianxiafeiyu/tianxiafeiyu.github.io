---
title: Java中无处不在的坑
date: 2022-12-15 23:38:01
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java中无处不在的坑
---

#### 关于Integer
```
public static void main(String[] args) {
    Integer a = 1;
    Integer b = 1;
    Integer c = 2000;
    Integer d = 2000;
    System.out.println(a==b);   //true
    System.out.println(c==d);   //false
}
```
原因是自动装箱时调用了Integer.valueOf()这个方法，当值在-128到127之间时从缓存里面拿出来的，超出后会new一个对象

所以Integer的比较要用a.intValue()==b.intValue() 或者调用equals方法。Long也有类似的特性。

Java的包装类都不能直接用 == 比较。封箱和拆箱在下面的场景中才会存在：


#### 关于Arrays.asList 
```
public static void main(String[] args) {
		String[] strings = {"zhao","qian","sun"};
		List<String> list = Arrays.asList(strings);
		list.add("li"); // java.lang.UnsupportedOperationException
	}
```
Arrays.asList() 返回的是java.util.Arrays.ArrayList;不是java.util.ArrayList。

源码中：
```
public class Arrays {
    public static <T> List<T> asList(T... a) {
            return new ArrayList<>(a);
        }
    
    /**
     * @serial include
     */
    private static class ArrayList<E> extends AbstractList<E>
        implements RandomAccess, java.io.Serializable
    {
        private static final long serialVersionUID = -2764017481108945198L;
        private final E[] a;

        ArrayList(E[] array) {
            a = Objects.requireNonNull(array);
        }

        @Override
        public int size() {
            return a.length;
        }
        ...
    }
}
```
java.util.Arrays.ArrayList 只是Arrays的一个静态内部类，只实现了 get、set、forEach等方法，没有add、remove等方法，无法改变集合大小。

#### 重载函数传入 null
```
public class Test {
    public  void func1(String param) {
        System.out.println("Param type is String");
    }

    public  void func1(Object param) {
        System.out.println("Param type is Object");
    }


    public  void func2( Double param) {
        System.out.println("Param type is Double");
    }

    public  void func2(Integer param) {
        System.out.println("Param type is Integer");
    }

    public static void main(String[] args) {
        Test test = new Test();
        test.func1(null);   //Param type is String
        test.func2(null);   //编译不通过
    }
}
```
重载函数传入 null:
- 此时如果参数存在继承关系的话，走的是 类型参数是子类的方法（更具体）
- 如果参数类型不存在继承关系的话，程序不知道要调哪一个方法，编译报错

#### 关于继承强转的问题
java中子类强转父类,实际上依然是子类，该引用只能调用父类中定义的方法和变量；

如果子类中重写了父类中的一个方法，那么在调用这个方法的时候，将会调用子类中的这个方法；

可以认为子类强转父类就是在子类的基础上，照着父类的模版削减自身，只留下父类中存在的方法和属性。

父类是不能强转子类的，除非当前父类是子类装 (new) 出来的，可以转回真正的子类身份。
```java
List list1 = new ArrayList();
ArrayList list2 = (ArrayList) list1;
```

#### HashSet的问题
```
public class Person {
    public int age;
    public String name;

    //注意此处重写了hashCode方法
    @Override
    public int hashCode() {
        return Objects.hash(age, name);
    }

    @Override public String toString() {
        return "Person{" + "age=" + age + ", name='" + name + '\'' + '}';
    }

    public Person(int age, String name) {
        this.age = age;
        this.name = name;
    }
}
public class Test {
    public static void main(String[] args) {
        Person person1 = new Person(25, "xiaoming");
        Person person2 = new Person(32, "xiaohong");
        HashSet<Person> hashSet = new HashSet<>();
        hashSet.add(person1);
        hashSet.add(person2);
        person1.age = 18;
        hashSet.remove(person1);
        Iterator<Person>  iterator=  hashSet.iterator();
        while (iterator.hasNext()){
            System.out.println(iterator.next());
        }
    }
}
```
控制台打印结果：  
Person{age=18, name=‘xiaoming’}  
Person{age=32, name=‘xiaohong’}  
可发现 xiaoming 并没有被删除掉 是因为age改成18以后 hashcode值改变了。

#### ArrayList遍历删除的问题
```
public static void main(String[] args) {
        List<String> list = new ArrayList<String>();
        list.add("a");
        list.add("b");
        list.add("b");
        list.add("c");
        for (int i = 0; i < list.size(); i++) {
            if ("b".equals(list.get(i))) {
                list.remove(list.get(i));
            }
        }
    }
```
结果错误，因为 remove 会导致下标的改变。针对这种情况可以用**倒序删除**的方式来避免，数组倒序遍历时即使发生元素删除也不影响后序元素遍历。
```
public static void main(String[] args) {
        List<String> list = new ArrayList<String>();
        list.add("a");
        list.add("b");
        list.add("b");
        list.add("c");
        for(int i=list.size()-1;i>=0;i--){
            if("b".equals(list.get(i))){
                list.remove(list.get(i));
            }
        }
    }
```

```
public static void main(String[] args) {
        List<String> list = new ArrayList<String>();
        list.add("a");
        list.add("b");
        list.add("b");
        list.add("c");
        for (String item:list) {
            if ("b".equals(item)) {
                list.remove(item);
            }
        }
    }
```
上面的程序抛出了java.util.ConcurrentModificationException异常。

正确写法：
```
public static void main(String[] args) {
    List<String> list = new ArrayList<String>();
    list.add("a");
    list.add("b");
    list.add("b");
    list.add("c");
    Iterator<String> iterator = list.iterator();
    while (iterator.hasNext()) {
        if ("b".equals(iterator.next())) {
            iterator.remove();
        }
    }
}
```

#### 使用 String.compareTo() 注意问题
java8 源码：
```
public int compareTo(String anotherString) {
    int len1 = value.length;
    int len2 = anotherString.value.length;
    int lim = Math.min(len1, len2);
    char v1[] = value;
    char v2[] = anotherString.value;

    int k = 0;
    while (k < lim) {
        char c1 = v1[k];
        char c2 = v2[k];
        if (c1 != c2) {
            return c1 - c2;
        }
        k++;
    }
    return len1 - len2;
}
```
对于两个比较的字符串：
1. 从左到右最多取 min(len1, len2) 个字符做比较。在比较中，若字符不相等，则返回该位置的字符的**ASCII码的差值**。
2. 如果比较中的字符都相等，则返回 **长度的差值**

所以在做数字用的字符串中，整型数据可以使用 compareTo 比较，小数则不应该使用 compareTo 判断大小。

