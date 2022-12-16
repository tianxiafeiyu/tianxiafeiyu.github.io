---
title: lombok
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - lombok
---
### lombok简介

Lombok 是能自动接通编辑器和构建工具的一个Java库，对于简单的Java对象，通过注解的形式例如@Setter @Getter，可以替代代码中的getter和setter方法。Lombok中用到了注解，但是它并没有用到反射，而是在代码编译时期动态将注解替换为具体的代码。所以JVM实际运行的代码，和我们手动编写的包含了各种工具方法的类相同。

#### lombok常用注解

- @Data：注解在类上，将类提供的所有属性都添加get、set方法，并添加、equals、canEquals、hashCode、toString方法
- @Setter：注解在类上，为所有属性添加set方法、注解在属性上为该属性提供set方法
- @Getter：注解在类上，为所有的属性添加get方法、注解在属性上为该属性提供get方法
- @NotNull：在参数中使用时，如果调用时传了null值，就会抛出空指针异常
- @NoArgsConstructor：创建一个无参构造函数
- @toString：创建toString方法。
- @UtilityClass:工具类

#### idea项目中使用lombok

第一步： pom.xml中加入lombok依赖包

```
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.16.20</version>
    <scope>provided</scope>
</dependency
```

第二步：加入lombok插件
File —> Settings —> Plugins：搜索lombok，点击安装install。然后会提示重启，重启。

第三步：idea配置
File —> Settings —> Build, Execution, Deployment —> Compiler —> Java Compiler —> User compiler：选择javac
File —> Settings —> Build, Execution, Deployment —> Compiler —> Annotation Processors -> Enable annotation processors -> 勾选

#### 注意事项

- 1、使用 lombok.Data 注解实体类时，boolean类型的get方法，会变成is方法；若需要get方法，使用封装类Boolean。