## /etc/host.conf

文件 `/etc/host.conf` 包含了为解析库声明的配置信息。 它应该每行含一个配置关键字, 其后跟着合适的配置信息。

系统识别的关键字有: `order`, `trim`, `multi`, `nospoof`和 `reorder`:  

* `order`
  * **确定主机查询是如何执行的**
  * 它后面应该跟随**一个或者更多**的查询方式, 用逗号分隔
  * 有效的方式有: **`bind`**, **`hosts`**和 **`nis`**
* `trim`
  * 这个选项**将一个域名作为参数**，在查寻之前它将被从主机名中删去
  * 这个关键字可以多次出现。每次出现其后应该跟随单个的以句点开头的域名. 
  * 如果设置了它, `resolv+` 库会自动截去任何通过 DNS 解析出来的主机名中的域名信息. 这个选项用于本地主机和域. 
  * `trim` 配置项对通过 `NIS` 或者 `hosts` 文件获取的主机名不生效
  * Care should be taken to ensure that **the first hostname for each entry in the hosts file is fully qualified or unqualified**, as appropriate for the local installation
* `multi`
  * 有效的值为: `on` 和 `off`
  * 如果设置为 `on`, `resolv+` 库会返回一台主机在 `/etc/hosts` 文件中出现的的所有有效地址, 而不只是第一个
  * 默认情况下设为 `off` , 否则可能会导致拥有庞大 hosts 文件的站点潜在的性能损失.
* `nospoof`
  * 是否允许对该服务器进行**IP地址欺骗**, 有效的值为: `on` 和 `off`
  * 如果设置为 `on`, `resolv+` 库会尝试阻止主机名欺骗以提高使用 `rlogin` 和 `rsh` 的安全性
  * 它是如下这样工作的: 在执行了一个主机地址的查询之后, `resolv+` 会对该地址执行一次主机名的查询. 如果两者不匹配, 查询即失败.
* `spoofalert`
  * 如果该选项设为 `on` 同时也设置了 `nospoof` 选项, `resolv+` 会通过 `syslog` 设备记录错误报警信息
  * 默认的值为 `off`
* `reorder`
  * 有效的值为: `on` 和 `off`
  * 如果设置为 `on`, `resolv+` 会试图重新排列主机地址, 以便执行 `gethostbyname(3)` 时, 首先列出本地地址(即在同一子网中的地址)
  * 重新排序适合于所有查询方式
  * 默认的值为 `off`.

相关文件

- `/etc/host.conf` : 解析配置文件
- `/etc/resolv.conf` : 解析配置文件
- `/etc/hosts` : 本地主机数据库 