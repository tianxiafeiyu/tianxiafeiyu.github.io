---
title: Java优雅的关闭连接资源
date: 2022-12-15 23:38:01
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java优雅的关闭连接资源
---
## 背景
在Java中，如果打开了外部资源（文件、数据库连接、网络连接等），因为外部资源不由JVM管理，无法享用JVM的垃圾回收机制，我们必须在这些外部资源使用完毕后，手动关闭它们。如果我们不在编程时确保在正确的时机关闭外部资源，就会导致外部资源泄露，紧接着就会出现文件被异常占用，数据库连接过多导致连接池溢出等诸多很严重的问题。

## 传统关闭方式 try-catch-finally
```java
 public Object add(User user) {
        String sql = "insert into user values(?, ?)";
        Connection connection = null;
        PreparedStatement pstm = null;
        try{
            connection = defaultConnection();
            pstm = connection.prepareStatement(sql);

            pstm.setString(1, user.getName());
            pstm.setString(2, user.getAge());
            pstm.executeUpdate();
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            if(pstm != null){
                try {
                    pstm.close();
                }catch (Exception e){
                    e.printStackTrace();
                }finally {
                    if(connection != null){
                        try {
                            connection.close();
                        }catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }
        return user;
    }


private Connection defaultConnection(){
    Connection connection = null;
    try {
        Class.forName(driverClassName);
        return DriverManager.getConnection(url, username, password);
    }catch (Exception e){
        e.printStackTrace();
    }
    return connection;
}
```
这一连串的 try-catch-finally 简直是噩梦。。。

## 优雅释放资源 try-with-resource
try-with-resource 是 Java7 新增的语法糖，可以省略很多模板化的代码。在 try() 括号中定义的资源将会在 try 语句执行完毕后释放。

使用try-with-resource的前提：
- JDK1.7及以上的版本
- 资源必须实现AutoClosable接口（基本都会实现）

```java
public Object add(User user) {
    String sql = "insert into user values(?, ?)";
    try (
        Connection connection = defaultConnection();
        PreparedStatement pstm = connection.prepareStatement(sql)
    ) {
        pstm.setString(1, user.getName());
        pstm.setString(2, user.getAge());
        pstm.executeUpdate();
    }catch (Exception e){
        e.printStackTrace();
    }
    return user;
}

private Connection defaultConnection(){
    Connection connection = null;
    try {
        Class.forName(driverClassName);
        return DriverManager.getConnection(url, username, password);
    }catch (Exception e){
        e.printStackTrace();
    }
    return connection;
}
```

## 单例模式