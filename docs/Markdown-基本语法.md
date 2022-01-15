## 1. 标题

```markdown
# 111
## 222
...
###### 666666
yijie
=
erjie
--
```

## 2. 斜体

```markdown
*xieti*
```

## 3. 粗体

```markdown
**cuti**
```

### 粗斜体

```markdown
***cuxieti***
```

## 4 插入链接

```markdown
[哔哩哔哩](http://www.bilibili.com "title") title可以省略
```

```markdown
<http://www.bilibili.com>
```

扩展用法：

```markdown
[哔哩哔哩][wangzhi1]
[wangzhi1]:http://www.bilibili.com "title")
```


## 5. 插入图片

```markdown
![名称](链接 "title")	网页图片
```
```
![名称][tupian1]	
[tupian1]:链接 "title"
```
```
![](./tupian1)	本地图片-当前目录
![](tupian1)
![](zimulu/tupian2)	本地图片-子目录
```


## 6. 角注

```markdown
待解释文本[^er]

[^er]:jieshi
```

## 7. 引用

```markdown
> 123
>> 1234
>>> 12345
```

## 8. 代码块

```markdown
`daimakuai`

```daimakuai```
```

#### 代码区块

```markdown
    daima   //4个空格或一个tab
```

## 9. 分割线

```markdown
*-_ 
***
---
___
```

## 10. 上下标

```markdown
H<sub>2</sub>O
CO<sub>2</sub>
爆米<sup>TM</sup>
```

H<sub>2</sub>O

CO<sub>2</sub>

爆米<sup>TM</sup>


## 11. 插入空格、Tab

```markdown
&nbsp;
&ensp;
&emsp;
```


## 11. 删除线

```markdown
~~ABCDEFG~~
```

~~ABCDEFG~~

## 12. 下划线

```markdown
<u>下划线</u>
```

<u>下划线</u>

## 13. 合并单元格

```html
<table>
    <tr>
        <th>班级</th><th>课程</th><th>平均分</th>
    </tr>
    <tr>
        <td rowspan="3">1班</td><td>语文</td><td>100</td>
    </tr>
    <tr>
        <td>数学</td><td>100</td>
    </tr>
    <tr>
        <td>英语</td><td>100</td>
    </tr>
</table>
```