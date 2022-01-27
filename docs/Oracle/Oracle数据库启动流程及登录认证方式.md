# Oracle数据库启动流程及登录认证方式

## 启动

* Windows:

    * 1) 启动监听

        ```sh
        lsnrctl start
        ```
    * 2) 启动数据库/实例

        ```sh
        oradim –startup –sid 数据库实例名
        ```

* Linux:

    * 1) 启动监听

        ```sh
        lsnctl start
        ```

    * 2) 启动数据库/实例

        ```sh
        # Step 1
        sqlplus / as sysdba
        # or 
        sqlplus sys/change_on_install as sysdba
        # or
        sqlplus  /nolog
        SQL> conn / as sysdba
        # SQL> conn sys/change_on_install as sysdba

        # Step 2
        SQL> startup
        ```

> Note: 先起监听还是先起实例? 参考 [问题集-"ORA-12514"](问题集.md) .

## 登录认证方式

* Windows:

    * 操作系统认证

    如果当前用户属于本地操作系统的 `ora_dba` 组(对于Windows操作系统而言), 即可通过操作系统认证。

    * Oracle数据库验证(密码文件验证)

        * 对于普通用户, oracle默认使用数据库验证
        * 对于特权用户(如: sys), oracle默认使用操作系统认证; 如果验证不通过, 再到数据库验证(密码文件验证)

    * 修改认证方式

        * `SQLNET.AUTHENTICATION_SERVICES= (NTS)` : 基于操作系统验证
        * `SQLNET.AUTHENTICATION_SERVICES= (NONE)`: 基于Oracle验证
        * `SQLNET.AUTHENTICATION_SERVICES= (NONE，NTS)`: 二者共存
        * 不设置此参数 或 `sqlnet.ora`文件不存在 或 `SQLNET.AUTHENTICATION_SERVICES =`: 基于Oracle密码文件验证
        * `SQLNET.AUTHENTICATION_SERVICES = (ALL)`: 不支持(*ORA-12641: 验证服务无法初始化(Authentication service failed to initialize)*)

* Linux:
 
    * 默认情况下, Oracle数据库 `sqlnet.ora` 文件(甚至`sqlnet.ora`文件都没有)中没有 `SQLNET.AUTHENTICATION_SERVICES` 参数, 此时是**基于操作系统认证和oracle密码验证共存**的:
        * 登录进Linux系统以后, 任何用户都能直接以 sysdba 角色连接数据库, 无需输入密码; 
        * sys 用户只能以 sysdba/sysoper/sysasm等角色登录;
        * 其他普通用户如果要以Normal登录, 需要输入密码; 

    * 加上 `SQLNET.AUTHENTICATION_SERVICES` 参数后, 操作系统认证失效; 不管设置为 `=(NONE)`, `=(NONE,NTS)`或者 `=(NTS)`，此时都是 **基于Oracle数据库密码验证** 的。


## 密码文件

作用：主要进行SYSDBA和SYSOPER权限的身份认证。密码文件存放着被授予 SYSDBA 或 SYSOPER 权限的用户的用户名和密码。它是一个加密的文件，用户不能修改这个文件，但是可以使用 strings 命令看到密码的HASH值

* 在Linux系统中，密码文件一般保存在 `$ORACLE_HOME/dbs` 目录下，文件名为 `orapw$SID`
* 在Windows系统中，密码文件一般保存在 `%ORACLE_HOME%\database` 目录下，文件名为 `PWD$SID.ora`

```sh
# 密码文件查找顺序
---> orapw<sid> ---> orapw ---> Failure
```

`REMOTE_LOGIN_PASSWORDFILE` 设置 非 NONE, 且密码文件位置
