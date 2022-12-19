---
title: python多进程与多线程
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - python多进程与多线程
---

## 关于进程与线程
把进程比作一列火车，线程比作火车的一节车厢

*   线程在进程下行进（单纯的车厢无法运行）
*   一个进程可以包含多个线程（一辆火车可以有多个车厢）
*   不同进程间数据很难共享（一辆火车上的乘客很难换到另外一辆火车，比如站点换乘）
*   同一进程下不同线程间数据很易共享（A车厢换到B车厢很容易）
*   进程要比线程消耗更多的计算机资源（采用多列火车相比多个车厢更耗资源）
*   进程间不会相互影响，一个线程挂掉将导致整个进程挂掉（一列火车不会影响到另外一列火车，但是如果一列火车上中间的一节车厢着火了，将影响到所有车厢）
*   进程可以拓展到多机，进程最多适合多核（不同火车可以开在多个轨道上，同一火车的车厢不能在行进的不同的轨道上）
*   进程使用的内存地址可以上锁，即一个线程使用某些共享内存时，其他线程必须等它结束，才能使用这一块内存。（比如火车上的洗手间）－"互斥锁"
*   进程使用的内存地址可以限定使用量（比如火车上的餐厅，最多只允许多少人进入，如果满了需要在门口等，等有人出来了才能进去）－“信号量”

这里有几个知识点要重点记录一下

单个CPU在任一时刻只能执行单个线程，只有多核CPU才能真正做到多个线程同时运行 一个进程包含多个线程，这些线程可以分布在多个CPU上 多核CPU同时运行的线程可以属于单个进程或不同进程 所以，在大多数编程语言中因为切换消耗的资源更少，多线程比多进程效率更高

坏消息，Python是个特例！

## GIL锁

python始于1991年，创立初期对运算的要求不高，为了解决多线程共享内存的数据安全问题，引入了GIL锁，全称为Global Interpreter Lock，也就是全局解释器锁。

GIL规定，在一个进程中每次只能有一个线程在运行。这个GIL锁相当于是线程运行的资格证，某个线程想要运行，首先要获得GIL锁，然后遇到IO或者超时的时候释放GIL锁，给其余的线程去竞争，竞争成功的线程获得GIL锁得到下一次运行的机会。

正是因为有GIL的存在，python的多线程其实是假的，所以才有人说python的多线程非常鸡肋。但是虽然每个进程有一个GIL锁，进程和进程之前还是不受影响的。

GIL是个历史遗留问题，过去的版本迭代都是以GIL为基础来的，想要去除GIL还真不是一件容易的事，所以我们要做好和GIL长期面对的准备。

## 多进程 vs 多线程

那么是不是意味着python中就只能使用多进程去提高效率，多线程就要被淘汰了呢？

那也不是的。

这里分两种情况来讨论，CPU密集型操作和IO密集型操作。针对前者，大多数时间花在CPU运算上，所以希望CPU利用的越充分越好，这时候使用多进程是合适的，同时运行的进程数和CPU的核数相同；针对后者，大多数时间花在IO交互的等待上，此时一个CPU和多个CPU是没有太大差别的，反而是线程切换比进程切换要轻量得多，这时候使用多线程是合适的。

所以有了结论：

*   CPU密集型操作使用多进程比较合适，例如海量运算
*   IO密集型操作使用多线程比较合适，例如爬虫，文件处理，批量ssh操作服务器等等&#x20;

## 代码实现

待执行函数

```python
def func():
    print('process {} starts'.format(os.getpid()))
    time.sleep(2)
    print('process {} ends'.format(os.getpid()))
```

### 多进程

做为对比，首先来看看顺序执行两遍函数的情况

```python
if __name__ == '__main__':
    print('main process is {}'.format(os.getpid()))
    start_time = time.time()
    ### single process
    func()
    func()
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))

```

打印结果如下
```
main process is 24308
process 24308 starts
process 24308 ends
process 24308 starts
process 24308 ends
total time is 4.001222372055054
```
可以看到，这里是**单个进程**先后顺序执行了两遍函数，共耗时约4秒。

