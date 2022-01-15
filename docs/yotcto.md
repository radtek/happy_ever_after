# yocto

## yocto基础知识介绍

* Yocto: Yocto是这个开源项目的名称，该项目旨在帮助我们自定义Linux系统
* Poky: Poky有两个含义:
  * 用来构建Linux的**构建系统**。此时，Poky仅仅是一个概念而非实体：它包含了 **BitBake工具**、**编译工具链**、**BSP**、**诸多程序包或层**。可以认为Poky即是Yocto的本质；
  * 使用Poky系统得到的默认参考 Linux 发行版也叫Poky(当然，我们可以对此发行版随意命名)。
* Layers：即各种`meta-xxx`目录，将Metadata按层进行分类，有助于项目的维护
* Metadata：元数据集; 所谓元数据集就是**发行版内各基本元素的描述与来源**
  * Recipes：`.bb`/`.bbappend`文件(配方文件)，描述了**从哪获取软件源码，如何配置，如何编译**。`bbappend`和`bb`的区别主要在于: `bbappend`是基于`bb`的，功能是对相应的bb文件作补充和覆盖，有点类似于“重写”的概念
  * Configuration：`.conf`文件，即配置文件，我们可以用它来改变构建方式
  * Class:`.bbclass`文件
* Bitbake：一个任务执行引擎，**用来解析并执行Metadata**
* Output：即各种输出image

总结：假如用烹饪一桌酒席来形容构建发行版，则`Yocto`就是饭店名，`Poky`就是厨房(以及提供作为参考的菜的搭配套餐)，`Layers`就是菜谱的分类(如川菜谱、粤菜谱)，`Metadata`就是烹饪资源(`.bb`/`.bbappend`表示配方/配方上的贴士，`.conf`表示厨房里的管事的小组长)，`Bitbake`就是厨师，`Output`就是得到的一桌酒席.



### `Bitbake`

Bitbake是yocto的核心组件，负责解析metadata，生成一系列任务，并执行这些任务。

BitBake是一种任务调度程序和执行引擎，可解析指令(即食谱)和配置数据。**在解析阶段之后，BitBake创建一个依赖树来排序编译，安排所包含代码的编译，最后执行指定的自定义Linux镜像(发行版)的构建**。

BitBake类似于make工具。在构建过程中，构建系统跟踪依赖关系并执行包的本机或交叉编译。作为交叉构建设置的第一步，框架尝试创建适合目标平台的交叉编译器工具链(即Extensible SDK)。

* 可使用以下命令查看bitbake所支持的所有选项。

```sh
$ bitbake --help
```

最常见的用法是 `bitbake <packagename>`

packagename指的是你想编译的软件包的名称，即target，target通常是一个.bb文件的文件名(不带后缀)。因此你可以使用以下命令执行`busybox_1.18.4.bb`：

```sh
$ bitbake busybox
```

* 如果存在多个版本的bb文件，yocto将根据配置文件中的配置选择版本。如无指定，将选择最新版本编译。

* 其他比较常用的选项包括`-c`，`-g`等
  * `-c`选项是选择执行一项任务的某一阶段。
  * `-g`选项生成任务的依赖关系。

```sh
$ bitbake busybox –c compile
$ bitbake -g busybox
```

### Metadata

元数据集，所谓元数据集就是**发行版内各基本元素的描述与来源**

元数据松散地分组到配置文件或包配方中。



* 配方(recipes)是BitBake用来**设置变量或定义其他构建时任务的不可执行元数据的集合**
* 配方包含诸如**配方说明**、**配方版本**、**软件包许可证**和**上游源存储库**等字段
* 配方还可能指示构建过程使用`autotools`、`make`、`distutils`或任何其他构建过程，在这种情况下，基本功能可以由它从`./meta/classes`中的OE-Core层的类定义继承的类来定义。
* 在配方中，还可以**定义其他任务**以及**任务先决条件**。
* bitBake的配方语法还支持`_prepend`和`_append`运算符，作为扩展任务功能的方法。这些运算符将代码注入任务的开始或结束。
* 以文件扩展名.bb表示的BitBake Recipes是最基本的元数据文件。**通常，一个recipe包含一个软件的信息**。这些信息包括**软件包的描述信息**、**配方的版本**、**依赖关系**、**源码获取路径**，**如何打补丁**，**如何配置**、**编译以及如何安装**、**打包该软件**。

