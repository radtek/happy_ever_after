# Installation


## Prerequisites

### User Creation

* create stor2rrd user under root user

```sh
useradd -c "STOR2RRD user" -m stor2rrd
```

* Increase limits for user stor2rrd and the WEB server user (under root)

```sh
~] vi /etc/security/limits.conf

stor2rrd        hard    stack           -1
stor2rrd        soft    stack           -1
stor2rrd        hard    data            -1
stor2rrd        soft    data            -1
stor2rrd        hard    nofile          32768 
stor2rrd        soft    nofile          32768 
stor2rrd        hard    nproc           5000
stor2rrd        soft    nproc           5000

apache          hard    stack           -1
apache          soft    stack           -1
apache          hard    data            -1
apache          soft    data            -1
```

### Linux RedHat, CentOS

* RHEL 8: enable the **codeready-builder-for-rhel-8-*-rpms** repository

```sh
ARCH=$( /bin/arch )
subscription-manager repos --enable "codeready-builder-for-rhel-8-${ARCH}-rpms"
```

* CentOS 8: enable the **PowerTools** repository

```sh
yum config-manager --set-enabled PowerTools
# or
dnf config-manager --set-enabled powertools
```

You can also just open /etc/yum.repos.d/CentOS-Linu-PowerTools.repo with a text editor and set enabled= to 1 instead of 0

[Follow this](https://stor2rrd.com/rhel8-install.php) to get installed SNMP and PDF support in the tool on RHEL8 and CentOS8.

* RedHat, CentOS: all versions

```sh
umask 0022
yum install perl rrdtool rrdtool-perl httpd
# yum install epel-release 
yum install perl-TimeDate perl-XML-Simple perl-XML-SAX perl-XML-LibXML perl-Env perl-CGI perl-Data-Dumper perl-LWP-Protocol-https perl-libwww-perl perl-Time-HiRes perl-IO-Tty
yum install perl-PDF-API2 perl-JSON-XS
yum install ed bc libxml2 sharutils tar
yum install graphviz perl-Want
```

Note that rrdtool-perl and epel-release (this is necessary only for [PDF reporting](https://stor2rrd.com/pdf.php)) might not be in your RedHat base repository especially for RHEL 6.x and olders.

Install CentOS package instead [rrdtool-perl-1.4.8-9.el7.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/rrdtool-perl-1.4.8-9.el7.x86_64.rpm) and [epel-release-7-9.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/epel-release-7-9.noarch.rpm)


## Web

* Apache install

```sh
yum install httpd
```

* Firewalld setting

```sh
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent
firewall-cmd --add-port=8162/tcp --permanent

firewall-cmd --reload
```

* Configuration: Linux CentOS, RedHat

Append at the end of `/etc/httpd/conf/httpd.conf` following

```sh
~] vi /etc/httpd/conf/httpd.conf

AddHandler cgi-script .sh
# DocumentRoot  "/home/stor2rrd/stor2rrd/www/"
Alias /stor2rrd  "/home/stor2rrd/stor2rrd/www/"
<Directory "/home/stor2rrd/stor2rrd/www/">
    AllowOverride 
    Options Indexes FollowSymLinks 
    Require all granted
</Directory>
# CGI-BIN
ScriptAlias /stor2rrd-cgi/ "/home/stor2rrd/stor2rrd/stor2rrd-cgi/"
<Directory "/home/stor2rrd/stor2rrd/stor2rrd-cgi">
    AllowOverride 
    SetHandler cgi-script
    Options ExecCGI FollowSymLinks
    Require all granted
</Directory>
```

* SELinux

    * Disable SELinux only for Apache

    ```sh
    # Step 1. Query for the Boolean value you need to change:
    ~] getsebool -a | grep httpd_dis
    httpd_disable_trans --> off

    # Step 2. Disable the SELinux protection:
    ~] setsebool -P httpd_disable_trans=1

    # Step 3. Verify that the Boolean has changed:
    ~] getsebool -a | grep httpd_dis
    httpd_disable_trans --> on
    ```

    * Globally disable SELinux

    ```sh
    ~] setenforce Permissive
    ~] vi /etc/sysconfig/selinux
    SELINUX=disabled
    ```

## STOR2RRD

Download the latest [STOR2RRD server](https://stor2rrd.com/download-xorux.php)

[Upgrade](https://stor2rrd.com/upgrade.php) your already running STOR2RRD instance.

* Product installation

```sh
root ~] su - stor2rrd
stor2rrd ~] tar xvf stor2rrd-7.XX.tar
stor2rrd ~] cd stor2rrd-7.XX
stor2rrd ~] ./install.sh
stor2rrd ~] cd /home/stor2rrd/stor2rrd
```

* Configure parameters in `etc/stor2rrd.cfg`.

Install process should do most of that automatically

Here is the list of parameters which need to be reviewed:

```sh
stor2rrd ~] vi /home/stor2rrd/stor2rrd/etc/stor2rrd.cfg  
  WEBDIR=/home/stor2rrd/stor2rrd/www  
  RRDTOOL=/usr/bin/rrdtool
  PERL=/usr/bin/perl  
```

* Schedule to run STOR2RRD from `stor2rrd` crontab

```sh
stor2rrd ~] crontab -e

# STOR2RRD UI (just ONE entry of load.sh must be there)
5 * * * * /home/stor2rrd/stor2rrd/load.sh > /home/stor2rrd/stor2rrd/load.out 2>&1
```

You might need to add stor2rrd user (lpar2rrd for Virtual Appliance) into /var/adm/cron/cron.allow (/etc/cron.allow on CentOS 8) under root user when crontab cmd fails.

```sh
echo "stor2rrd" >> /var/adm/cron/cron.allow
```

* Go to the web UI: http://<your web server>/stor2rrd/

```sh
chmod 755 /home/stor2rrd
```

## Troubleshooting

* If you have any problems with the UI then check:

(note that the path to Apache logs might be different, search apache logs in `/var`)

```sh
tail /var/log/httpd/error_log             # Apache error log
tail /var/log/httpd/access_log            # Apache access log
tail /var/tmp/stor2rrd-realt-error.log    # STOR2RRD CGI-BIN log
tail /var/tmp/systemd-private*/tmp/stor2rrd-realt-error.log # STOR2RRD CGI-BIN log when Linux has enabled private temp
```

* Test of CGI-BIN setup

```sh
umask 022
cd /home/stor2rrd/stor2rrd/
cp bin/stor-test-healthcheck-cgi.sh stor2rrd-cgi/
```

go to the web browser: `http://<your web server>/stor2rrd/test.html`

You should see your Apache, STOR2RRD, and Operating System variables, if not, then check Apache logs for connected errors
