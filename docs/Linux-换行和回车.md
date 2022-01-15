> `CR` 和 `LF` 最初是用于控制电传打印机（Teletype，所以 UNIX 里面有个 tty）
> - `CR` 把打印头移动到行首，
> - `LF` 把纸上卷一行
> 
> 操作系统中：
> - `\n` 对应是换行`LF`，英文是New line，表示换行; 
> - `\r` 对应是回车`CR`，英文是Carriage return，表示使光标移动到开头;


## 1. 文件中的换行符号

|系统|行结束||
|--|--|--|
|linux,unix|\n|LF|
|windows|\r\n|CRLF|
|旧Mac OS|\r|CR|

## 2. 常用转义符号的意义

转义|释义|对应16进制
--|--|--
\0|空字符|十六进制0x0000
\n|换行|十六进制0x000a
\r|回车|十六进制0x000d
\t|水平制表符|十六进制0x0009
\\|反斜杠|十六进制0x005c
\"|双引号|十六进制0x0022
\'|单引号|十六进制0x0027

## 3. vim中回车键

`ctrl+M`: `^M`  也称回车键

通过`vim -b xxx` 可以查看到`^M`


## 4. 关于Linux系统对\n的处理

理论上以下命令：

```
printf "first line\nsecond line
```

输出应该是

```
first line
               second line
```

因为这里只有换行，没有回车。而不管是在 Windows 还是 Unix 上，前面这样的输出都是:

```
first line
second line
```

理论上只有

```
printf "first line\r\nsecond line
printf "first line\n\rsecond line
```

这两种情况下，输出才应该是

```
first line
second line
```

因此，准确来说，在linux上处理`\n`时，是"**换行并移动到行首**"