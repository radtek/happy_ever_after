## 1. 常用快捷键
### 移动类

|快捷键|作用|
|-|-|
|ctrl+a|移动光标至行首|
|ctrl+e|移动光标至行尾|
|ctrl+f|→|
|ctrl+b|←|
|ctrl+p|上一条命令|
|ctrl+n|下一条命令|

### 剪切

|快捷键|作用|
|-|-|
|ctrl+k|剪切光标所在位置至行尾|
|ctrl+u|剪切光标所在位置至行首|
|ctrl+w|往前剪切一个单词|
|ctrl+y|粘贴由 ctrl+k、u、w剪切|
|ctrl+shift+- (即 ctrl+_ )|撤销之前的操作|

### 其他

|快捷键|作用|
|-|-|
|ctrl+h|删除光标前面的字母|
|ctrl+d|1. 删除光标后面的字母；<br>2. logout；|
|ctrl+t|光标前两个字符互换位置|
|ESC-b |往回(左)移动一个单词|
|ESC-f |往后(右)移动一个单词|

|快捷键|作用|
|-|-|
|ctrl+r|从历史命令中搜索|
|ctrl+g|从ctrl+r中退出|
|ctrl+o|执行已经当前输入的命令，并将命令自动填充，准备下一次执行(等同于执行完命令，在按ctrl+p或者上箭头选择上一条命令)|

|快捷键|作用|
|-|-|
|Ctrl+s |阻止屏幕输出|
|Ctrl+q |允许屏幕输出|


# 2.设置终端命令提示符($PS1)

### 默认设置

```bash
echo $PS1
	[\u@\h \W]\$
```
### PS1变量设置

|特殊符号|含义|
|-|-|
|\d|代表日期，格式为weekday month date，例如："Mon Aug1"|
|\H|完整的主机名称。例如：我的机器名称为：fc4.linux，则这个名称就是fc4.linux|
|\h|仅取主机的第一个名字，如上例，则为fc4，.linux则被省略 |
|\t|显示时间为24小时格式，如：HH:MM:SS |
|\T|显示时间为12小时格式 |
|\A|显示时间为24小时格式：HH:MM |
|\u|当前用户的账号名称|
|\v|BASH的版本信息|
|\w|完整的工作目录名称。家目录会以 ~代替|
|\W|利用basename取得工作目录名称，所以只会列出最后一个目录|
|\#|下达的第几个命令|
|\$|提示字符，如果是root时，提示符为：# ，普通用户则为：$|

#### 设置变量彩色

> 1. `\[\e[F;Bm\]`   
> 2. `\e[F;Bm`

其中F为字体颜色，编号30-37；B为背景色，编号40-47

>> 颜色对照表

|前景F|背景B|颜色|
|-|-|-|
|30|40|黑色|
|31|41|红色|
|32|42|绿色|
|33|43|黃色|
|34|44|蓝色|
|35|45|紫红|
|36|46|青蓝|
|37|47|白色|

>> 特殊代码对照表

|代码|意义|
|-|-|
|0|OFF|
|1|高亮显示|
|4|underline|
|5|闪烁|
|7|反白显示|
|8|不可见|

For example:   
```bash
PS1="[\[\e[34;1m\]\u@\[\e[0m\]\[\e[32;1m\]\h\[\e[0m\]\[\e[31;1m\] \w\[\e[0m\]]\\$ "
PS1="[\[\e[34;1m\]\u@\[\e[0m\]\[\e[32;1m\]\h\[\e[31;1m\] \w\[\e[0m\]]\\$ "
```


![效果图][PS1_Picture]</center>

#### 总结与扩展

> PS1	主提示符变量,也是默认提示符变量  
> PS2   换行提示符(命令较长时需要换行)  
> PS3   如下示例  
> PS4	bash -x 追踪命令执行时的提示符，默认为+  

示例 : 

```bash
#! /bin/bash

#ps3_test1.sh

select i in mon tue wed exit
do
    case $i in
        mon) echo "Monday";;
        tue) echo "Tuesday";;
        wed) echo "Wednesday";;
        exit) exit;;
    esac
done
```	

```bash
#! /bin/bash 

#ps3_test2.sh

PS3='##?'     #ps3_test2.sh多这一行
select i in mon tue wed exit
do
    case $i in
        mon) echo "Monday";;
        tue) echo "Tuesday";;
        wed) echo "Wednesday";;
        exit) exit;;
    esac
done
```

```	
bash ps3_test1.sh 
	1) mon
	2) tue
	3) wed
	4) exit
	#? 1
	Monday
	# 此处的#?即由PS3设置的
```

```
bash ps3_test2.sh
	1) mon
	2) tue
	3) wed
	4) exit
	##?1
	Monday
	已经变为##?
```


