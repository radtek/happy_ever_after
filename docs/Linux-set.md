set指令能设置所使用shell的执行方式，可依照不同的需求来做设置: 

```
　-a       标示已修改的变量，以供输出至环境变量。 
　-b       使被中止的后台程序立刻回报执行状态。 
　-C       转向所产生的文件无法覆盖已存在的文件。 
　-d       Shell预设会用杂凑表记忆使用过的指令，以加速指令的执行。使用-d参数可取消。 
　-e       若指令传回值不等于0，则立即退出shell。　　 
　-f       取消使用通配符。 
　-h 　    自动记录函数的所在位置。 
　-H Shell 可利用"!"加<指令编号>的方式来执行history中记录的指令。 
　-k 　    指令所给的参数都会被视为此指令的环境变量。 
　-l 　    记录for循环的变量名称。 
　-m 　    使用监视模式。 
　-n 　    只读取指令，而不实际执行。 
  -o Option
　-p 　    启动优先顺序模式。 
　-P 　    启动-P参数后，执行指令时，会以实际的文件或目录来取代符号连接。 
　-t 　    执行完随后的指令，即退出shell。 
　-u 　    当执行时使用到未定义过的变量，则显示错误信息。 
　-v 　    显示shell所读取的输入值。 
　-x 　    执行指令后，会先显示该指令及所下的参数。 
　+<参数>  取消某个set曾启动的参数。
```

About `-o Option-Name`: 

```
-a, -o allexport
-b, -o braceexpand
    -o emacs    Use an emacs-style command line editing interface. 
                This is enabled by default when the shell is interactive, unless the shell is started with the --noediting option. 
                This also affects the editing interface used for read -e.
-e, -o errexit   
-E, -o errtrace  
-T, -o functrace 
-h, -o hashall   
-H, -o histexpand
    -o history     Enable command history. This option is on by default in interactive shells.
    -o ignoreeof   The effect is as if the shell command 'IGNOREEOF=10' had been executed
-k, -o keyword   
-m, -o monitor   
-C, -o noclobber 
-n, -o noexec    
-f, -o noglob    
-b, -o notify    
-u, -o nounset   
-t, -o onecmd    
-P, -o physical  
    -o pipefail     If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, 
                    or zero if all commands in the pipeline exit successfully. This option is disabled by default.
    -o posix        Change the behavior of bash where the default operation differs from the POSIX standard to match the standard (posix mode).
-p, -o privileged 
-v, -o verbose 
    -o vi       Use a vi-style command line editing interface. This also affects the editing interface used for read -e.
-x, -o xtrace 

If -o is supplied with no option-name, the values of the current options are printed.  
If +o is supplied with no option-name, a series of set commands to recreate the current option settings is displayed on the standard output.
```



* 1.出错立即退出: `set -e`

* 2.命令回显: `set -x` 每条执行的命令都会先打印，然后才执行

* 3.脚本返回值为最后一个非零返回值: `set -o pipefail`

```sh
set -o pipefail
ls ./no_find_file.txt |echo "hi" >/dev/null
echo $?  # <= 输出1
```

* 43.模拟传入参数: `set --`

```sh
eval set -- <String>
eval set -- "${Variable}"

set -- <String>
set -- "${Variable}"
```

示例：

```
~]# parm="aaa bbb"

~]# eval set -- "${parm}"
~]# echo $*
aaa bbb
~]# echo $#
2

~]# set -- "${parm}"
~]# echo $#
1
~]# echo $*
aaa bbb
```



