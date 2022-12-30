---
title: css知识点
date: 2022-12-15 23:25:17
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - css知识点
---

## css调整元素位置
https://blog.csdn.net/dyk11111/article/details/126666975

## 属性声明顺序
选择器中属性数量较多时，将相关的属性声明放在一起，并按以下顺序排列：

定位相关，如 position、top/bottom/left/right、z-index 等

盒模型相关，如 display、float、margin、width/height 等

排版相关，如 font、color、line-height 等

可视相关，如 background、color 等

其他，如 opacity、animation 等

建议：在属性数量较多时可以参考这 5 个类别归类排列。
```html
/* 定位相关 */
position: absolute;
top: 0;
right: 0;
bottom: 0;
left: 0;
z-index: 100;
/* 盒模型相关 */
display: block;
float: right;
width: 100px;
height: 100px;
/* 排版相关 */
font: normal 13px "Helvetica Neue", sans-serif;
line-height: 1.5;
color: #333;
text-align: center;
/* 可视相关 */
background-color: #f5f5f5;
border: 1px solid #e5e5e5;
border-radius: 3px;
/* 其他 */
opacity: 1;
```