* `*.conf`文件用于全局配置，而`*.bb文件`的配置只影响其对应的软件包。
* `*.inc`和`*.bbclass`文件中的配置作用范围则取决于他们在什么文件中被包含和继承。
* 语法上`*.inc`、`*.bbclass`、`*.bbappend`都可以看做是`.bb`文件。
  * `*.inc`类似于c中的头文件
  * `.bbclass`定义一些公共的函数等
  * `.bbappend`是对`.bb`文件的内容的追加和重载。
  * 要编译一个包，必须有对应的`.bb`文件，`.inc`、`.bbclass`、`.bbappend`不是必须的。没有`.bb`文件，即使有对应的`.bbappend`也是无效的，编译会报错。

* 附加文件是具有`.bbappend`文件扩展名的文件，扩展或覆盖现有配方文件中的信息。
  * BitBake期望每个附加文件都有相应的配方文件。
  * 附加文件和相应的配方文件必须使用相同的根文件名。文件名只能在所使用的文件类型后缀上有所不同(例如`acl_0.0.bb`和`acl_0.0.bbappend`)。附加文件中的信息扩展或覆盖底层的，类似名称的配方文件中的信息。
  * 在命名附加文件时，可以使用通配符(`％`)来匹配配方名称。例如，`busybox_1.21％.bbappend`将匹配任何`busybox_1.21.x.bb`(`busybox_1.21.1.bb`、`busybox_1.21.3.bb`、...)版本的配方。如果busybox配方更新为`busybox_1.3.0.bb`，则附加名称不匹配。但是，如果将追加文件命名为`busybox_1.％.bbappend`，那么可以匹配`busybox_1.3.0.bb`。

### Classes

类文件(.bbclass)是一些公用的模板库，包含有助于在元数据文件之间共享的信息。例如`autotool`，在bb文件中使用`inherit`命令继承。
bbclass文件提供了一些常见的模板和函数。Yocto提供的所有bbclass放在`poky-dora-10.0.0/meta/classes`目录(bb文件中每个任务的默认函数原型都是在这里定义的)下，供开发者调用，也可开发自定义的bbclass，放在自定义layer的`classes`目录下。

BitBake源码当前带有一个名为base.bbclass的类元数据文件。base.bbclass类文件是特殊的，因为它总是自动包含在所有的配方和类中。这个类包含了标准的基本任务的定义，例如**抓取，解包，配置(默认为空)，编译(运行任何Makefile)，安装(默认为空)和打包(默认为空)**。这些任务通常被项目开发过程中添加的其他类所覆盖或扩展。

### Configuration

包含 `machine.conf`、`layer.conf`、`local.conf`、`distro.conf`、`bblayers.conf`.

* `machine.conf`: 定义了**特定架构的信息**，如架构、内核版本等。
* `layer.conf`: 定义了**特定layer层信息**，如bb文件的位置，layer的优先级等。
* `distro.conf`: 定义了**特定发布物的信息**、发布者、发布版本、软件版本等，如版本号V1R1C01就是放在这里。

以上三个文件均放在特定的layer文件夹中。

* `local.conf`: 定义了特定工程的属性, 该配置文件每个工程包含一个。该配置文件指定了本工程的machine、distro和工具链等。
* `bblayers.conf`: 指定bb文件和layer的位置
* `local.conf`和`bblayers.conf`由configure脚本生成。开发者也可手动修改。


**如何理解Yocto的配置方法？**

这要从发行版的定制流程说起。我们的目的很简单，是要**得到uboot、kernel、rootfs这三个image**；Yocto的目的也很简单，它要**经过一级一级配置，逐步缩小配方，直至得到uboot、kernel、rootfs这三个image**。每一级需要哪些配方，由该级对应的配置文件（conf/bb）决定。越上级的配置是越笼统的，越下级的配置越细致。如果下级的配置项相对于上级有补充或者冲突，则以下级的内容为准，可以认为下级会对上级进行“重写”。这其实有点类似交通法规。

对于整个发行版构建，虽然每一级的配方由（conf/bb）决定，但是每一级路线和方向的选择，是由我们最终bitbake的对象决定的，比如我们最终`bitbake apple-image`，我们想要获得rootfs.img，那么：