下面来看看**多进程**的情况

```python
if __name__ == '__main__':
    print('main process is {}'.format(os.getpid()))
    start_time = time.time()
    ### multiprocess
    from multiprocessing import Process
    p1 = Process(target=func)
    p2 = Process(target=func)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))

```

从主进程创建新的进程使用的是Process类，该类在实例化时通常接两个参数

target - 新的进程执行的函数的函数名
args - 函数的参数，元组格式传入
这里因为func函数没有参数需要传递，所以args没有赋值。

创建完Process对象以后通过start()方法来启动该进程，同时如果想让某个进程阻塞主进程，可以执行该进程的join()方法。正常情况下创建完子进程以后主进程会继续向下执行直到结束，如果有子进程阻塞了主进程则主进程会等待该子进程执行完以后才向下执行。这里主进程会等待p1和p2两个子进程都执行完毕才计算结束时间。

打印结果如下
```
main process is 33536
process 25764 starts
process 11960 starts
process 25764 ends
process 11960 ends
total time is 2.3870742321014404
```
可以看到，创建的子进程和主进程的进程ID是不一样的，说明此时一共有三个进程在同时跑。最后的用时为2.387秒，几乎降到了顺序执行一半的程度，当然比单个函数执行的时间还是慢了点，说明进程的创建和停止还是需要耗时的。

### 进程池

从上面的例子可以看出，进程的创建和停止都是消耗资源的，所以进程绝不是越多越好。因为单个CPU核某时刻只能执行单个进程，所以最好的情况是将进程数量与CPU核数相等，这样可以最大化利用CPU。

这时就有一个问题出现了，进程数少还好说，进程数多了的话如何自动去维持一个固定的进程数目呢，这时候就要用到进程池了。进程池就是规定一个可容纳最大进程数目的池子，当池子中进程数目不足时自动添加新进程，从而将同时运行的进程数目维持在一个上限之内。这里的上限就应该是CPU的核数。

```python
if __name__ == '__main__':
	from multiprocessing import Process, cpu_count, Pool
    print('main process is {}'.format(os.getpid()))
    print('core number is {}'.format(cpu_count()))  # 8
    start_time = time.time()
	### multiprocess pool
    p = Pool(8)
    for i in range(14):
        p.apply_async(func)
    p.close()
    p.join()
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))

```

这里我首先利用`cpu_count()`方法计算了一下我这台电脑的CPU核数，8核，所以进程池的最大进程数目设定为8。

这里利用Pool类来创建进程池，传递一个参数是最大进程数。利用Pool对象的apply\_async()方法往进程池中添加待执行的任务（注意不是进程，只是任务），这里也可以利用map\_async(func,iterable)来添加，用来类似于内建的map()方法，不过需要待执行的函数带参数，类似下面这样
```python
    def func(n):
        print('process {} starts'.format(os.getpid()))
        time.sleep(n)
        print('process {} ends'.format(os.getpid()))
        
    ### multiprocess pool
        p = Pool(8)
        # for i in range(14):
        #     p.apply_async(func)
        p.map_async(func,range(14))
        p.close()
        p.join()
```
然后是close()方法，进程池不再接受新的任务（注意不是进程），以及terminate()方法，关闭主进程，此时未开始的子进程都不会执行了。同样的，想要让进程池去阻塞主进程可以用join()方法。注意join()一定要在close()或者terminate()之后。

上面的程序执行结果如下
```
main process is 12860
core number is 8
process 11956 starts
process 34224 starts
process 10596 starts
process 20596 starts
process 27668 starts
process 15604 starts
process 10820 starts
process 16632 starts
process 11956 ends
process 11956 starts
process 34224 ends
process 34224 starts
process 10596 ends
process 10596 starts
process 20596 ends
process 20596 starts
process 27668 ends
process 27668 starts
process 15604 ends
process 15604 starts
process 10820 ends
process 16632 ends
process 11956 ends
process 34224 ends
process 10596 ends
process 20596 ends
process 27668 ends
process 15604 ends
total time is 5.258298635482788
```
一共14个任务，在最大数目为8的进程池里面至少要执行两轮，同时加上进程启动和停止的消耗，最后用时5.258秒。

