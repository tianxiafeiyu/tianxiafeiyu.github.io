---
title: python编程技巧
date: 2022-12-15 23:22:29
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - python编程技巧
---
## 避免过多的if else
表驱动方法编程（Table-Driven Methods）是一种编程模式,适用场景:消除代码中频繁的if else或switch case的逻辑结构代码,使代码更加直白.
```
def response(method):
    '''if 语句  黄哥Python培训 黄哥所写'''
    if method == "POST":
        return "/post"
    elif method == "GET":
        return "/get"
    elif method == "HEAD":
        return "/head"
    return "/"


def resposne_by_dict(method_dict, method):
    '''用字典代替if 语句  黄哥Python培训 黄哥所写 '''
    return method_dict.get(method, "/")


if __name__ == '__main__':
    method_dict = {
        "POST": "/post",
        "GET": "/get",
        "HEAD": "/head",
    }

    method = "POST"
    print(response(method))
    print(resposne_by_dict(method_dict, method))
```
```
假设让你实现一个返回每个月天数的函数（为简单起见不考虑闰年）。
static int monthDays[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
public static int getDayByMonth(int month){
　　if(month<1|| month>12){ 
　　　　throw new RuntimeException("month invalid parameter:"+month);
　　}
　　return monthDays[(month- 1)]; 
}
```