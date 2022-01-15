## 一、CPU节能概念

    随着CPU的发展，Intel出现了EIST技术，它可以动态的调整CPU的频率。当CPU使用率地下或者接近0时候,能降低CPU频率并且降压，从而降低功耗和发热。当检测到CPU使用率增高，它会马上回到原始工作频率，但是你必须考虑CPU被唤醒的时间，并且确保它会再次100％运行。这一系列的过程通常被称为“C-states”或“C-modes”,它是从C0开始的。

    随着C-states的不断增加，CPU睡眠模式就更深，即更多的电路和信号被关闭，并且CPU将需要更多时间返回到C0模式，即唤醒。

    对于每个模式也有不同的名称与不同功耗的子模式，从而唤醒时间级别等。

    而在一些case中，CPU节能会带一些不稳定的因素，如unstable issue或performance issue，所以我们可以通过系统层面来disable CPU节能。

## 二、常见的几种`C-states`

* `C0`: 工作状态，CPU完全运行。
* `C1`: 停止状态，主CPU停止内部时钟经由软件；总线接口单元和APIC保持全速运行。
* `C3`: 深度睡眠，止所有CPU内部和外部时钟。
* `C6`: 深度功率下降, 将CPU内部电压降低到任何值，包括0V。

## 三、查看CPU节能

* `cat /proc/cpuinfo | grep -i 'cpu mhz'`: 查看CPU MHz是否一致
* `./i7z_x64bit`: `C0%` 列为 `100` 则说明当前是CPU为C0模式

## 四、设置CPU节能

### （1）RHEL 6.x

直接在grub中添加以下内容，重启主机即可: 

```sh
intel_idle.max_cstate=0 idle=poll
```

### （2）RHEL 7.x

* 1 修改`/etc/default/grub`, 在`GRUB_CMDLINE_LINUX=`行中添加以下内容：

```sh
intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable idle=poll
```

或者只加"intel_pstate=disable"，写入grub以后重启，通过 `tuned-adm` 配置高性能模式 (throughput-performance)

* 2 写入grub, 然后重启主机即可。

```sh
grub2-mkconfig -o /boot/grub2/grub.cfg
```

## Ubuntu

和RHEL 7类似，不过添加 `intel_idle.max_cstate=0 processor.max_cstate=1` 即可。


```sh
/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
tuned-adm profile throughput-performance
cpupower frequency-set -g performance
cpupower frequency-info
cpupower -c all frequency-set -g performance
cpupower -c all frequency-info
```