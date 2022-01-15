```sh
shell> free -m
              total        used        free      shared  buff/cache   available
Mem:            862         157         483           6         222         568
Swap:          1023           0        1023
```

## `free` 

**free** displays the total amount of free and used physical and swap memory in the system, as well as the buffers and caches used by the kernel. The information is gathered by parsing `/proc/meminfo`.  The  displayed columns are:

* **`total`**

    Total installed memory (`MemTotal` and `SwapTotal` in `/proc/meminfo`)

* **`used`**

    Used memory (calculated as `total - free - buffers - cache`)

* **`free`**

    Unused memory (`MemFree` and `SwapFree` in /proc/meminfo)

* **`shared`** 

    Memory used (mostly) by tmpfs (`Shmem` in `/proc/meminfo`, available on kernels 2.6.32, displayed as `zero` if not available)

* **`buffers`**

    Memory used by **kernel buffers** (`Buffers` in /proc/meminfo)

* **`cache`**

    Memory used by the **page cache** and **slabs** (`Cached` and `SReclaimable` in /proc/meminfo)

* **`buff/cache`**

    Sum of `buffers` and `cache`

* **`available`**

    Estimation of **how much memory is available for starting new applications, without swapping**. Unlike the data provided  by the cache or free fields, this field takes into account page cache and also that not all reclaimable memory slabs will be reclaimed due to items being in use  (`MemAvailable` in `/proc/meminfo`, available on kernels 3.14, emulated on kernels 2.6.27+, otherwise the same as free)



## 关于操作系统的文件系统

* 概念
    * 扇区：磁盘的最小存储单位；
    * 磁盘块：文件系统读写数据的最小单位；
    * 页：内存的最小存储单位；
  
* 联系
    * 一个磁盘块由连续几个 `2^n` 扇区组成；
    * 页的大小为磁盘块大小的 `2^n` 倍；

* 查看
    * 页大小查看： `getconf PAGE_SIZE`，常见为`4K`；
    * 磁盘块大小查看：`stat /boot/|grep "IO Block"`，常见为`4K`；
    * 扇区大小查看：`fdisk -l`，常见为 `512Byte`；

**扇区是对硬盘而言，块是对文件系统而言**: 

* 从应用程序包括用户界面的角度来看，存取信息的最小单位是**Byte**(字节）；
* 从磁盘的物理结构来看存取信息的最小单位是**扇区**，一个扇区是512字节；
* 从操作系统对硬盘的存取管理来看，存取信息的最小单位是**簇**，簇是一个逻辑概念，一个簇可以是2、4、8、16、32或64个连续的扇区。一个簇只能被一个文件占用，哪怕是只有1个字节的文件，在磁盘上存储时也要占用一个簇，这个簇里剩下的扇区是无用的。例如用NTFS文件系统格式化的时候默认是8个扇区组成一个簇，即4096字节。所以你如果保存了一个只有1字节的文件(例如字母N），它在磁盘上实际也要占用4096字节(4K），所以 **"簇"也可以理解为操作系统存取信息的最小单位**。





## 关于 `Page Cache` 和 `Buffer Cache`





Storing Blocks in the Page Cache: 

> In old versions of the Linux kernel, there were two different main disk caches: **the page cache**, which stored whole pages of disk data resulting from accesses to **the contents of the disk files**, and **the buffer cache**, which was used to keep in memory **the contents of the blocks** accessed by the VFS to manage the disk-based filesystem. Starting from stable version 2.4.10, the buffer cache does not really exist anymore. In fact, for reasons of efficiency, block buffers are no longer allocated individually; instead, they are stored in dedicated pages called "**buffer pages**", which are kept in the page cache. Formally, a buffer page is a page of data associated with additional descriptors called "buffer heads", whose main purpose is to quickly locate the disk address of each individual block in the page. In fact, the chunks of data stored in a page belonging to the page cache are not necessarily adjacent on disk. 


**`Page Cache`** 缓存 **文件内容** 以 **优化文件 I/O**，**`Buffer Cache`** 缓存 **磁盘blocks** 以 **优化block I/O**

* Linux kernel 2.4以前，这两个cache的使用是有明显区别的：**文件的内容在Page Cache中缓冲**，**(管理基于磁盘的文件系统的VFS所访问的)blocks在Buffer Cache中缓冲**。鉴于大多数的文件都是由基于磁盘的文件系统(disk-base filesystem)来存储和表示(represented）的，这样数据就被CACHE了两次，每个cache(Page Cache & Buffer Cache）中各表示一次。 这样易于实现，但存在明显的槽点: **CACHE重复** 和 **低效**

* Linux kernel 2.4开始, 两个cache中的内容统一:
    * (1) **buffer cache不再真正的存在**: `buffer cache` 不再独立分配，而是在 `page cache` 中用专门的 `buffer page` 来替代 `buffer page`
    * (2) 在形式上就是**缓冲区描述符**，称为 **`buffer_head`**
    * (3) 如果缓冲的数据既有文件表示(`file representation`）又有块表示(`block representation`）, 大多数数据都是这样的, 那么 `buffer cache` 就简单的指向` page cache`, 这样就仅有一份数据被缓冲在内存中。`page cache` 可以想象为：**它将文件数据从磁盘中缓存, 以便后续I/O操作更快**. 

**注:**
> *1*. 内存页中有一种专门用途的页面叫 "**缓冲区页**", 专门用来放 **块缓冲区**(包含两部分, **缓冲区首部**(用数据结构 `buffer_head` 表示）及真正的**缓冲区内容**(即所存储的数据)  
> *2*. 由于内核处理块时需要一些信息，如块属于哪个设备与块对应于哪个缓冲区。所以每个缓冲区都有一个缓冲区描述符，称为`buffer_head`, 它包含了内核操作缓冲区所需要的全部信息。通过`buffer_head` 可以快速的**定位page中独立的blocak在磁盘上的逻辑地址**  
> *3*. 文件在内存中由**file结构体**表示, 磁盘块在内存中是由**缓冲区**来进行表示的, **每个缓冲区与一个块对应，它相当于磁盘块在内存中的表示**。

* `Buffer cache`还依旧被保留，**因为内核还要以block为单位(而不是page）来进行block I/O操作**
    * 大多数情况下, block就已经代表了文件数据，所以大多数的 `buffer cache` 由 `page cache` 来代替了; 
    * 少量block数据不是文件内容本身, 例如文件系统的**元数据**(`metadata`）和**裸设备(`raw`) block I/O** , 这些还是在 `buffer cache` 中缓冲的。 

注释：由于内核处理块时需要一些信息(比如将CACHE中的脏数据写入到磁盘中，而数据是被文件系统组织存储在block中的），如块属于哪个设备与块对应于哪个缓冲区。所以每个缓冲区都有一个缓冲区描述符，称为buffer_head。它包含了内核操作缓冲区所需要的全部信息。通过buffer_head 可以快速的定位page中独立的block在磁盘上的逻辑地址。 