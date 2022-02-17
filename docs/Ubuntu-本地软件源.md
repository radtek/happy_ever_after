# Ubuntu

## 挂载ISO镜像, 配置本地软件源

* 清空或者注释 /etc/apt/sources.list 内容

* 挂载ISO至 /media/cdrom

    ```sh
    mount /dev/cdrom /media/cdrom
    ```

* 添加本地目录到软件源

    ```sh
    sudo apt-cdrom -m -d=/media/cdrom add
    apt-get update
    ```
