---
title: 各种语言版本的 Helloworld
date: 2022-12-15 23:10:53
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - 各种语言版本的 Helloworld
---
接触过C、C++、Java、C#、Python、Go，自认为接触过的编程语言很多了，那么各种语言的经典程序 Hello World 都是什么样的呢？

### C

```
#include <stdio.h>

void main()
{
    printf("Hello,World!");
    return (0);
}
```

### C++

```
#include <iostream>
using namespace std;
void main()                 
{
    cout << "Hello,World!\n";
}
```

### Java

```
public class Helloworld {
    public static void main(String[] args) {
        System.out.println("Hello,World!");
    }
}
```

### C#

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
namespace log{
    class helloworld{
        static void  Main(string[] args){
            Console.WriteLine("Hello,World!");
        }
    }
} 
```

### Python

Python2.x

```
print "Hello,World!"
```

Python3.x

```
print("Hello,World!")
```

### Go

```
package main
import "fmt"
func main(){
    fmt.Printf("Hello,World!\n");
}
```

### Javascript

```
console.log("Hello,World!");
```