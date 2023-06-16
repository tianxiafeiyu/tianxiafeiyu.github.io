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

## 元素的 id 和 class 属性
在 HTML 中，id 和 class 是用于标识和描述元素的属性。

id 属性用于唯一标识一个元素。每个 id 属性的值在文档中必须是唯一的，不能重复。可以使用 id 属性来为元素创建锚点，或者使用 JavaScript 来操作特定的元素。

例如，以下代码为一个段落元素添加了一个唯一的 id 属性：
```
<p id="my-paragraph">这是一个段落。</p>
```

class 属性用于描述元素的类别。一个元素可以有多个 class 属性，每个 class 属性的值可以是相同的或不同的。可以使用 class 属性来为元素应用样式，或者使用 JavaScript 来选择一组元素。

例如，以下代码为一个段落元素添加了一个 class 属性：
```
<p class="important">这是一个重要的段落。</p>
```

总的来说，id 属性用于唯一标识一个元素，而 class 属性用于描述元素的类别。在 CSS 中，可以使用 # 符号来选择 id 属性，使用 . 符号来选择 class 属性。在 JavaScript 中，可以使用 getElementById() 方法来选择 id 属性，使用 getElementsByClassName() 方法来选择 class 属性。

id 选择器的优先级比 class 选择器的优先级更高。这意味着，如果一个元素同时具有 id 和 class 属性，并且这两个属性都有相应的 CSS 规则，那么 id 属性的 CSS 规则将覆盖 class 属性的 CSS 规则。

## CSS常用属性
1. color：用于设置文本颜色，可以使用颜色名称、十六进制值、RGB值等方式来指定颜色。
1. font-size：用于设置字体大小，可以使用像素、百分比、em等单位来指定大小。
1. font-family：用于设置字体系列，可以指定多个字体，如果第一个字体不可用，则会尝试使用下一个字体。
1. font-weight：用于设置字体粗细，可以设置为normal、bold、bolder、lighter或者数字值。
1. text-align：用于设置文本对齐方式，可以设置为left、right、center、justify等。
1. background-color：用于设置背景颜色，可以使用颜色名称、十六进制值、RGB值等方式来指定颜色。
1. background-image：用于设置背景图片，可以指定图片的URL地址。
1. background-position：用于设置背景图片位置，可以指定像素值、百分比等方式来指定位置。
1. background-repeat：用于设置背景图片重复方式，可以设置为repeat、repeat-x、repeat-y、no-repeat等。
1. border：用于设置边框样式、宽度和颜色，可以分别指定边框样式、宽度和颜色，也可以使用简写方式指定。
1. padding：用于设置元素的内边距，可以指定像素值、百分比等方式来指定内边距。
1. margin：用于设置元素的外边距，可以指定像素值、百分比等方式来指定外边距。
1. display：用于设置元素的显示方式，可以设置为block、inline、inline-block、none等。
1. position：用于设置元素的定位方式，可以设置为static、relative、absolute、fixed等。
1. top、right、bottom、left：用于设置元素的定位位置，可以指定像素值、百分比等方式来指定位置。
1. float：用于设置元素的浮动方式，可以设置为left、right、none等。
1. clear：用于清除浮动，可以设置为left、right、both、none等。
1. width、height：用于设置元素的宽度和高度，可以指定像素值、百分比等方式来指定大小。
1. line-height：用于设置行高，可以指定像素值、百分比等方式来指定行高。
1. text-decoration：用于设置文本装饰效果，如下划线、删除线等。
1. text-transform：用于设置文本大小写转换方式，可以设置为uppercase、lowercase、capitalize等。
1. text-indent：用于设置文本缩进，可以指定像素值、em等单位来指定缩进大小。
1. white-space：用于设置空白符处理方式，可以设置为normal、nowrap、pre、pre-wrap等。
1. opacity：用于设置元素透明度，可以指定0到1之间的值，0表示完全透明，1表示完全不透明。
1. z-index：用于设置元素的堆叠顺序，可以指定正整数值，值越大，元素越靠前。
1. text-align-last：用于设置最后一行文本的对齐方式，可以设置为left、right、center、justify等。
1. text-justify：用于设置文本对齐方式，可以设置为auto、inter-word、inter-character、distribute等。
1. text-shadow：用于设置文本阴影效果，可以指定阴影的颜色、位置、模糊半径等属性。
1. box-shadow：用于设置盒子阴影效果，可以指定阴影的颜色、位置、模糊半径、扩展半径等属性。
1. border-radius：用于设置边框圆角效果，可以指定四个角的半径值，也可以指定单个角的半径值。
1. box-sizing：用于设置盒子模型的计算方式，可以设置为content-box、border-box等。
1. overflow：用于设置元素内容溢出时的处理方式，可以设置为visible、hidden、scroll、auto等。
1. text-overflow：用于设置文本溢出时的处理方式，可以设置为clip、ellipsis等。
1. word-wrap：用于设置长单词或URL地址的换行方式，可以设置为normal、break-word等。
1. cursor：用于设置鼠标指针的样式，可以设置为default、pointer、text等。
1. background-size：用于设置背景图片的大小，可以指定像素值、百分比等方式来指定大小。
1. background-attachment：用于设置背景图片的滚动方式，可以设置为scroll、fixed等。
1. transition：用于设置元素的过渡效果，可以指定过渡的属性、时间、延迟时间、过渡方式等属性。
1. transform：用于设置元素的变形效果，可以指定旋转、缩放、平移、倾斜等变形效果。
1. animation：用于设置元素的动画效果，可以指定动画的名称、时间、延迟时间、动画方式等属性。