### 进程间通讯

前面说到进程间是相互独立的，不共享内存空间，所以在一个进程中声明的变量在另一个进程中是看不到的(包括全局变量)。这时候就要借助一些工具来在两个进程间进行数据传输了，其中最常见的就是队列了。

队列（queue）在生产消费者模型中很常见，生产者进程在队列一端写入，消费者进程在队列另一端读取。

首先创建两个函数，分别扮演生产者和消费者

```python
def write_to_queue(queue):
    for index in range(5):
        print('write {} to {}'.format(str(index), queue))
        queue.put(index)
        time.sleep(1)


def read_from_queue(queue):
    while True:
        result = queue.get(True)
        print('get {} from {}'.format(str(result), queue))
```

这两个函数都接受一个队列作为参数然后利用`put()`方法往其中写入或者`get()`方法来读取。生产者会连续写入5个数字，每次间隔1秒，消费者则会一直尝试读取。

```python
if __name__ == '__main__':
	from multiprocessing import Process, cpu_count, Pool
    print('main process is {}'.format(os.getpid()))
    print('core number is {}'.format(cpu_count()))  # 8
    start_time = time.time()
	### multiprocess queue
    from multiprocessing import Queue
    queue = Queue()
    pw = Process(target=write_to_queue, args=(queue,))
    pr = Process(target=read_from_queue, args=(queue,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```

注意这里在创建子进程的时候就用元组的形式传递了参数，如果元组只有一个元素，记住添加逗号，否则会被认为是单个元素而不是元组。同时这里**因为消费者是死循环，所以只是将生产者加入了阻塞**，生产者进程执行完毕以后停止消费者进程。

最后打印结果如下
```
main process is 28268
core number is 8
write 0 to <multiprocessing.queues.Queue object at 0x0000023C6B25BF88>
get 0 from <multiprocessing.queues.Queue object at 0x000002EF410B1C88>
write 1 to <multiprocessing.queues.Queue object at 0x0000023C6B25BF88>
get 1 from <multiprocessing.queues.Queue object at 0x000002EF410B1C88>
write 2 to <multiprocessing.queues.Queue object at 0x0000023C6B25BF88>
get 2 from <multiprocessing.queues.Queue object at 0x000002EF410B1C88>
write 3 to <multiprocessing.queues.Queue object at 0x0000023C6B25BF88>
get 3 from <multiprocessing.queues.Queue object at 0x000002EF410B1C88>
write 4 to <multiprocessing.queues.Queue object at 0x0000023C6B25BF88>
get 4 from <multiprocessing.queues.Queue object at 0x000002EF410B1C88>
total time is 5.603313446044922
```
### 多线程

首先创建一个函数用于测试

```python
import threading
def func2(n):
    print('thread {} starts'.format(threading.current_thread().name))
    time.sleep(2)
    print('thread {} ends'.format(threading.current_thread().name))
    return n
```

多线程使用的是`threading.Thread`类

```python
if __name__ == '__main__':
	print('main thread is {}'.format(threading.current_thread().name))
    start_time = time.time()
    ### multithread
    t1 = threading.Thread(target=func2, args=(1,))
    t2 = threading.Thread(target=func2, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```

