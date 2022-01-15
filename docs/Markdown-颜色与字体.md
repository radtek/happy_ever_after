# Markdown

## 1.说明

本文主要叙述如何写出更加优美的markdown文档。在我们观看文档的过程中，良好的格式将会带来很大的收益。对于不同颜色的字体也并不会显得花里胡哨，只会让我们表达的内容更加的清晰。下面来具体的看一下操作的流程。

## 2. 文字的居中， 右对齐

对于标准的markdown文本，是不支持居中对齐的。还好markdown支持html语言，所以我们采用html语法格式即可。（有些markdown编辑器不支持）

```markdown
<center>这一行需要居中</center>
<div align = center>这一行需要居中</div>
<div align = left>这一行需要靠左</div>
<div align = right>这一行需要靠右</div>
```

```markdown
<p align="right">右对齐</p>
<p align="left">左对齐</p>
```

<p align="right">右对齐</p>

<p align="left">左对齐</p>

## 3.文字的字体及颜色

### 3.1 字体更换

同样我们也需要遵照其标准的语法格式

```markdown
<font face="黑体">我是黑体字</font>
```

下面是测试结果

<font face="黑体">我是黑体字</font>

### 3.2 大小更换

大小为size

```markdown
<font face="黑体" size=10>我是黑体字</font>
```

<font face="黑体" size=10>我是黑体字</font>

### 3.3 颜色替换


对于html语音中，颜色是用color来表示，所以可以表示如下

```markdown
<font color=red size=2>注意！！！</font>
<font color=orange size=4>注意！！！</font>
<font color=#0000FF size=6>注意！！！</font>
<font color=#FF00FF size=8>注意！！！</font>
```

效果如下

<font color=red size=2>注意！！！</font>

<font color=orange size=4>注意！！！</font>

<font color=#0000FF size=6>注意！！！</font>

<font color=#FF00FF size=8>注意！！！</font>