* 第一步Poky就会从`local.conf`开始，一路向下，一级一级配置，直到配置到和rootfs有关的那一堆bb，最终形成完整完全的配方(`local.conf -> bblayer.conf -> layers/meta-xxx/conf/layer.conf`)
* 第二步获取配方需要的资源，比如各种软件包，比如kernel的源码
* 第三步把所有的资源编译出我们需要的镜像

### bb文件常用配置项

| 配置项 | 含义 | 必选项 |
| ------ | :---- | ------ |
| `DESCRIPTION` | 描述 | Y |
| `SECTION` | 类别 | Y |
| `LICENSE` | 软件的license | Y |
| `LIC_FILES_CHKSUM` | License文件的位置和MD5(默认相对${S}) | Y |
| `inherit` | 继承bbclass | N |
| `require` | 包含的文件，和Makfile中的include类似 | N |
| `PROVIDES` | 该软件包提供的开发组件，和DEPENDS对应 | N |
| `RPROVIDES` | 该软件提供的运行时组件，和RDEPENDS对应 | N |
| `PACKAGES` | 最后打包生成的rpm包的名称，例如`PACKAGES =+ "${PN}-utils"`、`PACKAGES = "${PN} ${PN}-server"`、`PACKAGES_prepend = "lsm"`；如果不指定，则按yocto默认方式分包。 | N |
| `FILES_xxx` | xxx包（上面PACKAGES中的rpm包名）中要包含哪些文件(文件路径是相对于${D}的根目录)。例如 `FILES_${PN} = "${libdir}/*.so"`、`FILES_${PN}-sever = "/*"`、`FILES_lsm += " ${base_libdir}/*.la"` | Y |
| `SRC_URI` | 源码及所需文件的路径，yocto会自动识别里面的`.patch`文件，并根据所列的顺序打补丁。另外。`File://`可加绝对路径和相对路径。相对路径指向和bb文件同层的目录下的文件夹，该文件夹以files或者以“**包名-版本号**”命名。Yocto将优先匹配以“**包名-版本号**”命名的文件夹。 | Y |
| `DEPENDS` | 开发依赖的包，这里指定的软件包会在当前包configure阶段前完成编译和populate_sysroot阶段。`DEPENDS`中生成的开发库、命令将拷贝到sysroot中。 | N |
| `RDEPENDS` | 运行时依赖的包。`RDEPENDS`中生成的开发库、命令将不会拷贝到sysroot中。 | N |
| `PR` | Package Release Version | Y |
| `COMPATIBLE_MACHINE` | 支持的平台（machine） | N |
| `EXTRA_OECONF` | configure选项，当执行执行oe_runconf，等价于执行`configure ${EXTRA_OECONF}` | N |
| `EXTRA_OEMAKE` | Make选项，当执行oe_runmake时，等价于执行`make ${EXTRA_OEMAKE}` | N |


常用预定义变量: 

| 变量 | 含义 |
| --- | :--- |
| `COREBASE` | poke顶层目录路径（此处为yocto文件夹路径） |
| `TOPDIR` | 编译目录根目录 |
| `TMPDIR` | 工程下的tmp目录`${TOPDIR}/tmp*/` |
| `WORKDIR` | 每个模块的工作目录 |
| `S` | 源码解压路径；默认为`${WORKDIR}/${PN}-${PV}`,如果压缩包解压路径xxx不是`${PN}-${PV}`，则需要自行指定`S=${WORKDIR}/xxx` |
| `D` | 软件包的安装目录，即WORKDIR下的image目录（即`make install`的路径） |
| `B` | 每个bb实际编译目录，B可能等于${S}，默认B是`${WORKDIR}/build/` |
| `PN` | Package name，包含前缀或后缀。例如`bash-native`，`lib32-bash` |
| `PV` | Package version |
| `P` | `${PN}-${PV}` |
| `RECIPE_SYSROOT` | `${WORKSPACE}/recipe-sysroot` |
| `BPN` | Package name，已移除-cross –native lib32-等后缀或前缀。例如`binutils-cross-canadian.inc:BPN = "binutils"`；`eglibc-locale.inc:BPN = "eglibc"`；`tar-replacement-native_1.26.bb:BPN = "tar"` |
| `BP` | `${BPN}-${PV}` |
