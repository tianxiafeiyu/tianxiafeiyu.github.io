---
title: Java创建线程的4种方式
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java创建线程的4种方式
---
### 一、概述

#### 1. 线程与进程

进程（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。

线程，有时被称为轻量级进程(Lightweight Process，LWP），是程序执行流的最小单元。线程是程序中一个单一的顺序控制流程，在单个程序中同时运行多个线程完成不同的工作，称为多线程

### 2. 同步与异步

同步（Synchronous）：同步是指一个进程在执行某个请求的时候，如果该请求需要一段时间才能返回信息，那么这个进程会一直等待下去，直到收到返回信息才继续执行下去。

异步（Asynchronous）：异步是指进程不需要一直等待下去，而是继续执行下面的操作，不管其他进程的状态，当有信息返回的时候会通知进程进行处理。

通俗地讲，也就是说，同步需要按部就班地走完一整个流程，完成一整个动作。而异步则不需要按部就班，可以在等待那个动作的时候同时做别的动作

### 3. 并行与并发

并行：时间上是由重叠的，也就是说并行才是真正意义上的同一时刻可以有多个任务同时执行。

并发：任务在执行的时候，并发是没有时间上的重叠的，两个任务是交替执行的，由于切换的非常快，对于外界调用者来说相当于同一时刻多个任务一起执行了。

### 二、Java创建线程的3种方式

#### 1. 继承 Thread 类

1. 定义 Thread 类的子类,并重写该类的 run() 方法,该 run() 方法的方法体就代表了线程需要完成的任务.因此把 run() 方法称为线程执行体。
2. 创建 Thread 子类的实例,即创建了线程对象。
3. 调用线程对象的 start() 方法来启动该线程。

```
public class MyThread extends Thread {
	public MyThread() {
		
	}
	public void run() {
		for(int i=0;i<10;i++) {
			System.out.println(Thread.currentThread()+":"+i);
		}
	}
	public static void main(String[] args) {
		MyThread mThread1=new MyThread();
		MyThread mThread2=new MyThread();
		MyThread myThread3=new MyThread();
		mThread1.start();
		mThread2.start();
		myThread3.start();
	}
}
```

#### 2. 实现 Runnable 接口

1. 定义 Runnable 接口的实现类,并重写该接口的 run() 方法,该 run() 方法的方法体同样是该线程的线程执行体。
2. 创建 Runnable 实现类的实例,并以此实例作为 Thread 的target来创建 Thread 对象,该 Thread 对象才是真正的线程对象。
3. 调用线程对象的 start() 方法来启动该线程。

```
public class MyThread implements Runnable{
	public static int count=20;
	public void run() {
		while(count>0) {
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			System.out.println(Thread.currentThread().getName()+"-当前剩余票数:"+count--);
		}
	}
	public static void main(String[] args) {
		MyThread Thread1=new MyThread();
		Thread mThread1=new Thread(Thread1,"线程1");
		Thread mThread2=new Thread(Thread1,"线程2");
		Thread mThread3=new Thread(Thread1,"线程3");
		mThread1.start();
		mThread2.start();
		myThread3.start();
	}
}
```

推荐使用此方式

#### 3. 使用 Callable 和 Future

1. 创建 Callable 接口的实现类,并实现 call() 方法,该 call() 方法将作为线程执行体,且该 call() 方法有返回值,再创建 Callable 实现类的实例。
2. 使用 FutureTask 类来包装 Callable 对象,该 FutureTask 对象封装了该 Callable 对象的 call() 方法的返回值。
3. 使用 FutureTask 对象作为 Thread 对象的 target 创建并启动新线程。
4. 调用 FutureTask 对象的 get() 方法来获得子线程执行结束后的返回值。

```
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
 
public class MyThread implements Callable<String> {
	private int count = 20;
 
	@Override
	public String call() throws Exception {
		for (int i = count; i > 0; i--) {
        //Thread.yield();
			System.out.println(Thread.currentThread().getName()+"当前票数：" + i);
		}
		return "sale out";
	} 
 
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		Callable<String> callable  =new MyThread();
		FutureTask <String>futureTask=new FutureTask<>(callable);
		Thread mThread=new Thread(futureTask);
		Thread mThread2=new Thread(futureTask);
		Thread mThread3=new Thread(futureTask);
        //mThread.setName("hhh");
		mThread.start();
		mThread2.start();
		mThread3.start();
		System.out.println(futureTask.get());
		
	}
}
```

#### 4. 使用线程池

通过 `java.util.concurrent.Executors` 的工具类可以创建三种类型的普通线程池：

##### (1)SingleThreadPoolExecutor :单线程池

适用于需要保证顺序执行各个任务的场景。

```
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
 
public class Test {
	public static void main(String[] args) {
		ExecutorService ex=Executors.newSingleThreadExecutor();
		
		for(int i=0;i<5;i++) {
			ex.submit(new Runnable() {
				
				@Override
				public void run() {
					for(int j=0;j<10;j++) {
						System.out.println(Thread.currentThread().getName()+j);
					}
					
				}
			});
		}
		ex.shutdown();
	}	
}
```

##### (2) FixThreadPool(int n); 固定大小的线程池

使用于为了满足资源管理需求而需要限制当前线程数量的场合。使用于负载比较重的服务器。

```
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
 
public class Test {
	public static void main(String[] args) {
		ExecutorService ex=Executors.newFixedThreadPool(5);
		
		for(int i=0;i<5;i++) {
			ex.submit(new Runnable() {
				
				@Override
				public void run() {
					for(int j=0;j<10;j++) {
						System.out.println(Thread.currentThread().getName()+j);
					}
					
				}
			});
		}
		ex.shutdown();
	}	
}
```

##### (5)CashedThreadPool(); 缓存线程池

当提交任务速度高于线程池中任务处理速度时，缓存线程池会不断的创建线程 适用于提交短期的异步小程序，以及负载较轻的服务器

```
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
 
public class Test {
	public static void main(String[] args) {
		ExecutorService ex=Executors.newCachedThreadPool();
		
		for(int i=0;i<5;i++) {
			ex.submit(new Runnable() {
				
				@Override
				public void run() {
					for(int j=0;j<10;j++) {
						System.out.println(Thread.currentThread().getName()+j);
					}
					
				}
			});
		}
		ex.shutdown();
	}	
}
```