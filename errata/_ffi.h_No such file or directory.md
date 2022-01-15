## 原因
Linux下缺少libffi和libffi-dev(el)

## 解决方法

* Ubuntu

```sh
sudo apt install libffi libffi-dev -y
```

* Centos

```sh
sudo yum -y install libffi libffi-devel 
```