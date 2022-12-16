---
title: spring boot使用多线程
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - spring boot使用多线程
---
业务场景：查询数据分页，每条数据需要添加上概览信息，获取概览信息需要调用一些http接口，有一定的等待时间，单线程查询效率较慢。现在需要在查出了数据库持久化数据的基础上，使用多线程给数据添加概览信息，而且在所有异步线程都完成后，再返回分页信息给前端。

#### 1. 
应用主程序添加注解 @EnableAsync 来开启 Springboot 对于异步任务的支持
```java
@SpringBootApplication
@EnableAsync
public class SpringBootApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringBootApplication.class, args);
    }
}
```

#### 2.
配置类实现接口 AsyncConfigurator，返回一个 ThreadPoolTaskExecutor 线程池对象。
```java
@Configuration
@EnableAsync
public class AsyncTaskConfig implements AsyncConfigurer {

    // ThredPoolTaskExcutor的处理流程
    // 当池子大小小于corePoolSize，就新建线程，并处理请求
    // 当池子大小等于corePoolSize，把请求放入workQueue中，池子里的空闲线程就去workQueue中取任务并处理
    // 当workQueue放不下任务时，就新建线程入池，并处理请求，如果池子大小撑到了maximumPoolSize，就用RejectedExecutionHandler来做拒绝处理
    // 当池子的线程数大于corePoolSize时，多余的线程会等待keepAliveTime长时间，如果无请求可处理就自行销毁

    @Override
    @Bean
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor threadPool = new ThreadPoolTaskExecutor();
        //设置核心线程数
        threadPool.setCorePoolSize(10);
        //设置最大线程数
        threadPool.setMaxPoolSize(20);
        //线程池所使用的缓冲队列
        threadPool.setQueueCapacity(10);
        // 等待时间 （默认为0，此时立即停止），并没等待xx秒后强制停止
        threadPool.setAwaitTerminationSeconds(60);
        //  线程名称前缀
        threadPool.setThreadNamePrefix("my-Async-");
        // 初始化线程
        threadPool.initialize();
        return threadPool;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return null;
    }
}
```
#### 3.
异步调用的方法上添加注解@Async，表明该方法是异步方法，如果注解在类上，那表明这个类里面的所有方法都是异步的。异步方法必须是public修饰的，而且需要在另一个类中调用才会生效，否则无法实现异步。  

Service层：
```java
@Async
public CompletableFuture<Long> addOverViewInfo(K8sClusterDTO k8sClusterDTO) throws ApiException {
    // 添加概览信息
    // return CompletableFuture.completedFuture(k8sClusterId);
}
```
Controller层：
```java
// result = 查询数据库得到的分页数据
List<CompletableFuture<Long>> completableFutureList = new ArrayList<>();
// 多线程添加集群概览数据
for (K8sClusterDTO k8sClusterDTO : result.getObjectList()){
    try{
        CompletableFuture<Long> completableFuture = k8sClusterService.addOverViewInfo(k8sClusterDTO);
        completableFutureList.add(completableFuture);
    }catch (Exception e) {
        e.printStackTrace();
        continue;
    }
}

CompletableFuture<Long>[] completableFutureArray = new CompletableFuture[completableFutureList.size()];
// 合并线程，确保子线程全部执行完
CompletableFuture.allOf(completableFutureList.toArray(completableFutureArray)).join();

return result;
```
#### 4.
至此，功能完成。查询效率确实有所提高。 
这算是第一次成功在实际项目中使用多线程，网上查询了很多博客，spring boot中使用多线程是很方便的，但是关键是如何等待所有子线程执行完，像这种直接使用注解来声明一个异步方法，很多网上的方案都行不通，最后看到简书上的一篇文章才有了思路。  

使用了异步编程后，接口调用顺序大概是这样的：  

查询数据库分页数据 
返回分页数据给前端 
第一次调用异步方法 
第二次调用异步方法 
......

所以还没等到数据添加上概览信息，就已经返回了结果，这肯定是行不通的。

使用了CompletableFuture.allOf(...).jion() 方法后，顺序大概就是：

查询数据库分页数据 
第一次调用异步方法 
第二次调用异步方法 
......  
最后一个异步方法执行完毕 
返回分页数据给前端

这样才能返回正确的结果

#### 5.
CompletableFuture allOf().jion(): 
法实现多实例的同时返回，如果allOf里面的所有线程未执行完毕，主线程会阻塞，直到allOf里面的所有线程都执行，主线程就会被唤醒，继续向下运行。总的来说就是保证了子线程之间的异步，又保证了主线程和子线程的同步。


#### 6.
参考资料：  
1. Spring Boot 创建及使用多线程。<https://blog.csdn.net/asd136912/article/details/87716215>
2. SpringBoot 多线程异步调用-提高程序执行效率。<https://www.jianshu.com/p/d919f4372351>