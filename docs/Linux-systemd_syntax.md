# systemd.syntax -- 通用配置语法



* 此配置语法适用于 ***systemd*** 以及相关程序的配置文件：
  * **systemd 单元文件**:  `systemd.unit(5)`, `systemd.service(5)`, `systemd.socket(5)`, `systemd.device(5)`, `systemd.mount(5)`, `systemd.automount(5)`, `systemd.swap(5)`, `systemd.target(5)`, `systemd.path(5)`, `systemd.timer(5)`, `systemd.slice(5)`, `systemd.scope(5)`
  * **守护进程配置文件**：例如 `systemd-system.conf(5)`, logind.conf(5), `journald.conf(5)`, `journal-remote.conf(5)`, `journal-upload.conf(5)`, `systemd-sleep.conf(5)`, `timesyncd.conf(5)`

* 每个配置文件都是纯文本文件
* 文件内容由一个个小节组成，每个小节都由一个 "`[标题]`" 格式的标题行开始， 后面跟着一行行 *`key`*=*`value`* 格式的配置项。

* 空行、以 "`#`" 或 "`;`" 开头的行(用作注释) 都将被忽略。
* 行尾的反斜线 "`\`"是续行符，表示将下一行拼接到本行末尾，同时将反斜线本身替换为一个空格。这样可以将一个超长的行分拆为几个较短的行。 虽然单行长度的上限很大(当前是 1 MB)，但是依然建议不要使用太长的单行，而应该分拆为几个较短的行，或者在条件允许的情况下，使用多个指令、变量替换，或配置文件允许的其他方法来避免超长的单行。 当续行符之后紧跟一行或多行注释时，整个注释块都将被忽略，续行符将跳过整个注释块，而与注释块后面的内容进行拼接。

    ```ini
    [Section A]
    KeyOne=value 1
    KeyTwo=value 2
    
    # 一行注释
    
    [Section B]
    Setting="something" "some thing" "…"
    KeyTwo=value 2 \
           value 2 continued
    
    [Section C]
    KeyThree=value 2\
    # 这一行将被忽略
    ; 这一行也会被忽略
           value 2 continued
    ```

* 配置文件中的**布尔值**可以有多种写法。 真值可以写为： `1`, `yes`, `true`, `on` 之一，假值可以写为： `0`, `no`, `false`, `off` 之一。
* 配置文件中的**时间长度**可以有多种写法(详见`systemd.time(7)`手册)：
  * 不带任何后缀的一个纯数值表示秒数，如 "`50`" 表示50秒；
  * 亦可在纯数值后面加上时间单位，可使用的时间单位如下： "`s`", "`min`", "`h`", "`d`", "`w`", "`ms`", "`us`" ，如 "`50s`" 也表示50秒；
  * 亦可以将多个带有时间单位后缀的时间长度使用空格连接起来，表示这几段时间长度之和，如 "`2min 200ms`" 表示2分200毫秒，也就是120200毫秒；。

* 很多配置选项都允许多次使用，但是对于多次使用的解释可能有所不同：

  * 一般来说，多次使用同一个配置选项表示将多次设置的列表融合成一个更大的列表；

  * 但是若设为空则表示清空该配置选项之前所有已经设置的列表。 这种情况一定会在该配置选项的说明中提到。 

    >  注意，允许多次设置同一配置选项是不兼容于 XDG `.desktop` 文件格式的。
