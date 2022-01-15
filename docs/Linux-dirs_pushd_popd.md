* `pushd`和`popd`在linux中可以用来方便地在多个目录之间切换
* `pushd`和`popd`是对一个目录栈进行操作，而`dirs`是显示目录栈的内容
* 目录栈的栈顶永远存放的是当前目录。如果当前目录发生变化，那么目录栈的栈顶元素肯定也变了；反过来，如果栈顶元素发生变化，那么当前目录肯定也变了。

```sh
$ dirs -v
 0  /mnt
 1  /etc/yum.repos.d
 2  /etc
 3  ~
```

## dirs -- Display directory stack

```
-c 清空目录栈
-l 列出栈中所有Index
-p 列出栈中所有Index(每行一条Index)
-v 列出栈中所有Index(每行一条Index, 且每行前带序号)

+N 显示序号为N的Index
-N 显示序号为N的Index(倒序)
```

## pushd -- Add directories to stack.

```
不带任何参数时 切换回上一次的目录(即序号为1的Index)
-n 仅操作堆栈, 不切换当前目录(即栈顶不发生改变)

+N 栈顶切换到序号为N的Index, 如果该Index的目录不存在, 该Index会被修改成当前目录
-N 栈顶切换到序号为N的Index(倒序)
DIR 目录切换到DIR, 并将DIR添加到栈顶
```

## popd -- Remove directories from stack.

```
不带任何参数时 弹出栈顶Index
-n 仅操作堆栈
   不带 +N/-N时，从栈底开始弹出Index
   +N 弹出序号为N的Index，如果Index为栈顶，则N+1
   -N 弹出序号为N的Index(倒序)，如果Index为栈顶，则N-1

+N 弹出序号为N的Index
-N 弹出序号为N的Index(倒序)
```
