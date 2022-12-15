---
title: java多线程核心技术梳理
---

#### 一、基础知识
1. 创建线程的两种方式：
    - 继承 Thread 类
    - 实现 Runnable 接口
2. 一些基本 API：isAlive(),sleep(),getId(),yield() 等。
    - isAlive() 测试线程是否处于活动状态
    - sleep() 让“正在执行的线程”休眠
    - getId() 取得线程唯一标识
    - yield() 放弃当前的CPU资源
3. 弃用的 API:stop(),suspend(),resume() 等，已经弃用了，因为可能产生数据不同步等问题。
4. 停止线程的几种方式： 
    - 使用退出标识，使线程正常退出，即 run 方法完成。
    - 使用 interrupt 方法中断线程
5. 线程的优先级特性:继承性，规则性，随机性
    - 线程的优先级具有继承性. 如,线程A启动线程B，则B和A优先级一样
    - 线程的优先级具有规则性. CPU尽量倾向于把资源分配给优先级高的线程
    - 线程的优先级具有随机性. 优先级不等同于执行顺序，二者关系不确定
6. java中的两种线程：用户线程和守护(Daemon)线程。
    - 守护线程：进程中不存在非守护线程时，守护线程自动销毁。典型例子如垃圾回收线程。

#### 二、比较和辨析
1. 某个线程与当前线程：当前线程则是指正在运行的那个线程，可由 currentThread() 方法返回值确定。例如，直接在 main 方法里调用 run 方法，和调用线程的 start 方法，打印出的当前线程结果是不同的。
2. interrupted() 和 isInterrupted() 
    - interrupted() 是类的静态方法，测试当前线程是否已经是中断状态，执行后具有将状态标志清除为false的功能。
    - isInterrupted() 是类的实例方法，测试Thread对象是否已经是中断状态，但不清楚状态标志。
3. sleep()和wait()区别： 
    - sleep() 是 Thread 类的 static (静态)的方法；wait() 方法是 Object 类里的方法。
    - sleep() 睡眠时，保持对象锁，仍然占有该锁；wait() 睡眠时，释放对象锁。
    - 在 sleep() 休眠时间期满后，该线程不一定会立即执行，这是因为其它线程可能正在运行而且没有被调度为放弃执行，除非此线程具有更高的优先级；wait() 使用 notify 或者 notifyAlll 或者指定睡眠时间来唤醒当前等待池中的线程。
    - wait() 必须放在 synchronized block 中，否则会在 runtime 时抛出 java.lang.IllegalMonitorStateException 异常。

方法 | 是否释放锁 | 备注
---|--- | ---
wait | 是 | wait 和 notify/notifyAll 是成对出现的, 必须在 synchronize 块中被调用
sleep | 否 | 可使低优先级的线程获得执行机会
yield | 否 | yield 方法使当前线程让出 CPU 占有权, 但让出的时间是不可设定的

#### 三、对象及变量的并发访问
1. synchronized 关键字 
    - 调用用关键字 synchronized 声明的方法是排队运行的。但假如线程A持有某对象的锁，那线程B异步调用非 synchronized 类型的方法不受限制。
    - synchronized 锁重入:一个线程得到对象锁后，再次请求此对象锁时是可以得到该对象的锁的。同时，子类可通过“可重入锁”调用父类的同步方法。
    - 同步不具有继承性。
    - synchronized 使用的“对象监视器”是一个，即必须是同一个对象
2. synchronized 同步方法和 synchronized 同步代码块。
    - 对其他 synchronized 同步方法或代码块调用呈阻塞状态。
    - 同一时间只有一个线程可执行 synchronized 方法/代码块中的代码。
3. synchronized(非 this 对象 x)，将 x 对象作为“对象监视器”。
    - 当多个线程同时执行 synchronized(x){} 同步代码块时呈同步效果。
    - 当其他线程执行 x 对象中 synchronizd 同步方法时呈同步效果。
    - 当其他线程执行 x 对象方法里的 synchronized(this) 代码块时呈同步效果。
4. 静态同步 synchronized 方法与 synchronized(class) 代码块：对当前对应的 class 类进行持锁。
5. volatile 关键字：主要作用是使变量在多个线程间可见。**加 volatile 关键字可强制性从公共堆栈进行取值,而不是从线程私有数据栈中取得变量的值。**
    - 在方法中 while 循环中设置状态位(不加 volatile 关键字)，在外面把状态位置位并不可行，循环不会停止，比如 JVM 在 -server 模式。因为私有堆栈中的值和公共堆栈中的值不同步。
    - volatile 增加了实例变量在多个线程间的可见性，但不支持原子性。
