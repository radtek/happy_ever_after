## 1. 生成公私钥

```bash
ssh-keygen -t rsa
```

## 2. 拷贝公钥至目标主机

```bash
ssh-copy-id -i /root/.ssh/id_rsa.pub root@192.168.55.8
```

## 3. 可免密登录root@192.168.55.8

```bash
ssh-keygen -t rsa -f ~/.ssh/id_rsa -N "" -q                
#-N指定私钥的密码，可用以下命令修改
ssh-keygen -p -P "123qweQ" -N "" -f /home/qwer/.ssh/id_rsa
sshpass -p123456 ssh-copy-id -i ~/.ssh/id_rsa.pub " root@172.16.1.$ip  -o StrictHostKeyChecking=no "
```


## sshpass 用法

```bash
sshpass -p123qweQ ssh root@192.168.163.241 'ls /root'
sshpass -f ~/password ssh root@192.168.163.241 'ls /root'
sshpass -p123qweQ scp -o StrictHostKeyChecking=no root@192.168.1.12:/tmp/testfile /root/

sshpass -p123qweQ ssh -o StrictHostKeyChecking=no root@192.168.1.103 "lsblk "
```