基本用法和上面进程的`Process`差不多，打印的结果如下
``
main thread is MainThread
thread Thread-1 starts
thread Thread-2 starts
thread Thread-1 ends
thread Thread-2 ends
total time is 2.002077341079712
```
对比前面多进程的2.38秒，这里还是快了不少的。

### [线程池](https://so.csdn.net/so/search?q=%E7%BA%BF%E7%A8%8B%E6%B1%A0\&spm=1001.2101.3001.7020)

和进程一样，通常是使用线程池来完成自动控制线程数量的目的。但是这里就没有一个推荐的上限数量了，毕竟因为GIL的存在不管怎么样每次都只有一个线程在跑。

同时threading模块是不支持线程池的，python3.4以后官方推出了concurrent.futures模块来统一进程池和线程池的接口，这里关注一下线程池。

```python
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
if __name__ == '__main__':
	print('main thread is {}'.format(threading.current_thread().name))
    start_time = time.time()
    ### threadpool
    executor = ThreadPoolExecutor(5)
    all_tasks = [executor.submit(func2, i) for i in range(8)]
    wait(all_tasks, return_when=ALL_COMPLETED)
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```

这里利用ThreadPoolExecutor()创建一个线程池，最大上限为5，然后利用submit()方法往线程池中添加任务（注意是任务，不是线程），submit方法会返回一个future对象，注意这里我将创建的任务放进了一个列表中。

如果要阻塞主线程，不能用join方法了，需要用到wait()方法，该方法接受三个参数，第一个参数是一个future对象的列表，第二个参数是超时时间，这里放空，第三个参数是在什么时候结束阻塞，默认是ALL\_COMPLETED表示全部任务结束之后，也可以设定为FIRST_COMPLETED表示第一个任务结束以后。

打印结果如下
```
main thread is MainThread
thread ThreadPoolExecutor-0_0 starts
thread ThreadPoolExecutor-0_1 starts
thread ThreadPoolExecutor-0_2 starts
thread ThreadPoolExecutor-0_3 starts
thread ThreadPoolExecutor-0_4 starts
thread ThreadPoolExecutor-0_0 ends
thread ThreadPoolExecutor-0_0 starts
thread ThreadPoolExecutor-0_2 ends
thread ThreadPoolExecutor-0_2 starts
thread ThreadPoolExecutor-0_1 ends
thread ThreadPoolExecutor-0_1 starts
thread ThreadPoolExecutor-0_3 ends
thread ThreadPoolExecutor-0_4 ends
thread ThreadPoolExecutor-0_0 ends
thread ThreadPoolExecutor-0_2 endsthread ThreadPoolExecutor-0_1 ends

total time is 4.003619432449341
```

最后的结果也是接近两倍的函数耗时4秒，比进程池快了不止一点点。

### map

这里需要额外提一下多线程中的map方法。

多进程中的`map_async()`方法和多线程中的`map()`方法除了将任务加入线程池，还会**按添加的顺序**返回每个线程的执行结果，这个执行结果也很特殊，是一个生成器

```python
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
if __name__ == '__main__':
	print('main thread is {}'.format(threading.current_thread().name))
    start_time = time.time()
    ### map
    executor = ThreadPoolExecutor(5)
    all_results = executor.map(func2, range(8))  # map返回的是线程执行的结果的生成器对象
    for result in all_results:
        print(result)
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```

这里的`all_results`是一个生成器，可以通过for循环来按顺序获取每个线程的返回结果。同时值得注意的是**map方法并不会阻塞主线程，也没法使用wait方法**，只能通过获取生成器的结果来阻塞主线程了。

执行结果如下
```
main thread is MainThread
thread ThreadPoolExecutor-0_0 starts
thread ThreadPoolExecutor-0_1 starts
thread ThreadPoolExecutor-0_2 starts
thread ThreadPoolExecutor-0_3 starts
thread ThreadPoolExecutor-0_4 starts
thread ThreadPoolExecutor-0_0 ends
thread ThreadPoolExecutor-0_0 starts
0
thread ThreadPoolExecutor-0_1 ends
thread ThreadPoolExecutor-0_1 starts
thread ThreadPoolExecutor-0_2 ends
1
thread ThreadPoolExecutor-0_2 starts
2
thread ThreadPoolExecutor-0_3 ends
3
thread ThreadPoolExecutor-0_4 ends
4
thread ThreadPoolExecutor-0_0 ends
5
thread ThreadPoolExecutor-0_1 ends
6
thread ThreadPoolExecutor-0_2 ends
7
total time is 4.004628419876099
```
### 异步

想要不用map方法又要异步获取线程的返回值，还可以用`as_completed()`方法

```python
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, as_completed
if __name__ == '__main__':
	print('main thread is {}'.format(threading.current_thread().name))
    start_time = time.time()
    executor = ThreadPoolExecutor(5)
    all_tasks = [executor.submit(func2, i) for i in range(8)]
    for future in as_completed(all_tasks):
        print(future.result())
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```
```
main thread is MainThread
thread ThreadPoolExecutor-0_0 starts
thread ThreadPoolExecutor-0_1 starts
thread ThreadPoolExecutor-0_2 starts
thread ThreadPoolExecutor-0_3 starts
thread ThreadPoolExecutor-0_4 starts
thread ThreadPoolExecutor-0_0 endsthread ThreadPoolExecutor-0_1 ends
thread ThreadPoolExecutor-0_1 starts
1
thread ThreadPoolExecutor-0_2 ends
thread ThreadPoolExecutor-0_2 starts
2

