---
title: Java获取时间工具类
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Java获取时间工具类
---
```java
public class CalendarUtil {
    /**
     * 获取当前时间
     * @Param format：时间格式，例：yyyy-MM-dd HH:mm:ss
     * @return
     */
    public static String getTimeNow(String format){
        Calendar calendar= Calendar.getInstance();
        SimpleDateFormat dateFormat= new SimpleDateFormat(format);
        return dateFormat.format(calendar.getTime());
    }

    /**
     * 获取当前时间的前n天
     * @Param format：时间格式，例：yyyy-MM-dd HH:mm:ss
     * @return
     */
    public static String getTimeDayBefore(int n, String format){
        Calendar calendar= Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_MONTH, - n); 
        SimpleDateFormat dateFormat= new SimpleDateFormat(format);
        return dateFormat.format(calendar.getTime());
    }

    /**
     * 更加自由的时间字符串获取
     * @param n 当前时间之间 n 个单位
     * @param step 步进单位，如 Calendar.MONTH(2)
     * @param format 时间格式，如：yyyy-MM-dd HH:mm:ss
     * @return
     */
    public static String getTimeBefore(int n, int step, String format){
        Calendar calendar= Calendar.getInstance();
        calendar.add(step, - n); 
        SimpleDateFormat dateFormat= new SimpleDateFormat(format);
        return dateFormat.format(calendar.getTime());
    }
}
```