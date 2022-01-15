## 手动调节风扇风速

Linux内核中有个`thinkpad_acpi`的模块，可以利用它来调节风扇转速

```sh
shell> locate thinkpad_acpi
/dev/input/by-path/platform-thinkpad_acpi-event
/usr/lib/modules/5.11.10-200.fc33.x86_64/kernel/drivers/platform/x86/thinkpad_acpi.ko.xz   <=
/usr/lib/modules/5.11.7-200.fc33.x86_64/kernel/drivers/platform/x86/thinkpad_acpi.ko.xz    <=
/var/lib/systemd/rfkill/platform-thinkpad_acpi:bluetooth
```

**加载模块**

```sh
shell> vi /etc/modprobe.d/thinkpad_acpi.conf
options thinkpad_acpi experimental=1 fan_control=1  # <= 添加

shell> modprobe thinkpad_acpi
```

**手动调节**

```sh
shell> cat /proc/acpi/ibm/fan
status:		enabled
speed:		3575
level:		auto    # <= 此时风扇速度为'auto', 即自动调节
commands:	level <level> (<level> is 0-7, auto, disengaged, full-speed)
commands:	enable, disable
commands:	watchdog <timeout> (<timeout> is 0 (off), 1-120 (seconds))

shell> echo level 0 > /proc/acpi/ibm/fan            # (fan off)
shell> echo level 2 > /proc/acpi/ibm/fan            # (low speed)
shell> echo level 4 > /proc/acpi/ibm/fan            # (medium speed)
shell> echo level 7 > /proc/acpi/ibm/fan            # (maximum speed)
shell> echo level auto > /proc/acpi/ibm/fan         # (automatic - default)
shell> echo level disengaged > /proc/acpi/ibm/fan   # (disengaged)
```

## 利用`thinkfan`自动调节风扇风速

**安装**

```sh
shell> dnf -y install thinkfan

shell> rpm -ql thinkfan-1.2.1-2.fc33.x86_64 
/etc/modprobe.d/thinkfan.conf    <= 此文件和上文手动配置的/etc/modprobe.d/thinkpad_acpi.conf内容相似, 可将上文的文件删除
/etc/sysconfig/thinkfan          <= 启动参数
/etc/thinkfan.conf               <= 配置文件
/usr/lib/.build-id
/usr/lib/.build-id/2c
/usr/lib/.build-id/2c/2d91675b8dc817efb31d5d35cf9ff3a1311041
/usr/lib/systemd/system/thinkfan-sleep.service
/usr/lib/systemd/system/thinkfan-wakeup.service
/usr/lib/systemd/system/thinkfan.service   <= systemd托管服务
/usr/sbin/thinkfan
/usr/share/doc/thinkfan
/usr/share/doc/thinkfan/README.md
/usr/share/doc/thinkfan/thinkfan.yaml
/usr/share/licenses/thinkfan
/usr/share/licenses/thinkfan/COPYING
/usr/share/man/man1/thinkfan.1.gz
/usr/share/man/man5/thinkfan.conf.5.gz
```

**配置**

- 查找 `thinkfan` 所需的几个标准文件

```sh
shell> find /sys/devices -type f -name "temp*_input"
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp6_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp13_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp3_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp10_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp7_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp14_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp4_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp11_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp8_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp1_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp15_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp5_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp12_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp9_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp2_input    # <= 这些文件需要写入配置文件
/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp16_input   # <= 这些文件需要写入配置文件
/sys/devices/platform/coretemp.0/hwmon/hwmon8/temp3_input
/sys/devices/platform/coretemp.0/hwmon/hwmon8/temp4_input
/sys/devices/platform/coretemp.0/hwmon/hwmon8/temp1_input
/sys/devices/platform/coretemp.0/hwmon/hwmon8/temp5_input
/sys/devices/platform/coretemp.0/hwmon/hwmon8/temp2_input
/sys/devices/pci0000:00/0000:00:1c.4/0000:02:00.0/hwmon/hwmon4/temp1_input
/sys/devices/pci0000:00/0000:00:1c.4/0000:02:00.0/hwmon/hwmon4/temp2_input
/sys/devices/virtual/thermal/thermal_zone0/hwmon1/temp1_input
/sys/devices/virtual/thermal/thermal_zone3/hwmon5/temp1_input
/sys/devices/virtual/thermal/thermal_zone6/hwmon10/temp1_input
```

- 编辑`/etc/thinkfan.conf`

清空原文件, 写入以下内容

```conf
tp_fan /proc/acpi/ibm/fan

hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp6_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp13_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp3_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp10_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp7_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp14_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp4_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp11_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp8_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp1_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp15_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp5_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp12_input
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp9_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp2_input 
hwmon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp16_input

(0,0,42)
(1,40,47)
(2,45,52)
(3,50,57)
(4,55,62)
(5,60,67)
(6,65,72)
(7,70,77)
(127,75,32767)
```

- 启动服务

```sh
shell> systemctl enabled thinkfan
shell> systemctl start thinkfan
```

- 可能的报错

`ERROR: Lost sensor read_temps: Failed to read temperature(s) from /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp2_input: No such device or address`

注释 `hwwon /sys/devices/platform/thinkpad_hwmon/hwmon/hwmon6/temp2_input`行