thread ThreadPoolExecutor-0_0 starts
thread ThreadPoolExecutor-0_3 ends
thread ThreadPoolExecutor-0_4 ends
0
3
4
thread ThreadPoolExecutor-0_1 ends
5
thread ThreadPoolExecutor-0_0 ends
7
thread ThreadPoolExecutor-0_2 ends
6
total time is 4.003146648406982
```
这里的线程结果就不是按照就不是按照添加任务的顺序，而是按照返回的先后顺序打印的。

所以，想要获取多线程的返回结果，按照添加顺序就用map方法，按照返回的先后顺序就用as\_completed方法。

想要更深入了解python中的futures模块，可以参考下面的文章学习下源码分析

<https://www.jianshu.com/p/b9b3d66aa0be>

同时python中还有专门做异步编程的asyncio模块，以后有时间再专门写文章说明。

### 线程间通讯

与多进程的内存独立不同，多线程间可以共享内存，所以同一个变量是可以被多个线程共享的，不需要额外的插件。想要让多个线程能同时操作某变量，要么将该变量作为参数传递到线程中（必须是可变变量，例如list和dict），要么作为全局变量在线程中用global关键字进行声明。

因为有GIL的存在，每次只能有一个线程在对变量进行操作，有人就认为python不需要互斥锁了。但是实际情况却和我们想的相差很远，先看下面这个例子:
```python
    def increase(var):
        global total_increase_times
        for i in range(1000000):
            var[0] += 1
            total_increase_times += 1


    def decrease(var):
        global total_decrease_times
        for i in range(1000000):
            var[0] -= 1
            total_decrease_times += 1
            
            
    if __name__ == '__main__':
        print('main thread is {}'.format(threading.current_thread().name))
        start_time = time.time()
        var = [5]
        total_increase_times = 0
        total_decrease_times = 0
        t1 = threading.Thread(target=increase, args=(var,))
        t2 = threading.Thread(target=decrease, args=(var,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(var)
        print('total increase times: {}'.format(str(total_increase_times)))
        print('total decrease times: {}'.format(str(total_decrease_times)))
        end_time = time.time()
        print('total time is {}'.format(str(end_time - start_time)))
```
这里首先定义了两个函数，分别对传进来的list的第一个元素进行加一和减一操作，重复多遍。这里之所以使用list因为要满足可变变量的要求，对于python中变量和传参不熟悉的朋友可以参考另一篇博客《python3中各类变量的内存堆栈分配和函数传参区别实例详解》。

然后在主线程中创建两个子线程分别运行，同时创建两个全局变量total\_increase\_times和total\_decrease\_times分别来统计对变量进行加值和减值的次数，为了防止可能由于操作次数不一致导致的错误。

打印结果如下
```
main thread is MainThread
[281970]
total increase times: 1000000
total decrease times: 1000000
total time is 0.7370336055755615
```

很奇怪，对变量值增加和减少同样的次数，最后的结果却和原先的值不一致。而且如果将该程序重复运行多次，每次得到的最终值都不同，有正有负。

这是为什么呢？

这是因为某些在我们看来是原子操作的，例如+或者-，在python看来不是的。例如执行a+=1操作，在python看来其实是三步：获取a的值，将值加1，将新的值赋给a。在这三步中的任意位置，该线程都有可能被暂停，然后让别的线程先运行。这时候就有可能出现如下的局面:

```python
线程1获取了a的值为10，被暂停
线程2获取了a的值为10
线程2将a的值赋值为9，被暂停
线程1将a的值赋值为11，被暂停
线程2获取了a的值为11
...
```

这样线程1就将线程2的操作全部覆盖了，这也就是为什么最后的结果有正有负。

那么如何处理这种情况呢？

需要用到互斥锁。

#### 互斥锁

线程1在操作变量a的时候就给a上一把锁，别的线程看到变量有锁就不会去操作该变量，一直到线程1再次获得GIL之后继续操作将锁释放，别的线程才有机会对该变量进行操作。

修改下上面的代码

```python
def increase(var, lock):
    global total_increase_times
    for i in range(1000000):
        if lock.acquire():
            var[0] += 1
            lock.release()
            total_increase_times += 1


def decrease(var, lock):
    global total_decrease_times
    for i in range(1000000):
        if lock.acquire():
            var[0] -= 1
            lock.release()
            total_decrease_times += 1
            
            
if __name__ == '__main__':
    print('main thread is {}'.format(threading.current_thread().name))
    start_time = time.time()
    lock = threading.Lock()
    var = [5]
    total_increase_times = 0
    total_decrease_times = 0
    t1 = threading.Thread(target=increase, args=(var, lock))
    t2 = threading.Thread(target=decrease, args=(var, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(var)
    print('total increase times: {}'.format(str(total_increase_times)))
    print('total decrease times: {}'.format(str(total_decrease_times)))
    end_time = time.time()
    print('total time is {}'.format(str(end_time - start_time)))
```

这里创建了一个全局锁lock并传递给两个线程，利用`acquire()`方法获取锁，**如果没有获取到锁该线程会一直卡在这，并不会继续循环**，操作完毕用`release()`方法释放锁。

打印结果如下

    main thread is MainThread
    [5]
    total increase times: 1000000
    total decrease times: 1000000
    total time is 2.1161584854125977

最终的结果不管执行多少次都没有问题，但是因为前面说的等待锁的过程会造成大量时间的浪费，这里耗时2.116秒比前面的0.737秒要慢了3倍。

这里不能像进程中那样用terminate方法停止一个线程，需要用`setDaemon`方法。

打印结果如下
```
main thread is MainThread
write 0 to <queue.Queue object at 0x000001E3DACD21C8>
get 0 from <queue.Queue object at 0x000001E3DACD21C8>
write 1 to <queue.Queue object at 0x000001E3DACD21C8>
get 1 from <queue.Queue object at 0x000001E3DACD21C8>
write 2 to <queue.Queue object at 0x000001E3DACD21C8>
get 2 from <queue.Queue object at 0x000001E3DACD21C8>
write 3 to <queue.Queue object at 0x000001E3DACD21C8>
get 3 from <queue.Queue object at 0x000001E3DACD21C8>
write 4 to <queue.Queue object at 0x000001E3DACD21C8>
get 4 from <queue.Queue object at 0x000001E3DACD21C8>
total time is 5.00357986831665
```
## 扩展

多进程间的变量共享也可以用类似多线程那样传递变量或者全局变量的方式，限于篇幅这里没有展开说，感兴趣的朋友可以参考知乎上一篇不错的文章https\://zhuanlan.zhihu.com/p/68828849

### multiprocessing中的共享变量

## 总结

总结下文章中涉及的知识点

- CPU密集型使用多进程，IO密集型使用多线程

- 查看进程ID和线程ID的命令分别是os.getpid()和threading.current_thread()

- 多进程使用multiprocessing就可以了，通常使用进程池来完成操作，阻塞主进程使用join方法

- 多线程使用threading模块，线程池使用concurrent.futures模块，同时主线程的阻塞方法有多种

- 不管多进程还是多线程，生产消费模型都可以用队列来完成，如果要用多线程操作同一变量记得加锁

## 参考资料
- https://blog.csdn.net/Victor2code/article/details/109005171
- https://www.zhihu.com/question/25532384/answer/411179772