## 3. 设备名

|Type|示例|
|-|-|
|IDE|/dev/hda, /dev/hda1|
|SAS/SATA/SCSI|/dev/sda, /dev/sda1|



## 4. echo输出彩色

> 详情可参考： [Linux-echo](./Linux-echo.md)

`\033[B;Fm STRING \033[0m`

B,F取值参考上面表格，B,F的位置可以互换








<!-------------------以下是引用------------------->

<!---------Link--------->

<!---------Picture--------->
[PS1_Picture]:data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIcAAAAPCAIAAABBZkvoAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUDSURBVFhH7ZhfTFp3FMcP/gEKbaG382qaOOGKD+1YMKLtg0ldKY3JXkyW8kBq4qYJPvjg23iwy7Jse2DJHnwwGSaaNHHhgezBp8UMdTbxYbVkOkmWTXoFaxd7zRgYQRCUnd+9FwQFC1Ebk/rJL8I95/4ucM4933OukpaWFrjgnFEhvl5wnhBqhel3u20MOfbYjXYP7zkbZPcnmkxa4X1ipntlelV4n4+m03vrMkSXjHN+0VIUnaOn0yy+99ufTJ3llz8RZofXwX9RdtRicbK8rRjZWsFzjcjppURLD87r7PP1evEYISm5cw248ZWhbo6DdOuE6DgBmIkR4+QCCyFOtPCob7t7rD8fJKxMjmw3dwx4ew4t0VUieL8jltH8fGA9kFzhi5gznrepYCbaFI0pf18bHkvAKucal7yeFT3nH8/ciBHTLyys4GgIwqLrRDAML1EIyx7kK6tgDrDn1ZXKOn+dBjmdzdvs2tDjLbqvabBXJlog4mp/6QM4YuRqD2QqQ+Df39JXaGk6ui7T3xFMycjsX989RgkyMEAxIBWsEJgyBhuJginqQCmYQqOTLmcYmGar20AJpjy9wlu7q/EyhL4nFqq/y2pTC44M4QXL5DMotD3/mvhBU9BReHsmOOT6D6Tw4tmIPSiaSicn0gdtI0tG3I6rFYUKKojakNDH1u6p2jH6n1RCgBtu9w2PJyCstP5I3yxgVC13+3iNim+RJPmGcD2KKWEnJU3rtQl4FQ3h2tzbEz+orhakq0suIwnTxrKmkZRyDUmJ59cRewAgStkMOmw27hu7JGfi3Uo5um7n/yiBkHMyq2m8vuHCmBberus37C5nT3uCuS+yXbw49rw2W3VIu7vgLJYSRU/r3Zm7ZH35Hv6OmzPNzaInH9ZpIYLGtw5sHEThMnVxXFZiryEyjWpDIss62zn5PRmXrPKNYbiBG+N86t01zaXmAkYZLV4hB62M5uB6tDL0SsL9vU/9J6G4/ZTo22DB/8NiiL9/f/pUqIDNDYwg3oxsJATJbTQwaoqkCgcB1PQOHSizN3hJFNkeYsN1H5KRYcDRwBveANVv0K1KKM9iTp7yqWnoSW3B5vocJDS3WgdVyn/2q0XXUVDA2BcsMI1MroBBlfh65mhlEKuoSldHpBCHdFVSkgpjvsuAUVFcGKJB10OSv7Ipth0rw8k3c8dHA17sH1idxXWJae60yXcg7vu86DkaBaZBkoxtfPV8b7y1oesG2jYFVz5ZATN78XMRt9ecmc7K6PaJ5dkEXZ3S99FYCnQfrQ9L3w/sLBYwJsg4tIp/K+Mgrz3UYHAUq5FVXpPKNVcSBWqqKJ6gn1Zvaw1tJY1V4RAL0m2gGjMd4vjt2MwtS9jAt80aHTk+sp0H5Y7i5JeOKRTsisHn3X8sfBaMQSzY+/Spiaw/RV8exwhYWbXCja24NHqrCUdePpzYSx6hcHGFjEhkepzGKcA0oTfhETaS9VQ8Fqv/QIFH2FEqAa5izyidwJRFjZ0Z1YYPHOZ9yfUwoHN3tWW6C8W7hDbudy61YRu3dQ3Y0EPa9Ru3I377pPCEdHQ7Dgtt5jgplKIdpWyIgP2CAvYgX8CKz2CnDhnqrkJynh/b3llKi/Tbe16JLM8oVAHV/T4yQ+u/rv/4m9wHzAtyyWaFsbm9SM4D5mnj+2LFmwa6t+nbeVQ8VTtE3qmiMTtIfA8/oRTm4n/G5w+A/wGEsqTnvZZLlgAAAABJRU5ErkJggg==