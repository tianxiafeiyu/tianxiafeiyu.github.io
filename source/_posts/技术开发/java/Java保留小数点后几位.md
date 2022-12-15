#### 1. 使用 Math.round()
```java
float totalPrice = 11.21212
float num = (float)(Math.round(totalPrice*100)/100);//如果要求精确4位就*10000然后/10000
```

#### 2. 使用 DecimalFormat
```java
float price = 1.2;
DecimalFormat decimalFormat = new DecimalFormat(".00");//构造方法的字符格式这里如果小数不足2位,会以0补足.
String p = decimalFomat.format(price);//format 返回的是字符串
```