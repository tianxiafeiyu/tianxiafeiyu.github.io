---
title: Java 归并排序【转】
date: 2022-12-15 23:12:09
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java 归并排序【转】
---
# 归并排序

### 1、原理

归并排序是一种概念上最简单的排序算法，与快速排序一样，归并排序也是基于分治法的。归并排序将待排序的元素序列分成两个长度相等的子序列，为每一个子序列排序，然后再将他们合并成一个子序列。合并两个子序列的过程也就是两路归并。

### 2、复杂度

归并排序是一种稳定的排序算法，归并排序的主要问题在于它需要一个与待排序数组一样大的辅助数组空间。由于归并排序每次划分时两个子序列的长度基本一样，所以归并排序最好、最差和平均时间复杂度都是nlog2n。 

我们可以通过下图非常容易看懂归并排序的过程： 

![归并排序过程](https://note.youdao.com/yws/api/personal/file/F94C8510579B48B38D52AC97D3E6C1B7?method=download&shareKey=65d334fbb49d6f315cc8421850dd33a4)

时间复杂度：

![归并排序复杂度](https://note.youdao.com/yws/api/personal/file/E039B66FD79B46A4937A8C90D1AD018A?method=download&shareKey=f45e4224c86dbd0af47e81c6b20cb574)

### 3、完整Java代码

```
import org.junit.Test;
public class MergeSort {
    //两路归并算法，两个排好序的子序列合并为一个子序列
    public void merge(int []a,int left,int mid,int right){
        int []tmp=new int[a.length];//辅助数组
        int p1=left,p2=mid+1,k=left;//p1、p2是检测指针，k是存放指针

        while(p1<=mid && p2<=right){
            if(a[p1]<=a[p2])
                tmp[k++]=a[p1++];
            else
                tmp[k++]=a[p2++];
        }

        while(p1<=mid) tmp[k++]=a[p1++];//如果第一个序列未检测完，直接将后面所有元素加到合并的序列中
        while(p2<=right) tmp[k++]=a[p2++];//同上

        //复制回原素组
        for (int i = left; i <=right; i++) 
            a[i]=tmp[i];
    }

    public void mergeSort(int [] a,int start,int end){
        if(start<end){//当子序列中只有一个元素时结束递归
            int mid=(start+end)/2;//划分子序列
            mergeSort(a, start, mid);//对左侧子序列进行递归排序
            mergeSort(a, mid+1, end);//对右侧子序列进行递归排序
            merge(a, start, mid, end);//合并
        }
    }

    @Test
    public void test(){
        int[] a = { 49, 38, 65, 97, 76, 13, 27, 50 };
        mergeSort(a, 0, a.length-1);
        System.out.println("排好序的数组：");
        for (int e : a)
            System.out.print(e+" ");
    }
}
```

原文链接：https://blog.csdn.net/qq_36442947/article/details/81612870