> [https://support.oracle.com/knowledge/Oracle%20Linux%20and%20Virtualization/2309075_1.html](https://support.oracle.com/knowledge/Oracle%20Linux%20and%20Virtualization/2309075_1.html)

## SYMPTOMS

Local users cannot login to the server.  The /var/log/secure log shows entries similar to:

```sh
Sep 18 10:44:39 hostname sshd[XXXXXX]: Connection from XX.XX.XX.XX port XXXXX
Sep 18 10:44:40 hostname sshd[XXXXXX]: pam_sss(sshd:account): Request to sssd failed. Connection refused >>>
Sep 18 10:44:40 hostname sshd[XXXXXX]: Failed password for username from XX.XX.XX.XX port XXXXX ssh2
Sep 18 10:44:40 hostname sshd[XXXXXX]: fatal: Access denied for user <User_name> by PAM account configuration
```

## CAUSE

The PAM (Pluggable Authentication Module) subsystem module pam_sss.so is blocking the local user authentication.

PAM is not allowing user access to non-LAPD users when the sssd(8) service is not running.

```sh
shell> cat /etc/pam.d/system-auth
    ...
    auth sufficient pam_sss.so use_first_pass
    ...
    password sufficient pam_sss.so use_authtok
    ...
    session optional pam_sss.so

shell> cat /etc/pam.d/password-auth
    ...
    auth sufficient pam_sss.so use_first_pass
    ...
    password sufficient pam_sss.so use_authtok
    ...
    session optional pam_sss.so
```

## SOLUTION

Validate the availability of the LDAP server and then run the below command to restart the sssd(8) service:

```sh
service sssd restart
```

## One More Thing

* 检查sssd服务是否正常
* 如果升级了内核, 推荐同步升级sssd至最新版本