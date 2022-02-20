# systemd-timesyncd.service

* 配置文件

```
/etc/systemd/timesyncd.conf

/etc/systemd/timesyncd.conf.d/*.conf

/run/systemd/timesyncd.conf.d/*.conf

/usr/lib/systemd/timesyncd.conf.d/*.conf
```

* Default

```conf
[Time]
#NTP=10.2.224.11 10.2.224.12
#FallbackNTP=ntp.ubuntu.com
```

* Example

```conf
[Time]
NTP=10.2.224.11
FallbackNTP=10.2.224.12
```

* 配置项详解

    * `NTP=`

        一个空格分隔的NTP服务器列表，可以使用主机名，也可以使用IP地址。 在运行时，此处设置的列表将与 `systemd-networkd.service(8)` 中已配置的NTP服务器列表合并在一起。`systemd-timesyncd` 将会依次尝试列表中的每个NTP服务器，直到同步成功为止。如果为此选项设置一个空字符串，那么表示清空所有此选项先前已设置的NTP服务器列表。此选项的默认值为空。

    * `FallbackNTP=`

        一个空格分隔的NTP服务器列表，用作备用NTP服务器。 可以使用主机名，也可以使用IP地址。 如果所有已配置在 `systemd-networkd.service(8)` 中的NTP服务器以及上述 NTP= 中设置的NTP服务器都尝试失败， 那么将尝试此处t设置的备用NTP服务器。 如果为此选项设置一个空字符串， 那么表示清空所有此选项先前已设置的NTP服务器列表。 若未设置此选项， 则使用编译时设置的默认备用NTP服务器。

    * `RootDistanceMaxSec=`

        最大可接受的"root distance"秒数(最大误差)。 默认值为 5 秒。

    * `PollIntervalMinSec=`, `PollIntervalMaxSec=`

        NTP消息的 **最小/最大轮询间隔** 秒数，`PollIntervalMinSec=` 必须不小于 16 秒，`PollIntervalMaxSec=` 必须大于 `PollIntervalMinSec=`。`PollIntervalMinSec=` 默认为 32 秒，`PollIntervalMaxSec=` 默认为 2048 秒。