6. 原子类:一个原子类型就是一个原子操作可用的类型，可在没有锁的情况下做到线程安全。但原子类也不是完全安全，虽然原子操作是安全的，可方法间的调用却不是原子的，需要用同步。
7. synchronized 静态方法与非静态方法：
    - synchronized 关键字加 static 静态方法上是给 Class 类上锁，可以对类的所有实例对象起作用。
    - synchronized 关键字加到非 static 静态方法上是给对象上锁，对该对象起作用。
8. synchronized  和volatile 比较 ：
    - 关键字 volatile 是线程同步的轻量级实现，性能比 synchronized 好，且 volatile 只能修饰变量，synchronized 可修饰方法和代码块。
    - 多线程访问 volatile 不会发生阻塞，synchronized 会出现阻塞。
    - volatile 能保证数据可见性，不保证原子性；synchronized 可以保证原子性，也可以间接保证可见性，因为** synchronized 会将私有内存和公共内存中的数据做同步**。
    - volatile 解决的是变量在多个线程间的可见性，synchronized 解决的是多个线程访问资源的同步性。
9. String 常量池特性，故大多数情况下，synchronized 代码块都不适用 String 作为锁对象。
10. 多线程死锁。使用JDK自带工具，jps 命令 + jstack 命令监测是否有死锁。
11. 一个线程出现异常时，其所持有的锁会自动释放。

#### 四、线程间通信
1. 等待/通知机制：wait()和notify()/notifyAll()。wait使线程停止运行，notify使停止的线程继续运行。 
    - wait()：将当前执行代码的线程进行等待，置入”预执行队列”。
        - 在调用wait()之前，线程必须获得该对象的对象级别锁；
        - 执行wait()方法后，当前线程立即释放锁；
        - 从wait()返回前，线程与其他线程竞争重新获得锁；
        - 当线程呈wait()状态时，调用线程的interrup()方法会出现InterrupedException异常；
        - wait(long)是等待某一时间内是否有线程对锁进行唤醒，超时则自动唤醒。
    - notify()：通知可能等待该对象的对象锁的其他线程。随机挑选一个呈wait状态的线程，使它等待获取该对象的对象锁。
        - 在调用notify()之前，线程必须获得该对象的对象级别锁；
        - 执行完notify()方法后，不会马上释放锁，要直到退出synchronized代码块，当前线程才会释放锁；
        - notify()一次只随机通知一个线程进行唤醒。
    - notifyAll()和notify()差不多，只不过是使所有正在等待队中等待同一共享资源的“全部”线程从等待状态退出，进入可运行状态。

2. 每个锁对象有两个队列：就绪队列和阻塞队列。
    - 就绪队列：存储将要获得锁的线程
    - 阻塞队列：存储被阻塞的的线程
3. 生产者/消费者模式 
    - “假死”：线程进入WAITING等待状态，呈假死状态的进程中所有线程都呈WAITING状态。
        - 假死的主要原因：有可能连续唤醒同类。notify唤醒的不一定是异类，也许是同类，如“生产者”唤醒“生产者”。
        - 解决假死：将notify()改为notifyAll()。
    - wait条件改变，可能出现异常，需要将if改成while。
4. 通过管道进行线程间通信：一个线程发送数据到输出管道，另一个线程从输入管道读数据。
    - 字节流：PipedInputStream和PipedOutputStream。
    - 字符流：PipedReader和PipedWriter。
5. join()：等待线程对象销毁，具有使线程排队运行的作用。 
    - join()与interrupt()方法彼此遇到会出现异常。
    - join(long)可设定等待的时间。
6. join与synchronized的区别：join在内部使用wait()方法进行等待;synchronized使用的是“对象监视器”原理作为同步。
7. join(long)与sleep(long)的区别：join(long)内部使用wait(long)实现，所以join(long)具有释放锁的特点;Thread.sleep(long)不释放锁。
8. ThreadLocal类：每个线程绑定自己的值 。
    - 覆写该类的initialValue()方法可以使变量初始化，从而解决get()返回null的问题。
    - InheritableThreadLocal类可在子线程中取得父线程继承下来的值。

