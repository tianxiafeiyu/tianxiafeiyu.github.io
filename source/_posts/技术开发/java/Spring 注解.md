#### 什么是注解？
注解是JDK1.5版本开始引入的一个特性，用于对代码进行说明，可以对包、类、接口、字段、方法参数、局部变量等进行注解。

#### 注解与什么用？
1. 生成文档，通过代码里标识的元数据生成javadoc文档。

2. 编译检查，通过代码里标识的元数据让编译器在编译期间进行检查验证。

3. 编译时动态处理，编译时通过代码里标识的元数据动态处理，例如动态生成代码。

4. 运行时动态处理，运行时通过代码里标识的元数据动态处理，例如使用反射注入实例

注解和XML的区别：
- 注解：是一种分散式的元数据，与源代码紧绑定。
- xml：是一种集中式的元数据，与源代码无绑定
#### 怎么实现注解？
1、使用 @interface 定义注解。

2、通过继承以下注解，实现功能：

 元注解@Target,@Retention,@Documented,@Inherited 


元注解：
1. @Target 表示该注解用于什么地方，可能的 ElemenetType 参数包括：
    * ElemenetType.CONSTRUCTOR 构造器声明 
    * ElemenetType.FIELD 域声明（包括 enum 实例） 
    * ElemenetType.LOCAL_VARIABLE 局部变量声明 
    * ElemenetType.METHOD 方法声明 
    * ElemenetType.PACKAGE 包声明 
    * ElemenetType.PARAMETER 参数声明 
    * ElemenetType.TYPE 类，接口（包括注解类型）或enum声明

2. @Retention 表示在什么级别保存该注解信息。可选的 RetentionPolicy 参数包括：
    * RetentionPolicy.SOURCE 注解将被编译器丢弃 
    * RetentionPolicy.CLASS 注解在class文件中可用，但会被VM丢弃 
    * RetentionPolicy.RUNTIME VM将在运行期也保留注释，因此可以通过反射机制读取注解的信息。

3. @Documented 将此注解包含在 javadoc 中 

4. @Inherited 允许子类继承父类中的注解


#### 注解工作过程
以 spring 的 @controller 来当做示例:

@Controller继承@Component注解的方法，将其以单例的形式放入spring容器，然后spring会通过配置文件中的<context:component-scan>的配置，进行如下操作：
1. 使用asm技术扫描.class文件，并将包含@Component及元注解为@Component的注解@Controller、@Service、@Repository或者其他自定义的的bean注册到beanFactory中，

2. 然后spring注册注解处理器。注解处理器是一个在javac编译期处理注解的工具，你可以创建注解处理器并注册，在编译期你创建的处理器以Java代码作为输入，生成文件.java文件作为输出。 

3. 实例化处理器，然后将其放到beanPostFactory中，然后我们就可以在类中进行使用了。

4. 创建bean时，会自动调用相应的处理器进行处理。

spring @Controller源码：
```Java
package org.springframework.stereotype;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.springframework.core.annotation.AliasFor;

@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Controller {
    @AliasFor(
        annotation = Component.class
    )
    String value() default "";
}
```
@AliasFor 表示别名，它可以注解到自定义注解的两个属性上，表示这两个互为别名，也就是说这两个属性其实同一个含义

@Component
```
package org.springframework.stereotype;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Indexed
public @interface Component {
    String value() default "";
}
```
每个注解里面都有一个默认的value()方法，为当前的注解声明一个名字，一般默认为类名