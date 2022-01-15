单元文件是 `ini` 风格的纯文本文件。封装了有关下列对象的信息： 服务(**service**)、套接字(**socket**)、设备(**device**)、挂载点(**mount**)、自动挂载点(**automount**)、 启动目标(**target**)、交换分区或交换文件(**swap**)、被监视的路径(**path**)、任务计划(**timer**)、 资源控制组(**slice**)、一组外部创建的进程(**scope**)。



本手册列出了各类单元所共有的配置选项(亦称"配置指令"或"单元属性")， 这些选项位于单元文件的 `[Unit]` 或 `[Install]` 小节。除了通用的 `[Unit]` 与 `[Install]` 小节之外， 每种单元还有各自专属的小节。 详见各种单元的手册： `systemd.service(5)`, `systemd.socket(5)`, `systemd.device(5)`, `systemd.mount(5)`, `systemd.automount(5)`, `systemd.swap(5)`, `systemd.target(5)`, `systemd.path(5)`, `systemd.timer(5)`, `systemd.slice(5)`, `systemd.scope(5)`



单元文件可以通过一个"实例名"参数从"模板文件" 构造出来(这个过程叫"**实例化**")。 

* "**模板文件**" (也称"模板单元"或"单元模板") 是定义一系列同类型单元的基础。 模板文件的名称必须以 "`@`" 结尾(在类型后缀之前，如`teamd@.service`)。 
* 通过实例化得到的单元，其完整的单元名称是在模板文件的类型后缀与 "`@`" 之间插入实例名称形成的。在通过实例化得到的单元内部， 可以使用 "`%i`" 以及其他说明符来引用实例参数， 详见后文。

除了手册中列出的选项之外，单元文件还可以包含更多其他选项。 无法识别的选项不会中断单元文件的加载，但是 systemd 会输出一条警告日志。 如果选项或者小节的名字以 `X-` 开头， 那么 systemd 将会完全忽略它。 以 `X-` 开头的小节中的选项没必要再以 `X-` 开头， 因为整个小节都已经被忽略。 应用程序可以利用这个特性在单元文件中包含额外的信息。

如果想要给一个单元赋予别名，那么可以按照需求，在系统单元目录或用户单元目录中， 创建一个软连接(以别名作为文件名)，并将其指向该单元的单元文件。 例如 `systemd-networkd.service` 在安装时就通过 `/usr/lib/systemd/system/dbus-org.freedesktop.network1.service` 软连接创建了 `dbus-org.freedesktop.network1.service` 别名。 此外，还可以直接在单元文件的 [Install] 小节中使用 `Alias=` 创建别名。 注意，单元文件中设置的别名会随着单元的启用(enable)与禁用(disable)而生效和失效， 也就是别名软连接会随着单元的启用(enable)与禁用(disable)而创建与删除。 例如，因为 `reboot.target` 单元文件中含有 `Alias=ctrl-alt-del.target` 的设置，所以启用(enable)此单元之后，按下 CTRL+ALT+DEL 组合键将会导致启动该单元。单元的别名可以用于 **enable**, **disable**, **start**, **stop**, **status**, … 这些命令中，也可以用于 `Wants=`, `Requires=`, `Before=`, `After=`, … 这些依赖关系选项中。 但是务必注意，不可将单元的别名用于 **preset** 命令中。 再次提醒，通过 `Alias=` 设置的别名仅在单元被启用(enable)之后才会生效。