#### 五、Lock的使用
1. ReentrantLock类：实现线程之间的同步互斥，比synchronized更灵活 
    - lock()，调用了的线程就持有了“对象监视器”，效果和synchronized一样
2. 使用Condition实现等待/通知：比wait()和notify()/notyfyAll()更灵活，比如可实现多路通知。
    - 调用condition.await()前须先调用lock.lock()获得同步监视器。
3. Object与Condition方法对比

Object | Conditon
--- | ---
wait() | await()
wait(long timeout) | await(long time,TimeUnit unit)
notify() | signal()
notifyAll() | signalAll()

4. Condition API

方法 | 说明
--- | ---
int getHoldCount() | 查询当前线程保持此锁定的个数，即调用lock()方法的次数
int getQueueLength() | 返回正在等待获取此锁定的线程估计数
int getWaitQueueLength(Condition condition) | 返回等待与此锁定相关的给定条件Conditon的线程估计数
boolean hasQueueThread(Thread thread) | 查询指定的线程是否正在等待获取此锁定
boolean hasQueueThreads() | 查询是否有线程正在等待获取此锁定
boolean hasWaiters(Condition) | 查询是否有线程正在等待与此锁定有关的condition条件
boolean isFair() | 	判断是不是公平锁
boolean isHeldByCurrentThread() | 	查询当前线程是否保持此锁定
boolean isLocked() | 查询此锁定是否由任意线程保持
void lockInterruptibly() | 如果当前线程未被中断，则获取锁定，如果已经被中断则出现异常
boolean tryLock() | 仅在调用时锁定未被另一个线程保持的情况下，才获取该锁定
boolean tryLock(long timeout,TimeUnit unit) | 如果锁定在给定等待时间内没有被另一个线程保持，且当前线程未被中断，则获取该锁定

5. 公平锁与非公平锁 
    - 公平锁表示线程获取锁的顺序是按照加锁的顺序来分配的，即FIFO先进先出。
    - 非公平锁是一种获取锁的抢占机制，随机获得锁。
6. ReentrantReadWriteLock类 
    - 读读共享
    - 写写互斥
    - 读写互斥
    - 写读互斥

#### 六、定时器
1. schedule API

方法 | 说明
--- | ---
schedule(TimerTask task, Date time) | 在指定的日期执行某一次任务
scheduleAtFixedRate(TimerTask task, Date firstTime, long period) | 在指定的日期之后按指定的间隔周期，无限循环的执行某一任务
schedule(TimerTask task, long delay) | 以执行此方法的当前时间为参考时间，在此时间基础上延迟指定的毫秒数后执行一次TimerTask任务
schedule(TimerTask task, long delay, long period) | 以执行此方法的当前时间为参考时间，在此时间基础上延迟指定的毫秒数，再以某一间隔时间无限次数地执行某一TimerTask任务

2. schedule和scheduleAtFixedRate的区别:schedule不具有追赶执行性;scheduleAtFixedRate具有追赶执行性。

#### 七、单例与多线程
1. 立即加载/“饿汉模式”：调用方法前，实例已经被创建了。通过静态属性new实例化实现的。
2. 延迟加载/“懒汉模式”：调用get()方法时实例才被创建。最常见的实现办法是在get()方法中进行new实例化 。
    - 缺点：多线程环境中，会出问题。
    - 解决方法 ：
        - 声明synchronized关键字，但运行效率非常低下
        - 同步代码块，效率也低
        - 针对某些重要代码(实例化语句)单独同步，效率提升，但会出问题
        - 使用DCL双检查锁
        - 使用enum枚举数据类型实现单例模式

#### 七、补充
1. 线程的状态：Thread.State枚举类
    - BLOCKED 阻塞态
    - NEW   创建态
    - RUNNABLE  运行态
    - TERMINATED    结束态
    - TIMED_WAITING 指定时间休眠态
    - WAITING   休眠态
2. 线程组：线程组中可以有线程对象，也可以有线程组，组中还可以有线程。可批量管理线程或线程组对象。
3. SimpleDateFormat非线程安全，解决办法有：
    - 创建多个SimpleDateFormat类的实例
    - 使用ThreadLocal类
4. 线程组出现异常的处理
    - setUncaughtExceptionHandler() 给指定线程对线设置异常处理器
    - setDefaultUncaughtExceptionHandler() 对所有线程对象设置异常处理器
   

转载自 https://blog.csdn.net/h3243212/article/details/51180173