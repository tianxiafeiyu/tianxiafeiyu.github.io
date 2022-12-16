---
title: Java对象循环引用解法
date: 2022-12-15 23:38:00
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java对象循环引用解法
---
#### 前言
循环引用，或者说循环依赖，对象 A 持有对象 B 的引用，对象 B 又持有 A, 两个对象相互引用，或者多个对象形成引用环路。

- 序列化：对象转字节序列（toJson）。

- 反序列化：字节对象转对象（fromJson）。

在对象序列化的时候，循环引用会出现堆栈溢出的错误，因为字段将会无限的延伸，比如序列化对象 A 时候：
```
{
    A{
        B{
            A{
                B{
                    A{
                        ...
                    }
                }
            }
        }
    }
}
```
要解决循环引用的问题，就需要打断环。最好是在建模的时候就避免循环引用，当然，有时候循环引用是客观存在的，比如在父子关系的结构中。那么，在序列化的时候，就需要进行断环。

#### 解决方案

##### 1. @JsonIgnore
@JsonIgnore标注在属性上时候，直接忽略该属性，以断开无限递归，序列化或反序列化均忽略。当然如果标注在get、set方法中，则可以分开控制，序列化对应的是get方法，反序列化对应的是set方法。
```
class aDTO{

    //1. 直接忽略属性
     @JsonIgnore
    private B b;
    
    //2. 序列化时候忽略属性
     @JsonIgnore
    public B getB(){
        return b;
    }
    
    //3. 反序列化时候忽略属性
     @JsonIgnore
    public void setB(B b){
        this.b = b;
    }
}
```
**注意：当使用@JsonIgnore控制属性的序列化和反序列时，需要与@JsonProperty配合使用，比如要在序列化时忽略属性，在get方法上添加了@JsonIgnore注解，在set方法上添加@JsonProperty注解。否则，在反序列化时候也会被忽略。**


##### 2. @JsonBackReference和@JsonManagedReference
这两个注解通常配对使用，在父子结构中。

- 序列化(serialization)

@JsonBackReference标注的属性在序列化（serialization，即将对象转换为json数据）时，会被忽略（即结果中的json数据不包含该属性的内容）

@JsonManagedReference标注的属性则会被序列化。在序列化时，@JsonBackReference的作用相当于@JsonIgnore，此时可以没有@JsonManagedReference。

- 反序列化（deserialization）

如果没有@JsonManagedReference，则不会自动注入@JsonBackReference标注的属性（被忽略的父或子）

如果有@JsonManagedReference，则会自动注入自动注入@JsonBackReference标注的属性。

##### 3. @JsonIgnoreProperties
@JsonIgnoreProperties("xxx")标注在属性或对应的get（序列化）、set（反序列化）方法上,忽略被标对象的某个属性。

##### 4. @JsonIdentityInfo
@JsonIdentityInfo(generator=ObjectIdGenerators.IntSequenceGenerator.class, property="id")
- generator:唯一标识的类型

- Property 对象的唯一标识 ，无特殊需求的，一般都是对象的主键

jackson从2.0 增加注解@JsonIdentityInfo解决无限递归的问题,这种方法是，如果发现循环引用，在形成环的最后一步，会将被引用的对象置空，序列化后的结果可能会缺失一部分数据，导致数据不完整。如A->B->A , 最后返回的结果是中，A-B->null。

