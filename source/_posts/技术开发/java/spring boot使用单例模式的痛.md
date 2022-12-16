---
title: spring boot使用单例模式的痛
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - spring boot使用单例模式的痛
---
单例模式好处多多，是工具类中经常使用的设计模式，但是笔者在spring boot中使用单例模式中，尝到了许多痛苦的滋味。。。

Spring注解给开发带来了很多便利，要使用到这种便利，就需要使用spring的IOC注入，即类的创建需要交由spring来管理。如@Autowired，一个类如果在使用@Autowired注入了另一个类，但是当这个类被new时，@Autowired注入将会失效，出现NPE报错。

比如

```
public class A{
    //...
}

public class B{
    @Autowired
    A a;
    
    private static volatile B instance;
    private B();
    public static B getInstance(){
        if(null == instance){
             synchronized (B.class) {
                 instance = new B(); //B的@Autowired不生效，b.a==null
             }
        }
        return instance;
    }
    //...
}
```

一些spring辅助类是必须要交由spring注入的，比如Environment，单例模式就很不方便了。

当然，办法也是有的，可以使用`ApplicationContext`来注入Bean：

```
public class SpringUtil implements ApplicationContextAware {
    private static ApplicationContext applicationContext;

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        SpringUtil.applicationContext = applicationContext;
    }

    //beanName是类名，第一个字母小写
    public static <T> T getBean(String beanName) {
        if(applicationContext.containsBean(beanName)){
            return (T) applicationContext.getBean(beanName);
        }else{
            return null;
        }
    }

    public static <T> Map<String, T> getBeansOfType(Class<T> baseType){
        return applicationContext.getBeansOfType(baseType);
    }

}
```

要使用某一个类的时候`SpringUtil.getBean(beanName)`就可以的，坏处也是有的，无法使用全局变量，每个方法使用这个类时都需要注入一次。