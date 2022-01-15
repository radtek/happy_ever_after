## httpd yum源虚拟主机

> 在Fedora 33中，需要将welcome.conf删除，才能正常访问文件夹

```conf
<VirtualHost 192.168.1.1:80>
    DocumentRoot "/var/www/html/yum"
    ServerName 192.168.1.1
    ErrorLog "/var/log/httpd/yum-error_log"
    CustomLog "/var/log/httpd/yum-access_log" common

    <Directory "/var/www/html/yum">
        Options FollowSymLinks Indexes
        AllowOverride None
        Order Deny,Allow
        Deny From all
        Allow From 192.168.1.0/24
    </Directory>

</VirtualHost>
```

```
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="80" accept"
```