对于例如 `foo.service` 这样的单元文件， 可以同时存在对应的 `foo.service.wants/` 与 `foo.service.requires/` 目录， 其中可以放置许多指向其他单元文件的软连接。 软连接所指向的单元将会被隐含的添加到 `foo.service` 相应的 `Wants=` 与 `Requires=` 依赖中。 这样就可以方便的为单元添加依赖关系，而无需修改单元文件本身。 向 `.wants/` 与 `.requires/` 目录中添加软连接的首选方法是使用 [systemctl(1)](http://www.jinbuguo.com/systemd/systemctl.html#) 的 **enable** 命令， 它会读取单元文件的 [Install] 小节(详见后文)。

对于例如 `foo.service` 这样的单元文件，可以同时存在对应的 `foo.service.d/` 目录， 当解析完主单元文件之后，目录中所有以 "`.conf`" 结尾的文件，都会被按照文件名的字典顺序，依次解析(相当于依次附加到主单元文件的末尾)。 这样就可以方便的修改单元的设置，或者为单元添加额外的设置，而无需修改单元文件本身。 注意，配置片段("`.conf`" 文件)必须包含明确的小节头(例如 "`[Service]`" 之类)。 对于从模板文件实例化而来的单元，会优先读取与此实例对应的 "`.d/`" 目录(例如 "`foo@bar.service.d/`")中的配置片段("`.conf`" 文件)， 然后才会读取与模板对应的 "`.d/`" 目录(例如 "`foo@.service.d/`")中的配置片段("`.conf`" 文件)。 对于名称中包含连字符("`-`")的单元，将会按特定顺序依次在一组(而不是一个)目录中搜索单元配置片段。 例如对于 `foo-bar-baz.service` 单元来说，将会依次在 `foo-.service.d/`, `foo-bar-.service.d/`, `foo-bar-baz.service.d/` 目录下搜索单元配置片段。这个机制可以方便的为一组相关单元(单元名称的前缀都相同)定义共同的单元配置片段， 特别适合应用于 mount, automount, slice 类型的单元， 因为这些单元的命名规则就是基于连字符构建的。 注意，在前缀层次结构的下层目录中的单元配置片段，会覆盖上层目录中的同名文件， 也就是 `foo-bar-.service.d/10-override.conf` 会覆盖(取代) `foo-.service.d/10-override.conf` 文件。

存放配置片段("`.conf`" 文件)的 "`.d/`" 目录， 除了可以放置在 `/etc/systemd/{system,user}` 目录中， 还可以放置在 `/usr/lib/systemd/{system,user}` 与 `/run/systemd/{system,user}` 目录中。 虽然在优先级上，`/etc` 中的配置片段优先级最高、`/run` 中的配置片段优先级居中、 `/usr/lib` 中的配置片段优先级最低。但是这仅对同名配置片段之间的覆盖关系有意义。 因为所有 "`.d/`" 目录中的配置片段，无论其位于哪个目录， 都会被按照文件名的字典顺序，依次覆盖单元文件中的设置(相当于依次附加到主单元文件的末尾)。

注意，虽然 systemd 为明确设置单元之间的依赖关系提供了灵活的方法， 但是我们反对使用这些方法，你应该仅在万不得已的时候才使用它。 我们鼓励你使用基于 D-Bus 或 socket 的启动机制， 以将单元之间的依赖关系隐含化， 从而得到一个更简单也更健壮的系统。

如上所述，单元可以从模板实例化而来。 这样就可以用同一个模板文件衍生出多个单元。 当 systemd 查找单元文件时，会首先查找与单元名称完全吻合的单元文件， 如果没有找到，并且单元名称中包含 "`@`" 字符， 那么 systemd 将会继续查找拥有相同前缀的模板文件， 如果找到，那么将从这个模板文件实例化一个单元来使用。 例如，对于 `getty@tty3.service` 单元来说， 其对应的模板文件是 `getty@.service` (也就是去掉 "`@`" 与后缀名之间的部分)。

可以在模板文件内部 通过 "`%i`" 引用实例字符串(也就是上例中的"tty3")， 详见后面的小节。

如果一个单元文件的大小为零字节或者是指向 `/dev/null` 的软连接， 那么它的所有相关配置都将被忽略。同时，该单元将被标记为 "`masked`" 状态，并且无法被启动。 这样就可以 彻底屏蔽一个单元(即使手动启动也不行)。

单元文件的格式在未来将保持稳定(参见 [Interface Stability Promise](https://www.freedesktop.org/wiki/Software/systemd/InterfaceStabilityPromise))。



## 单元名称中的字符转义

有时需要将任意字符串(可以包含任意非NUL字符)转化为合法有效的单元名称。 为了达成这个目标，必须对特殊字符进行转义。 一个典型的例子是，为了便于识别，需要将某些单元的名称精确对应到文件系统上的对象。 例如将 `dev-sda.device` 与 `/dev/sda` 精确对应。

转义规则如下：(1)将 "`/`" 替换为 "`-`" ； (2)保持 ASCII字母与数字 不变； (3)保持 "`_`" 不变； (4)仅当 "`.`" 是首字符时将其替换为"\x2e"，否则保持不变； (5)将上述 1~4 之外的所有其他字符替换为C风格的"\x??"转义序列。

对于文件系统路径来说，"/"的转义规则略有不同，具体说来就是： (1)单纯的根目录"/"将被替换为"-"； (2)将其他路径首尾的"/"删除后再将剩余的"/"替换为"-"。 例如 `/foo//bar/baz/` 将被转义为 "`foo-bar-baz`"

只要知道转义对象是否为文件系统路径， 这种转义规则就是完全可逆的。 [systemd-escape(1)](http://www.jinbuguo.com/systemd/systemd-escape.html#) 可以用来转义与还原字符串。使用 **systemd-escape --path** 转义文件系统路径， 使用 **systemd-escape** 转义其他字符串。



## 自动依赖



### 隐含依赖

许多依赖关系是根据单元的类型与设置自动隐含创建的。 这些隐含的依赖关系可以让单元文件的内容更加简洁清爽。 对于各类单元的隐含依赖关系， 可以参考对应手册页的"隐含依赖"小节。

例如，带有 `Type=dbus` 的 service 单元 将会自动隐含 `Requires=dbus.socket` 与 `After=dbus.socket` 依赖。详见 [systemd.service(5)](http://www.jinbuguo.com/systemd/systemd.service.html#) 手册。



### 默认依赖

默认依赖与隐含依赖类似，不同之处在于默认依赖可以使用 `DefaultDependencies=` 选项进行开关(默认值 `yes` 表示开启默认依赖，而设为 `no` 则表示关闭默认依赖)， 而隐含依赖永远有效。 对于各类单元的默认依赖关系，可以参考对应手册页的"默认依赖"小节。

例如，除非明确设置了 `DefaultDependencies=no` ，否则 target 单元将会默认添加对通过 `Wants=` 或 `Requires=` 汇聚的单元 的 `After=` 依赖。 详见 [systemd.target(5)](http://www.jinbuguo.com/systemd/systemd.target.html#) 手册。注意，可以通过设置 `DefaultDependencies=no` 来关闭默认行为。



## 单元目录(单元文件加载路径)

systemd 将会从一组在编译时设定好的"单元目录"中加载单元文件(详见下面的两个表格)， 并且较先列出的目录拥有较高的优先级(细节见后文)。 也就是说，高优先级目录中的文件， 将会覆盖低优先级目录中的同名文件。

如果设置了 `$SYSTEMD_UNIT_PATH` 环境变量， 那么它将会取代预设的单元目录。 如果 `$SYSTEMD_UNIT_PATH` 以 "`:`" 结尾， 那么预设的单元目录将会被添加到该变量值的末尾。



**表 1. 当 systemd 以系统实例(`--system`)运行时，加载单元的先后顺序(较前的目录优先级较高)：**

| 系统单元目录                    | 描述                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `/etc/systemd/system.control`   | 通过 dbus API 创建的永久系统单元                             |
| `/run/systemd/system.control`   | 通过 dbus API 创建的临时系统单元                             |
| `/run/systemd/transient`        | 动态配置的临时单元(系统与全局用户共用)                       |
| `/run/systemd/generator.early`  | 生成的高优先级单元(系统与全局用户共用)(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`early-dir`* 的说明) |
| `/etc/systemd/system`           | 本地配置的系统单元                                           |
| `/run/systemd/system`           | 运行时配置的系统单元                                         |
| `/run/systemd/generator`        | 生成的中优先级系统单元(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`normal-dir`* 的说明) |
| `/usr/local/lib/systemd/system` | 本地软件包安装的系统单元                                     |
| `/usr/lib/systemd/system`       | 发行版软件包安装的系统单元                                   |
| `/run/systemd/generator.late`   | 生成的低优先级系统单元(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`late-dir`* 的说明) |





**表 2. 当 systemd 以用户实例(`--user`)运行时，加载单元的先后顺序(较前的目录优先级较高)：**

| 用户单元目录                                                 | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `$XDG_CONFIG_HOME/systemd/user.control` 或 `~/.config/systemd/user.control` | 通过 dbus API 创建的永久私有用户单元(仅在未设置 `$XDG_CONFIG_HOME` 时才使用 `~/.config` 来替代) |
| `$XDG_RUNTIME_DIR/systemd/user.control`                      | 通过 dbus API 创建的临时私有用户单元                         |
| `/run/systemd/transient`                                     | 动态配置的临时单元(系统与全局用户共用)                       |
| `/run/systemd/generator.early`                               | 生成的高优先级单元(系统与全局用户共用)(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`early-dir`* 的说明) |
| `$XDG_CONFIG_HOME/systemd/user` 或 `$HOME/.config/systemd/user` | 用户配置的私有用户单元(仅在未设置 `$XDG_CONFIG_HOME` 时才使用 `~/.config` 来替代) |
| `/etc/systemd/user`                                          | 本地配置的全局用户单元                                       |
| `$XDG_RUNTIME_DIR/systemd/user`                              | 运行时配置的私有用户单元(仅当 $XDG_RUNTIME_DIR 已被设置时有效) |
| `/run/systemd/user`                                          | 运行时配置的全局用户单元                                     |
| `$XDG_RUNTIME_DIR/systemd/generator`                         | 生成的中优先级私有用户单元(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`normal-dir`* 的说明) |
| `$XDG_DATA_HOME/systemd/user` 或 `$HOME/.local/share/systemd/user` | 软件包安装在用户家目录中的私有用户单元(仅在未设置 `$XDG_DATA_HOME` 时才使用 `~/.local/share` 来替代) |
| `$dir/systemd/user`(对应 `$XDG_DATA_DIRS` 中的每一个目录(`$dir`)) | 额外安装的全局用户单元，对应 `$XDG_DATA_DIRS`(默认值="/usr/local/share/:/usr/share/") 中的每一个目录。 |
| `/usr/local/lib/systemd/user`                                | 本地软件包安装的全局用户单元                                 |
| `/usr/lib/systemd/user`                                      | 发行版软件包安装的全局用户单元                               |
| `$XDG_RUNTIME_DIR/systemd/generator.late`                    | 生成的低优先级私有用户单元(参见 [systemd.generator(7)](http://www.jinbuguo.com/systemd/systemd.generator.html#) 手册中对 *`late-dir`* 的说明) |



可以使用环境变量来 扩充或更改 systemd 用户实例(`--user`)的单元文件加载路径。 环境变量可以通过环境变量生成器(详见 [systemd.environment-generator(7)](http://www.jinbuguo.com/systemd/systemd.environment-generator.html#) 手册)来设置。特别地， `$XDG_DATA_HOME` 与 `$XDG_DATA_DIRS` 可以方便的通过 [systemd-environment-d-generator(8)](http://www.jinbuguo.com/systemd/systemd-environment-d-generator.html#) 来设置。这样，上表中列出的单元目录正好就是默认值。 要查看实际使用的、基于编译选项与当前环境变量的单元目录列表，可以使用

```
systemd-analyze --user unit-paths
```



此外，还可以通过 [systemctl(1)](http://www.jinbuguo.com/systemd/systemctl.html#) 的 **link** 命令 向上述单元目录中添加额外的单元(不在上述常规单元目录中的单元)。



## 单元垃圾回收

systemd 会在首次引用一个单元时自动加载该单元的配置， 并在不再需要该单元时自动卸载该单元的配置与状态(垃圾回收)。 可以通过多种不同机制引用单元：

1. 该单元是另外一个已加载单元的依赖，例如 `After=`, `Wants=`, …
2. 该单元正在启动(starting)、运行(running)、重新加载配置(reloading)、停止(stopping)
3. 该单元正处于失败(`failed`)状态(详见下文)
4. 该单元的一个任务正在排队等候执行
5. 该单元正在被一个活动的IPC客户端程序锁定
6. 该单元是一个特殊的"永久"单元，总是被加载并启动。 例如，根文件系统挂载点 `-.mount` 单元、以及 systemd(PID=1) 自身所在的 `init.scope` 单元。
7. 该单元拥有与其关联的、正在运行中的进程

可以使用 `CollectMode=` 选项设置垃圾回收策略， 也就是，是否允许自动卸载处于失败(`failed`)状态的单元 (详见下文)。

当一个单元的配置与状态被卸载之后，该单元的所有执行结果，除了已经记录在日志中的信息之外，所有其他信息， 例如，退出码、退出信号、资源占用，等等，都会消失。

即使单元的配置已经加载，也可以使用 **systemctl daemon-reload** 或其他等效命令，强制重新加载单元配置。 所有已经加载的配置都将被清空， 并被新加载的配置取代(当然，新配置未必就立即生效)， 同时所有运行时状态都会被保存并恢复。



## [Unit] 小节选项

单元文件中的 [Unit] 小节 包含与单元类型无关的通用信息。 可用的选项(亦称"指令"或"属性")如下：

- `Description=`

  有利于人类阅读的、对单元进行简单描述的字符串。将被 **systemd** 或其他程序用来标记此单元， 这个字符串应该只用于识别此单元即可，不需要过分说明。例如 "`Apache2 Web Server`" 就是一个好例子，而 "`high-performance light-weight HTTP server`" (太通用) 与 "`Apache2`" (信息太少) 则是两个坏例子。因为 **systemd** 将会把这个字符串用于状态信息中("`Starting *`description`*...`", "`Started *`description`*.`", "`Reached target *`description`*.`", "`Failed to start *`description`*.`")，所以这个字符串应该表现的像一个名词， 而不是一个完整的句子或带有动词的短语。比如 "`exiting the container`" 或 "`updating the database once per day.`" 就是典型的坏例子。

- `Documentation=`

  一组用空格分隔的文档URI列表， 这些文档是对此单元的详细说明。 可接受 "`http://`", "`https://`", "`file:`", "`info:`", "`man:`" 五种URI类型。 有关URI语法的详细说明，参见 [uri(7)](http://man7.org/linux/man-pages/man7/uri.7.html) 手册。 这些URI应该按照相关性由高到低列出。 比如，将解释该单元作用的文档放在第一个， 最好再紧跟单元的配置说明， 最后再附上其他文档。 可以多次使用此选项， 依次向文档列表尾部添加新文档。 但是，如果为此选项设置一个空字符串， 那么表示 清空先前已存在的列表。

- `Requires=`

  设置此单元所必须依赖的其他单元。当启动此单元时，也必须启动这里列出的所有其他单元。 如果此处列出的某个单元启动失败、并且恰好又设置了到这个失败单元的 `After=` 依赖，那么将不会启动此单元。此外，无论是否设置了到被依赖单元的 `After=` 依赖，只要某个被依赖的单元被显式停止，那么该单元也会被连带停止。 想要添加多个单元，可以多次使用此选项，也可以设置一个空格分隔的单元列表。 注意，此选项并不影响单元之间的启动或停止顺序。 要想调整单元之间的启动或停止顺序，请使用 `After=` 或 `Before=` 选项。 例如，在 `foo.service` 中设置了 `Requires=bar.service` ， 但是并未使用 `After=` 或 `Before=` 设定两者的启动顺序， 那么，当需要启动 `foo.service` 的时候，这两个单元会被并行的同时启动。 建议使用 `Wants=` 代替 `Requires=` 来设置单元之间的非致命依赖关系， 从而有助于获得更好的健壮性， 特别是在某些单元启动失败的时候。注意，设置了此依赖并不意味着当本单元处于运行状态时，被依赖的其他单元也必须总是处于运行状态。 例如：(1)失败的条件检查(例如后文的 `ConditionPathExists=`, `ConditionPathIsSymbolicLink=`, …)只会导致被依赖的单元跳过启动，而不会导致被依赖的单元启动失败(也就是进入"failed"状态)。 (2)某些被依赖的单元可能会自己主动停止(例如有的服务进程可能会主动干净的退出、有的设备可能被用户拔出)， 而不会导致本单元自身也跟着一起停止。 要想达到这样的效果，可以同时联合使用 `BindsTo=` 与 `After=` 依赖，这样就可以确保：在被依赖的其他单元没有处于运行状态时， 本单元自身永远不会启动成功(详见后文)。注意， 此种依赖关系也可以在单元文件之外通过向 `.requires/`目录中添加软连接来设置。 详见前文。

- `Requisite=`

  与 `Requires=` 类似。不同之处在于：当此单元启动时，这里列出的依赖单元必须已经全部处于启动成功的状态， 否则，此单元将会立即进入启动失败的状态，并且也不会启动那些尚未成功启动的被依赖单元。 因为 `Requisite=` 不隐含任何顺序依赖(即使两个单元在同一个事务中启动)， 所以，此选项经常与 `After=` 一起使用， 以确保此单元不会在启动时间上早于被依赖的单元。如果 `a.service` 中包含了 `Requisite=b.service` ，那么这个依赖关系将在 `b.service` 的属性列表中显示为 `RequisiteOf=a.service` 。 也就是说，不能直接设置 `RequisiteOf=` 依赖。

- `Wants=`

  此选项是 `Requires=` 的弱化版。 当此单元被启动时， 所有这里列出的其他单元只是尽可能被启动。 但是，即使某些单元不存在或者未能启动成功， 也不会影响此单元的启动。 推荐使用此选项来设置单元之间的依赖关系。注意， 此种依赖关系也可以在单元文件之外通过向 `.wants/` 目录中添加软连接来设置， 详见前文。

- `BindsTo=`

  与 `Requires=` 类似，但是依赖性更强： 如果这里列出的任意一个单元停止运行或者崩溃，那么也会连带导致该单元自身被停止。 这就意味着该单元可能因为 这里列出的任意一个单元的 主动退出、某个设备被拔出、某个挂载点被卸载， 而被强行停止。如果将某个被依赖的单元同时放到 `After=` 与 `BindsTo=` 选项中，那么效果将会更加强烈：被依赖的单元必须严格的先于本单元启动成功之后， 本单元才能开始启动。这就意味着，不但在被依赖的单元意外停止时，该单元必须停止， 而且在被依赖的单元由于条件检查失败(例如后文的 `ConditionPathExists=`, `ConditionPathIsSymbolicLink=`, …)而被跳过时， 该单元也将无法启动。正因为如此，在很多场景下，需要同时使用 `BindsTo=` 与 `After=` 选项。如果 `a.service` 中包含了 `BindsTo=b.service` ，那么这个依赖关系将在 `b.service` 的属性列表中显示为 `BoundBy=a.service` 。 也就是说，不能直接设置 `BoundBy=` 依赖。

- `PartOf=`

  与 `Requires=` 类似， 不同之处在于：仅作用于单元的停止或重启。 其含义是，当停止或重启这里列出的某个单元时， 也会同时停止或重启该单元自身。 注意，这个依赖是单向的， 该单元自身的停止或重启并不影响这里列出的单元。如果 `a.service` 中包含了 `PartOf=b.service` ，那么这个依赖关系将在 `b.service` 的属性列表中显示为 `ConsistsOf=a.service` 。 也就是说，不能直接设置 `ConsistsOf=` 依赖。

- `Conflicts=`

  指定单元之间的冲突关系。 接受一个空格分隔的单元列表，表明该单元不能与列表中的任何单元共存， 也就是说：(1)当此单元启动的时候，列表中的所有单元都将被停止； (2)当列表中的某个单元启动的时候，该单元同样也将被停止。 注意，此选项与 `After=` 和 `Before=` 选项没有任何关系。如果两个相互冲突的单元A与B 需要在同一个事务内作为B启动， 那么这个事务要么会失败(A与B都是事务中的必要部分[Requires])， 要么就是必须被修改(A与B中至少有一个是事务中的非必要部分)。 在后一种情况下， 将会剔除一个非必要的单元 (若两个都是非必要的单元， 则优先剔除A)。

- `Before=`, `After=`

  强制指定单元之间的先后顺序，接受一个空格分隔的单元列表。 假定 `foo.service` 单元包含 `Before=bar.service` 设置， 那么当两个单元都需要启动的时候， `bar.service` 将会一直延迟到 `foo.service` 启动完毕之后再启动。 注意，停止顺序与启动顺序正好相反，也就是说， 只有当 `bar.service` 完全停止后，才会停止 `foo.service` 单元。 `After=` 的含义与 `Before=` 正好相反。 假定 `foo.service` 单元包含 `After=bar.service` 设置， 那么当两个单元都需要启动的时候， `foo.service` 将会一直延迟到 `bar.service` 启动完毕之后再启动。 注意，停止顺序与启动顺序正好相反，也就是说， 只有当 `foo.service` 完全停止后，才会停止 `bar.service` 单元。 注意，此二选项仅用于指定先后顺序， 而与 `Requires=`, `Wants=`, `BindsTo=` 这些选项没有任何关系。 不过在实践中也经常遇见将某个单元同时设置到 `After=` 与 `Requires=` 选项中的情形。 可以多次使用此二选项，以将多个单元添加到列表中。 假定两个单元之间存在先后顺序(无论谁先谁后)，并且一个要停止而另一个要启动，那么永远是"先停止后启动"的顺序。 但如果两个单元之间没有先后顺序，那么它们的停止和启动就都是相互独立的，并且是并行的。 对于不同类型的单元来说，判断启动是否已经完成的标准并不完全相同。 特别的，对于设置在 `Before=`/`After=` 中的服务单元来说， 只有在服务单元内配置的所有启动命令全部都已经被调用，并且对于每一个被调用的命令， 要么确认已经调用失败、要么确认已经成功运行的情况下， 才能认为已经完成启动。

- `OnFailure=`

  接受一个空格分隔的单元列表。 当该单元进入失败("`failed`")状态时， 将会启动列表中的单元。使用了 `Restart=` 的服务单元仅在超出启动频率限制之后， 才会进入失败(failed)状态。

- `PropagatesReloadTo=`, `ReloadPropagatedFrom=`

  接受一个空格分隔的单元列表。 `PropagatesReloadTo=` 表示 在 reload 该单元时， 也同时 reload 所有列表中的单元。 `ReloadPropagatedFrom=` 表示 在 reload 列表中的某个单元时， 也同时 reload 该单元。

- `JoinsNamespaceOf=`

  接受一个空格分隔的单元列表， 表示将该单元所启动的进程加入到列表单元的网络及 临时文件(`/tmp`, `/var/tmp`)的名字空间中。 此选项仅适用于支持 `PrivateNetwork=` 与/或 `PrivateTmp=` 指令的单元(对加入者与被加入者都适用)。详见 [systemd.exec(5)](http://www.jinbuguo.com/systemd/systemd.exec.html#) 手册。 如果单元列表中 仅有一个单元处于已启动状态， 那么该单元将加入到 这个唯一已启动单元的名字空间中。 如果单元列表中 有多个单元处于已启动状态， 那么该单元将 随机加入一个已启动单元的 名字空间中。

- `RequiresMountsFor=`

  接受一个空格分隔的绝对路径列表，表示该单元将会使用到这些文件系统路径。 所有这些路径中涉及的挂载点所对应的 mount 单元，都会被隐式的添加到 `Requires=` 与 `After=` 选项中。 也就是说，这些路径中所涉及的挂载点都会在启动该单元之前被自动挂载。注意，虽然带有 `noauto` 标记的挂载点不会被 `local-fs.target` 自动挂载， 但是它并不影响此选项所设置的依赖关系。 也就是说，带有 `noauto` 标记的挂载点 依然会在启动该单元之前被自动挂载。

- `OnFailureJobMode=`

  可设为 "`fail`", "`replace`", "`replace-irreversibly`", "`isolate`", "`flush`", "`ignore-dependencies`", "`ignore-requirements`" 之一。 默认值是 "`replace`" 。 指定 `OnFailure=` 中列出的单元应该以何种方式排队。值的含义参见 [systemctl(1)](http://www.jinbuguo.com/systemd/systemctl.html#) 手册中对 `--job-mode=` 选项的说明。 如果设为 "`isolate`" ， 那么只能在 `OnFailure=` 中设置一个单独的单元。

- `IgnoreOnIsolate=`

  接受一个布尔值。设为 `yes` 表示在执行 **systemctl isolate ...** 命令时，此单元不会被停止。 对于 service, target, socket, timer, path 单元来说，默认值是 `false` ； 对于 slice, scope, device, swap, mount, automount 单元来说， 默认值是 `true` 。

- `StopWhenUnneeded=`

  如果设为 `yes` ， 那么当此单元不再被任何已启动的单元依赖时， 将会被自动停止。 默认值 `no` 的含义是， 除非此单元与其他即将启动的单元冲突， 否则即使此单元已不再被任何已启动的单元依赖， 也不会自动停止它。

- `RefuseManualStart=`, `RefuseManualStop=`

  如果设为 `yes` ， 那么此单元将拒绝被手动启动(`RefuseManualStart=`) 或拒绝被手动停止(`RefuseManualStop=`)。 也就是说， 此单元只能作为其他单元的依赖条件而存在， 只能因为依赖关系而被间接启动或者间接停止， 不能由用户以手动方式直接启动或者直接停止。 设置此选项是为了 禁止用户意外的启动或者停止某些特定的单元。 默认值是 `no`

- `AllowIsolate=`

  如果设为 `yes` ， 那么此单元将允许被 **systemctl isolate** 命令操作， 否则将会被拒绝。 唯一一个将此选项设为 `yes` 的理由，大概是为了兼容SysV初始化系统。 此时应该仅考虑对 target 单元进行设置， 以防止系统进入不可用状态。 建议保持默认值 `no`

- `DefaultDependencies=`

  默认值 `yes` 表示为此单元隐式地创建默认依赖。 不同类型的单元，其默认依赖也不同，详见各自的手册页。 例如对于 service 单元来说， 默认的依赖关系是指： (1)开机时，必须在基础系统初始化完成之后才能启动该服务； (2)关机时，必须在该服务完全停止后才能关闭基础系统。 通常，只有那些在系统启动的早期就必须启动的单元， 以及那些必须在系统关闭的末尾才能关闭的单元， 才可以将此选项设为 `no` 。 注意，设为 `no` 并不表示取消所有的默认依赖， 只是表示取消非关键的默认依赖。 强烈建议对绝大多数普通单元 保持此选项的默认值 `yes` 。

- `CollectMode=`

  设置此单元的"垃圾回收"策略。可设为 `inactive`(默认值) 或 `inactive-or-failed` 之一。默认值 `inactive` 表示如果该单元处于停止(`inactive`)状态，并且没有被其他客户端、任务、单元所引用，那么该单元将会被卸载。 注意，如果此单元处于失败(`failed`)状态，那么是不会被卸载的， 它会一直保持未卸载状态，直到用户调用 **systemctl reset-failed** (或类似的命令)重置了 `failed` 状态。设为 `inactive-or-failed` 表示无论此单元处于停止(`inactive`)状态还是失败(`failed`)状态， 都将被卸载(无需重置 `failed` 状态)。 注意，在这种"垃圾回收"策略下， 此单元的所有结果(退出码、退出信号、资源消耗 …) 都会在此单元结束之后立即清除(只剩下此前已经记录在日志中的痕迹)。

- `FailureAction=`, `SuccessAction=`

  当此单元停止并进入失败(`failed`)或停止(`inactive`)状态时，应当执行什么动作。 对于系统单元，可以设为 `none`, `reboot`, `reboot-force`, `reboot-immediate`, `poweroff`, `poweroff-force`, `poweroff-immediate`, `exit`, `exit-force` 之一。 对于用户单元，仅可设为 `none`, `exit`, `exit-force` 之一。两个选项的默认值都是 `none`默认值 `none` 表示 不触发任何动作。 `reboot`/`poweroff` 表示按照常规关机流程重启/关闭整个系统(等价于 **systemctl reboot|poweroff**)。 `reboot-force`/`poweroff-force` 表示强制杀死所有进程之后强制重启/关机， 虽然可能会造成应用程序数据丢失，但是不会造成文件系统不一致(等价于 **systemctl reboot|poweroff -f**)。 `reboot-immediate`/`poweroff-immediate` 表示强制立即执行 [reboot(2)](http://man7.org/linux/man-pages/man2/reboot.2.html) 系统调用重启/关机， 可能会造成数据丢失以及文件系统不一致(等价于 **systemctl reboot|poweroff -ff**)。 `exit` 表示按照常规关闭流程，按部就班的退出 systemd 系统管理器。 `exit-force` 表示立即强制退出 systemd 系统管理器(不再按部就班的逐一退出全部服务)。 当设为 `exit` 或 `exit-force` 时， systemd 系统管理器将会默认把此单元主进程的返回值(如果有)用作系统管理器自身的返回值。 当然，这个默认行为可以通过下面的 `FailureActionExitStatus=`/`SuccessActionExitStatus=` 进行修改。

- `FailureActionExitStatus=`, `SuccessActionExitStatus=`

  当 `FailureAction=`/`SuccessAction=` 的值为 `exit` 或 `exit-force` 之一，并且设定的动作被触发时，应该返回什么样退出码给容器管理器(对于系统服务) 或 systemd 系统管理器(对于用户服务)。 默认情况下，将会使用该单元主进程的退出码(如果有)。 取值范围是 0…255 之间的一个整数。 设为空字符串表示重置回默认行为。

- `JobTimeoutSec=`, `JobRunningTimeoutSec=`

  当该单元的一个任务(job)进入队列的时候， `JobTimeoutSec=` 用于设置从该任务进入队列开始计时、到该任务最终完成，最多可以使用多长时间， `JobRunningTimeoutSec=` 用于设置从该任务实际运行开始计时、到该任务最终完成，最多可以使用多长时间。 如果上述任意一个设置超时，那么超时的任务将被撤销，并且该单元将保持其现有状态不变(而不是进入 "`failed`" 状态)。 对于非 device 单元来说，`DefaultTimeoutStartSec=` 选项的默认值是 "`infinity`"(永不超时)， 而 `JobRunningTimeoutSec=` 的默认值等于 `DefaultTimeoutStartSec=` 的值。 注意，此处设置的超时不是指单元自身的超时(例如 `TimeoutStartSec=` 就是指单元自身的超时)， 而是指该单元在启动或者停止等状态变化过程中，等候某个外部任务完成的最长时限。 换句话说，适用于单元自身的超时设置(例如 `TimeoutStartSec=`)用于指定单元自身在改变其状态时，总共允许使用多长时间； 而此处设置的超时则是设置此单元在改变其状态的过程中，等候某个外部任务完成所能容忍的最长时间。

- `JobTimeoutAction=`, `JobTimeoutRebootArgument=`

  `JobTimeoutAction=` 用于指定当超时发生时(参见上文的 `JobTimeoutSec=` 与 `JobRunningTimeoutSec=` 选项)，将触发什么样的额外动作。 可接受的值与 `StartLimitAction=` 相同，默认值为 `none` 。 `JobTimeoutRebootArgument=` 用于指定传递给 [reboot(2)](http://man7.org/linux/man-pages/man2/reboot.2.html) 系统调用的字符串参数。

- `StartLimitIntervalSec=*`interval`*`, `StartLimitBurst=*`burst`*`

  设置单元的启动频率限制。 也就是该单元在 *`interval`* 时间内最多允许启动 *`burst`* 次。 `StartLimitIntervalSec=` 用于设置时长(默认值等于 systemd 配置文件(system.conf)中 `DefaultStartLimitIntervalSec=` 的值)，设为 0 表示没有限制。 `StartLimitBurst=` 用于设置在给定的时长内，最多允许启动多少次(默认值等于 systemd 配置文件(system.conf)中 `DefaultStartLimitBurst=` 的值)。 虽然此选项通常与 `Restart=` 选项(参见 [systemd.service(5)](http://www.jinbuguo.com/systemd/systemd.service.html#)) 一起使用， 但实际上，此选项作用于任何方式的启动(包括手动启动)，而不仅仅是由 `Restart=` 触发的启动。 注意，一旦某个设置了 `Restart=` 自动重启逻辑的单元触碰到了启动频率限制， 那么该单元将再也不会尝试自动重启； 不过，如果该单元在经过 *`interval`* 时长之后，又被手动重启成功的话，那么该单元的自动重启逻辑将会被再次激活。 注意，**systemctl reset-failed** 命令能够重置单元的启动频率计数器。 系统管理员在手动启动某个已经触碰到了启动频率限制的单元之前，可以使用这个命令清除启动限制。 注意，因为启动频率限制位于所有单元条件检查之后， 所以基于失败条件的启动不会计入启动频率限制的启动次数之中。 注意，这些选项对 slice, target, device, scope 单元没有意义， 因为这几种单元要么永远不会启动失败、要么只能成功启动一次。当一个单元因为垃圾回收(见前文)而被卸载的时候， 该单元的启动频率计数器也会被一起清除。 这就意味着对不被持续引用的单元设置启动频率限制是无效的。

- `StartLimitAction=`

  设置该单元在触碰了 `StartLimitIntervalSec=` 与 `StartLimitBurst=` 定义的启动频率限制时，将会执行什么动作。 可接受的值与 `FailureAction=`/`SuccessAction=` 相同，值的含义也相同。 默认值 `none` 表示除了禁止启动之外， 不触发任何其他动作。

- `RebootArgument=`

  当 `StartLimitAction=` 或 `FailureAction=` 触发重启动作时， 此选项的值就是传递给 [reboot(2)](http://man7.org/linux/man-pages/man2/reboot.2.html) 系统调用的字符串参数。 相当于 **systemctl reboot** 命令接收的可选参数。

- `ConditionArchitecture=`, `ConditionVirtualization=`, `ConditionHost=`, `ConditionKernelCommandLine=`, `ConditionKernelVersion=`, `ConditionSecurity=`, `ConditionCapability=`, `ConditionACPower=`, `ConditionNeedsUpdate=`, `ConditionFirstBoot=`, `ConditionPathExists=`, `ConditionPathExistsGlob=`, `ConditionPathIsDirectory=`, `ConditionPathIsSymbolicLink=`, `ConditionPathIsMountPoint=`, `ConditionPathIsReadWrite=`, `ConditionDirectoryNotEmpty=`, `ConditionFileNotEmpty=`, `ConditionFileIsExecutable=`, `ConditionUser=`, `ConditionGroup=`, `ConditionControlGroupController=`

  这组选项用于在启动单元之前，首先测试特定的条件是否为真。 若为假，则悄无声息地跳过此单元的启动(仅是跳过，而不是进入"`failed`"状态)。 注意，即使某单元由于测试条件为假而被跳过， 那些由于依赖关系而必须先于此单元启动的单元并不会受到影响(也就是会照常启动)。 可以使用条件表达式来跳过那些对于本机系统无用的单元， 比如那些对于本机内核或运行环境没有用处的功能。 如果想要单元在测试条件为假时， 除了跳过启动之外，还要在日志中留下痕迹(而不是悄无声息的跳过)， 可以使用对应的另一组 `AssertArchitecture=`, `AssertVirtualization=`, … 选项(见后文)。`ConditionArchitecture=` 检测是否运行于 特定的硬件平台： `x86`, `x86-64`, `ppc`, `ppc-le`, `ppc64`, `ppc64-le`, `ia64`, `parisc`, `parisc64`, `s390`, `s390x`, `sparc`, `sparc64`, `mips`, `mips-le`, `mips64`, `mips64-le`, `alpha`, `arm`, `arm-be`, `arm64`, `arm64-be`, `sh`, `sh64`, `m68k`, `tilegx`, `cris`, `arc`, `arc-be`, `native`(编译 systemd 时的目标平台)。 可以在这些关键字前面加上感叹号(!)前缀 表示逻辑反转。注意， `Personality=` 的值 对此选项 没有任何影响。`ConditionVirtualization=` 检测是否运行于(特定的)虚拟环境中： `yes`(某种虚拟环境), `no`(物理机), `vm`(某种虚拟机), `container`(某种容器), `qemu`, `kvm`, `zvm`, `vmware`, `microsoft`, `oracle`, `xen`, `bochs`, `uml`, `bhyve`, `qnx`, `openvz`, `lxc`, `lxc-libvirt`, `systemd-nspawn`, `docker`, `rkt`, `private-users`(用户名字空间)。参见 [systemd-detect-virt(1)](http://www.jinbuguo.com/systemd/systemd-detect-virt.html#) 手册以了解所有已知的虚拟化技术及其标识符。 如果嵌套在多个虚拟化环境内， 那么以最内层的那个为准。 可以在这些关键字前面加上感叹号(!)前缀表示逻辑反转。`ConditionHost=` 检测系统的 hostname 或者 "machine ID" 。 参数可以是：(1)一个主机名字符串(可以使用 shell 风格的通配符)， 该字符串将会与 本机的主机名(也就是 [gethostname(2)](http://man7.org/linux/man-pages/man2/gethostname.2.html) 的返回值)进行匹配；(2)或者是一个 "machine ID" 格式的字符串(参见 [machine-id(5)](http://www.jinbuguo.com/systemd/machine-id.html#) 手册)。 可以在字符串前面加上感叹号(!)前缀表示逻辑反转。`ConditionKernelCommandLine=` 检测是否设置了某个特定的内核引导选项。 参数可以是一个单独的单词，也可以是一个 "`var=val`" 格式的赋值字符串。 如果参数是一个单独的单词，那么以下两种情况都算是检测成功： (1)恰好存在一个完全匹配的单词选项； (2)在某个 "`var=val`" 格式的内核引导选项中等号前的 "`var`" 恰好与该单词完全匹配。 如果参数是一个 "`var=val`" 格式的赋值字符串， 那么必须恰好存在一个完全匹配的 "`var=val`" 格式的内核引导选项，才算检测成功。 可以在字符串前面加上感叹号(!)前缀表示逻辑反转。`ConditionKernelVersion=` 检测内核版本(**uname -r**) 是否匹配给定的表达式(或在字符串前面加上感叹号(!)前缀表示"不匹配")。 表达式必须是一个单独的字符串。如果表达式以 "`<`", "`<=`", "`=`", "`>=`", "`>`" 之一开头， 那么表示对内核版本号进行比较，否则表示按照 shell 风格的通配符表达式进行匹配。注意，企图根据内核版本来判断内核支持哪些特性是不可靠的。 因为发行版厂商经常将高版本内核的新驱动和新功能移植到当前发行版使用的低版本内核中， 所以，对内核版本的检查是不能在不同发行版之间随意移植的， 不应该用于需要跨发行版部署的单元。`ConditionSecurity=` 检测是否启用了 特定的安全技术： `selinux`, `apparmor`, `tomoyo`, `ima`, `smack`, `audit`, `uefi-secureboot` 。 可以在这些关键字前面加上感叹号(!)前缀表示逻辑反转。`ConditionCapability=` 检测 systemd 的 capability 集合中 是否存在 特定的 [capabilities(7)](http://man7.org/linux/man-pages/man7/capabilities.7.html) 。 参数应设为例如 "`CAP_MKNOD`" 这样的 capability 名称。 注意，此选项不是检测特定的 capability 是否实际可用，而是仅检测特定的 capability 在绑定集合中是否存在。 可以在名称前面加上感叹号(!)前缀表示逻辑反转。`ConditionACPower=` 检测系统是否 正在使用交流电源。 `yes` 表示至少在使用一个交流电源， 或者更本不存在任何交流电源。 `no` 表示存在交流电源， 但是 没有使用其中的任何一个。`ConditionNeedsUpdate=` 可设为 `/var` 或 `/etc` 之一， 用于检测指定的目录是否需要更新。 设为 `/var` 表示 检测 `/usr` 目录的最后更新时间(mtime) 是否比 `/var/.updated` 文件的最后更新时间(mtime)更晚。 设为 `/etc` 表示 检测 `/usr` 目录的最后更新时间(mtime) 是否比 `/etc/.updated` 文件的最后更新时间(mtime)更晚。 可以在值前面加上感叹号(!)前缀表示逻辑反转。 当更新了 `/usr` 中的资源之后，可以通过使用此选项， 实现在下一次启动时更新 `/etc` 或 `/var` 目录的目的。 使用此选项的单元必须设置 `ConditionFirstBoot=systemd-update-done.service` ， 以确保在 `.updated` 文件被更新之前启动完毕。 参见 [systemd-update-done.service(8)](http://www.jinbuguo.com/systemd/systemd-update-done.service.html#) 手册。`ConditionFirstBoot=` 可设为 `yes` 或 `no` 。 用于检测 `/etc` 目录是否处于未初始化的原始状态(重点是 `/etc/machine-id` 文件是否存在)。 此选项可用于系统出厂后(或者恢复出厂设置之后)， 首次开机时执行必要的初始化操作。`ConditionPathExists=` 检测 指定的路径 是否存在， 必须使用绝对路径。 可以在路径前面 加上感叹号(!)前缀 表示逻辑反转。`ConditionPathExistsGlob=` 与 `ConditionPathExists=` 类似， 唯一的不同是支持 shell 通配符。`ConditionPathIsDirectory=` 检测指定的路径是否存在并且是一个目录，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀表示逻辑反转。`ConditionPathIsSymbolicLink=` 检测指定的路径是否存在并且是一个软连接，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀 表示逻辑反转。`ConditionPathIsMountPoint=` 检测指定的路径是否存在并且是一个挂载点，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀表示逻辑反转。`ConditionPathIsReadWrite=` 检测指定的路径是否存在并且可读写(rw)，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀 表示逻辑反转。`ConditionDirectoryNotEmpty=` 检测指定的路径是否存在并且是一个非空的目录，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀 表示逻辑反转。`ConditionFileNotEmpty=` 检测指定的路径是否存在并且是一个非空的普通文件，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀 表示逻辑反转。`ConditionFileIsExecutable=` 检测指定的路径是否存在并且是一个可执行文件，必须使用绝对路径。 可以在路径前面加上感叹号(!)前缀 表示逻辑反转。`ConditionUser=` 检测 systemd 是否以给定的用户身份运行。 参数可以是数字形式的 "`UID`" 、 或者字符串形式的UNIX用户名、 或者特殊值 "`@system`"(表示属于系统用户范围内) 。 此选项对于系统服务无效， 因为管理系统服务的 systemd 进程 总是以 root 用户身份运行。`ConditionGroup=` 检测 systemd 是否以给定的用户组身份运行。 参数可以是数字形式的 "`GID`" 或者字符串形式的UNIX组名。 注意：(1)这里所说的"组"可以是"主组"(Primary Group)、"有效组"(Effective Group)、"辅助组"(Auxiliary Group)； (2)此选项不存在特殊值 "`@system`"`ConditionControlGroupController=` 检测给定的一组 cgroup 控制器(例如 `cpu`)是否全部可用。 通过例如 `cgroup_disable=controller` 这样的内核命令行可以禁用名为"controller"的 cgroup 控制器。 列表中的多个 cgroup 控制器之间可以使用空格分隔。 不能识别的 cgroup 控制器将被忽略。 能够识别的全部 cgroup 控制器如下： `cpu`, `cpuacct`, `io`, `blkio`, `memory`, `devices`, `pids`如果在条件之前加上管道符(|)，那么这个条件就是"触发条件"， 其含义是只要满足一个触发条件，该单元就会被启动； 如果在条件之前没有管道符(|)，那么这个条件就是"普通条件"， 其含义是必须满足全部普通条件，该单元才会被启动。 如果在某个单元文件内， 同时存在"触发条件"与"普通条件"，那么必须满足全部普通条件， 并且至少满足一个触发条件，该单元才会被启动。 如果需要对某个条件同时使用"|"与"!"， 那么"|"必须位于"!"之前。 除 `ConditionPathIsSymbolicLink=` 之外， 其他路径检测选项都会追踪软连接。 如果将上述某个检测选项设为空字符串， 那么表示重置该选项先前的所有设置， 也就是清空该选项先前的设置。

- `AssertArchitecture=`, `AssertVirtualization=`, `AssertHost=`, `AssertKernelCommandLine=`, `AssertKernelVersion=`, `AssertSecurity=`, `AssertCapability=`, `AssertACPower=`, `AssertNeedsUpdate=`, `AssertFirstBoot=`, `AssertPathExists=`, `AssertPathExistsGlob=`, `AssertPathIsDirectory=`, `AssertPathIsSymbolicLink=`, `AssertPathIsMountPoint=`, `AssertPathIsReadWrite=`, `AssertDirectoryNotEmpty=`, `AssertFileNotEmpty=`, `AssertFileIsExecutable=`, `AssertUser=`, `AssertGroup=`, `AssertControlGroupController=`

  与前一组 `ConditionArchitecture=`, `ConditionVirtualization=`, … 测试选项类似，这一组选项用于在单元启动之前， 首先进行相应的断言检查。不同之处在于，任意一个断言的失败， 都会导致跳过该单元的启动并将失败的断言突出记录在日志中。 注意，断言失败并不导致该单元进入失败("`failed`")状态(实际上，该单元的状态不会发生任何变化)， 它仅影响该单元的启动任务队列。 如果用户希望清晰的看到某些单元因为未能满足特定的条件而导致没有正常启动， 那么可以使用断言表达式。注意，无论是前一组条件表达式、还是这一组断言表达式，都不会改变单元的状态。 因为这两组表达式都是在启动任务队列开始执行时进行检查(也就是，位于依赖任务队列之后、该单元自身启动任务队列之前)， 所以，条件表达式和断言表达式 都不适合用于对单元的依赖条件进行检查。

- `SourcePath=`

  指定 生成此单元时所参考的配置文件。 仅用于单元生成器 标识此单元生成自何处。 普通的单元 不应该使用它。



## 单元属性的正反对应

那些与其他单元关联的属性 通常同时显示(**systemctl show**)在两个关联单元的属性中。 多数情况下， 属性的名称就是单元配置选项的名称，但并不总是如此。 下表展示了存在依赖关系的两个单元的属性是如何显示的， 同时也展示了"源"单元的属性与"目标"单元的属性之间的对应关系。



**表 3. "正向"与"反向"单元属性**

| "正向"属性              | "反向"属性              | 用于何处                     |
| ----------------------- | ----------------------- | ---------------------------- |
| `Before=`               | `After=`                | [Unit] 小节                  |
| `After=`                | `Before=`               |                              |
| `Requires=`             | `RequiredBy=`           | [Unit] 小节； [Install] 小节 |
| `Wants=`                | `WantedBy=`             | [Unit] 小节； [Install] 小节 |
| `PartOf=`               | `ConsistsOf=`           | [Unit] 小节； 自动生成       |
| `BindsTo=`              | `BoundBy=`              | [Unit] 小节； 自动生成       |
| `Requisite=`            | `RequisiteOf=`          | [Unit] 小节； 自动生成       |
| `Triggers=`             | `TriggeredBy=`          | 自动生成(参见下文的解释)     |
| `Conflicts=`            | `ConflictedBy=`         | [Unit] 小节； 自动生成       |
| `PropagatesReloadTo=`   | `ReloadPropagatedFrom=` | [Unit] 小节                  |
| `ReloadPropagatedFrom=` | `PropagatesReloadTo=`   |                              |
| `Following=`            | n/a                     | 自动生成                     |



`WantedBy=` 与 `RequiredBy=` 位于 [Install] 小节，仅用于在 `.wants/` 与 `.requires/` 目录中创建软连接， 不能直接用作单元属性。

`ConsistsOf=`, `BoundBy=`, `RequisiteOf=`, `ConflictedBy=` 只能由对应的"正向"属性自动隐式创建，而不能直接在单元文件中设置。

`Triggers=` 只能隐式的创建于 socket, path, automount 单元之中。 默认触发对应的同名单元，但是可以通过 `Sockets=`, `Service=`, `Unit=` 选项进行改写。详见 [systemd.service(5)](http://www.jinbuguo.com/systemd/systemd.service.html#), [systemd.socket(5)](http://www.jinbuguo.com/systemd/systemd.socket.html#), [systemd.path(5)](http://www.jinbuguo.com/systemd/systemd.path.html#), [systemd.automount(5)](http://www.jinbuguo.com/systemd/systemd.automount.html#) 手册。`TriggeredBy=` 只能隐式的创建于被触发的单元之中。

`Following=` 用于汇聚设备别名， 并指向用于跟踪设备状态的"主"设备单元，通常对应到一个 sysfs 文件系统路径。 它并不会显示在"目标"单元中。



## [Install] 小节选项

"`[Install]`" 小节包含单元的启用信息。 事实上，[systemd(1)](http://www.jinbuguo.com/systemd/systemd.html#) 在运行时并不使用此小节。 只有 [systemctl(1)](http://www.jinbuguo.com/systemd/systemctl.html#) 的 **enable** 与 **disable** 命令在启用/停用单元时才会使用此小节。 [译者注]"启用"一个单元多数时候在效果上相当于将这个单元设为"开机时自动启动"或"插入某个硬件时自动启动"； "停用"一个单元多数时候在效果上相当于撤销该单元的"开机时自动启动"或"插入某个硬件时自动启动"。

- `Alias=`

  启用时使用的别名，可以设为一个空格分隔的别名列表。 每个别名的后缀(也就是单元类型)都必须与该单元自身的后缀相同。 如果多次使用此选项，那么每个选项所设置的别名都会被添加到别名列表中。 在启用此单元时，**systemctl enable** 命令将会为每个别名创建一个指向该单元文件的软连接。 注意，因为 mount, slice, swap, automount 单元不支持别名， 所以不要在这些类型的单元中使用此选项。

- `WantedBy=`, `RequiredBy=`

  接受一个空格分隔的单元列表， 表示在使用 **systemctl enable** 启用此单元时， 将会在每个列表单元的 `.wants/` 或 `.requires/` 目录中创建一个指向该单元文件的软连接。 这相当于为每个列表中的单元文件添加了 `Wants=此单元` 或 `Requires=此单元` 选项。 这样当列表中的任意一个单元启动时，该单元都会被启动。 有关 `Wants=` 与 `Requires=` 的详细说明， 参见前面 [Unit] 小节的说明。 如果多次使用此选项， 那么每个选项的单元列表都会合并在一起。在普通的 `bar.service` 单元内设置 **WantedBy=foo.service** 选项 与设置 **Alias=foo.service.wants/bar.service** 选项基本上是等价的。 但是对于模板单元来说，情况则有所不同。 虽然必须使用实例名称调用 **systemctl enable** 命令， 但是实际上添加到 `.wants/` 或 `.requires/` 目录中的软连接， 指向的却是模板单元(因为并不存在真正的单元实例文件)。 假设 `getty@.service` 文件中存在 **WantedBy=getty.target** 选项，那么 **systemctl enable getty@tty2.service** 命令将会创建一个 `getty.target.wants/getty@tty2.service` 软连接(指向 `getty@.service`)

- `Also=`

  设置此单元的附属单元， 可以设为一个空格分隔的单元列表。 表示当使用 **systemctl enable** 启用 或 **systemctl disable** 停用 此单元时， 也同时自动的启用或停用附属单元。如果多次使用此选项， 那么每个选项所设置的附属单元列表 都会合并在一起。

- `DefaultInstance=`

  仅对模板单元有意义， 用于指定默认的实例名称。 如果启用此单元时没有指定实例名称， 那么 将使用这里设置的名称。

在 [Install] 小节的选项中，可以使用如下替换符： %n, %N, %p, %i, %j, %g, %G, %U, %u, %m, %H, %b, %v 。 每个符号的具体含义详见下一小节。



## 替换符

在许多选项中都可以使用一些替换符(不只是 [Install] 小节中的选项)， 以引用一些运行时才能确定的值， 从而可以写出更通用的单元文件。 替换符必须是已知的、并且是可以解析的，这样设置才能生效。 当前可识别的所有替换符及其解释如下：



**表 4. 可以用在单元文件中的替换符**

| 替换符 | 含义                                                         |
| :----- | ------------------------------------------------------------ |
| "`%b`" | 系统的"Boot ID"字符串。参见 `random(4)` 手册                 |
| "`%C`" | 缓存根目录。对于系统实例来说是 `/var/cache` ；对于用户实例来说是 "`$XDG_CACHE_HOME`" |
| "`%E`" | 配置根目录。对于系统实例来说是 `/etc` ；对于用户实例来说是 "`$XDG_CONFIG_HOME`" |
| "`%f`" | 原始单元文件名称(不含路径，且遵守前文描述的已转义绝对文件系统路径的还原规则)。对于实例化的单元，就是带有 `/` 前缀的原始实例名；对于其他单元，就是带有 `/` 前缀的原始前缀名。 |
| "`%h`" | 用户的家目录。运行 systemd 实例的用户的家目录，对于系统实例则是 "`/root`" |
| "`%H`" | 系统的主机名(hostname)                                       |
| "`%i`" | 已转义的实例名称。对于实例化单元，就是 "`@`" 和后缀之间的部分。对于非实例化单元则为空。 |
| "`%I`" | 原始实例名称。对于实例化单元，就是 "`@`" 和后缀之间的部分(已还原的)。对于非实例化单元则为空。 |
| "`%j`" | 已转义的前缀名最后一部分。也就是前缀名中最后一个 "`-`" 之后的部分。如果没有 "`-`" 那么与 "`%p`" 相同。 |
| "`%J`" | 原始前缀名最后一部分。也就是前缀名中最后一个 "`-`" 之后的部分(已还原的)。如果没有 "`-`" 那么与 "`%p`" 相同。 |
| "`%L`" | 日志根目录。对于系统实例来说是 `/var/log` ；对于用户实例来说是 "`$XDG_CONFIG_HOME`"`/log` |
| "`%m`" | 系统的"Machine ID"字符串。参见 `machine-id(5)`手册           |
| "`%n`" | 带类型后缀的完整单元名称                                     |
| "`%N`" | 无类型后缀的完整单元名称                                     |
| "`%p`" | 已转义的前缀名称。对于实例化单元来说，就是单元名称里第一个 "`@`" 之前的字符串。对于非实例化单元来说，等价于 "`%N`" |
| "`%P`" | 原始前缀名称。对于实例化单元来说，就是单元名称里第一个 "`@`" 之前的字符串(已还原的)。对于非实例化单元来说，等价于 "`%N`" |
| "`%s`" | 用户的shell。运行 systemd 实例的用户的shell，对于系统实例则是 "`/bin/sh`" |
| "`%S`" | 状态根目录。对于系统实例来说是 `/var/lib` ；对于用户实例来说是 "`$XDG_CONFIG_HOME`" |
| "`%t`" | 运行时根目录。对于系统实例来说是 `/run` ；对于用户实例来说是 "`$XDG_RUNTIME_DIR`" |
| "`%T`" | 临时文件目录。也就是 `/tmp` 或 "`$TMPDIR`", "`$TEMP`", "`$TMP`" 之一(若已设置) |
| "`%g`" | 运行 systemd 用户实例的组名称。对于 systemd 系统实例来说，则是 "`root`" |
| "`%G`" | 运行 systemd 用户实例的组GID。对于 systemd 系统实例来说，则是 "`0`" |
| "`%u`" | 运行 systemd 用户实例的用户名称。对于 systemd 系统实例来说，则是 "`root`" |
| "`%U`" | 运行 systemd 用户实例的用户UID。对于 systemd 系统实例来说，则是 "`0`" |
| "`%v`" | 内核版本(`uname -r` 的输出)                                  |
| "`%V`" | 存放大体积临时文件以及持久临时文件的目录。也就是 `/var/tmp` 或 "`$TMPDIR`", "`$TEMP`", "`$TMP`" 之一(若已设置) |
| "`%%`" | 百分号自身(%)。使用 "`%%`" 表示一个真正的 "`%`" 字符。       |





## 例子



**例 1. 允许单元被启用**

下面这个 `foo.service` 单元中的 `[Install]` 小节表明该单元可以通过 **systemctl enable** 命令启用。

```
[Unit]
Description=Foo

[Service]
ExecStart=/usr/sbin/foo-daemon

[Install]
WantedBy=multi-user.target
```

执行 **systemctl enable** 启用命令之后， 将会建立一个指向该单元文件的软链接 `/etc/systemd/system/multi-user.target.wants/foo.service` ， 表示将 `foo.service` 包含到 `multi-user.target` 目标中， 这样，当启动 `multi-user.target` 目标时， 将会自动起动 `foo.service` 服务。 同时，**systemctl disable** 命令 将会删除这个软连接。





**例 2. 覆盖软件包的默认设置**

以例如 `foo.type` 这样的系统单元为例， 有两种修改单元文件的方法： (1)将单元文件从 `/usr/lib/systemd/system` 目录 复制到 `/etc/systemd/system` 目录中， 然后直接修改复制后的副本。 (2)创建 `/etc/systemd/system/foo.type.d/` 目录， 并在其中创建一些 `*`name`*.conf` 文件， 然后 仅针对性的修改某些个别选项。

第一种方法的优点是易于修改整个单元， 因为原有的单元文件会被完全忽略。 但此种方法的缺点是， 当原有的单元文件被更新时， 变更不能在修改后的副本上自动体现出来。

第二种方法的优点是仅需修改个别选项， 并且原有单元文件的更新能够自动生效。 因为 `.conf` 文件只会按照其文件名的字典顺序，被依次追加到原有单元文件的尾部。 但此种方法的缺点是原有单元文件的更新 有可能导致与 `.conf` 文件中的设置不兼容。

这同样适用于 systemd 用户实例， 只是用户单元文件的文件系统位置不同而已。 参见前文的"单元目录"小节。

下面是一个实例，假定原有的单元文件 `/usr/lib/systemd/system/httpd.service` 包含以下内容：

```
[Unit]
Description=Some HTTP server
After=remote-fs.target sqldb.service
Requires=sqldb.service
AssertPathExists=/srv/webserver

[Service]
Type=notify
ExecStart=/usr/sbin/some-fancy-httpd-server
Nice=5

[Install]
WantedBy=multi-user.target
```

假定系统管理员想要修改几个设置： 

* (1) 本地并不存在 `/srv/webserver` 目录，需要修改为 `/srv/www` 目录。 

* (2) 让此服务依赖于本地已经存在的 `memcached.service` 服务(`Requires=`)， 且在其后启动(`After=`)。 

* (3) 为了加固此服务， 添加一个 `PrivateTmp=` 设置(参见 `systemd.exec(5)` 手册)。 (4)将此服务的进程谦让值重置为默认值"0"。

第一种方法，将原有的单元文件复制到 `/etc/systemd/system/httpd.service` 并做相应的修改：

```
[Unit]
Description=Some HTTP server
After=remote-fs.target sqldb.service memcached.service
Requires=sqldb.service memcached.service
AssertPathExists=/srv/www

[Service]
Type=notify
ExecStart=/usr/sbin/some-fancy-httpd-server
Nice=0
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

第二种方法， 创建配置片段 `/etc/systemd/system/httpd.service.d/local.conf` 并在其中填入如下内容：

```
[Unit]
After=memcached.service
Requires=memcached.service
# 重置所有断言，接着重新加入想要的条件
AssertPathExists=
AssertPathExists=/srv/www

[Service]
Nice=0
PrivateTmp=yes
```

注意， 对于单元配置片段， 如果想要移除列表选项(例如 `AssertPathExists=` 或 `ExecStart=`)中的某些项， 那么必须首先清空列表(设为空)，然后才能添加(剔除掉某些项之后)剩余的列表项。 注意，因为依赖关系列表(`After=` 之类)不能被重置为空，所以： (1)在配置片段(`.conf`)中只能添加依赖关系； (2)如果你想移除现有的依赖关系，并重新设定， 那么只能用第一种方法(先复制，然后直接修改复制后的副本)。
