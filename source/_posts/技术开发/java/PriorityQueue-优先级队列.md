#### 一、什么是优先级队列
PriorityQueue类在Java1.5中引入。PriorityQueue是基于优先堆的一个无界队列，这个优先队列中的元素可以默认自然排序或者通过提供的Comparator（比较器）在队列实例化的时排序。要求使用Java Comparable和Comparator接口给对象排序，并且在排序时会按照优先级处理其中的元素。

优先级队列底层的数据结构其实是一棵二叉堆

#### 二、使用
```Java
public class PriorityQueueTest {
    public static void main(String[] args) {
        // 不用比较器，默认升序排列，每次出列都是队列中最大元素，相当于小顶堆
        Queue<Integer> minHeap = new PriorityQueue<>();

        // 降序排列，每次出列都是队列中最小元素，相当于大顶堆
        Queue<Integer> maxHeap1 = new PriorityQueue<>((a, b) -> b - a);
        Queue<Integer> maxHeap2 = new PriorityQueue<>(new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o2 - o1;
            }
        });

        int[] nums = {1, 7, 3, 9, 5};
        for(int num : nums){
            minHeap.add(num);   // 添加元素
            maxHeap1.add(num);
            maxHeap2.add(num);
        }

        int a = minHeap.peek(); // 获得队首元素，不出列
        int b = minHeap.poll(); // 获得队首元素并出列，队列为空返回 null
        int c = minHeap.remove();  // 获得队首元素并出列, 队列为空报错

        System.out.println(a + "," + b + "," + c);  // 1,1,3
        System.out.println(maxHeap1.peek() + "," + maxHeap1.poll() + "," + maxHeap1.remove());  // 9,9,7
    }
}
```