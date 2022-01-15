## Fedora 安装向日葵

1. 安装

```sh
rpm -ivh --nodeps  --force sunloginclient-11.0.0.35346-1.x86_64.rpm
```

2. 修改文件

```sh
cd /usr/local/sunlogin

vim scripts/commmon.sh

...
if [ $os_name == 'ubuntu' ]; then
        os_version=`cat /etc/issue | cut -d' ' -f2`
elif [ $os_name == 'kylin' ]; then
        os_version=`cat /etc/issue | cut -d' ' -f2`
elif [ $os_name == 'Deepin' ]; then
        os_version=`cat /etc/lsb-release |grep DISTRIB_RELEASE | cut -d'=' -f2 |sed 's/"//g'`
elif [ $os_name == 'Fedora' ]; then                                   <== 新增
        os_version=`cat /etc/fedora-release | cut -d' ' -f3`          <== 新增
elif  [ "$os_name" == "centos" ] || [ "$(echo $os_name |grep redhat)" != "" ] ; then
        os_version=`rpm -q centos-release|cut -d- -f3`
fi
...
```

```sh
vim rpminstall.sh

...
if [ "$os_name" == 'fedora' ] || [ "$os_name" == 'centos' ] || [ "$(echo $os_name |grep redhat)" != "" ]; then   <== 修改
        echo 'check operate system OK'
else
        echoAndExit 'unknown OS it not impl'
fi
...
#echo "create init"

if [ "$os_name" == 'fedora' ] || [ "$os_name" == "centos" ] || [ $(echo $os_name |grep redhat) != "" ] ; then    <== 修改
        gdm_init_create
...
```

```sh
vim scripts/start.sh

...
elif [ "$os_name" == "fedora" ] || [ "$os_name" == "centos" ] || [ "$(echo $os_name |grep redhat)" != "" ] ; then  <== 修改
        if [ $os_version_int -lt 7 ]; then
                isinstalledcentos
                if [ $isinstalled == true ]; then
...
```

3.  执行安装, 移除开机自启动

```sh
./rpminstall.sh
systemctl disable runsunloginclient
```