```sh
ping6 /lib64/libcrypto.so.10 no version information
```

解决: 

* 安装 `openssl-devel`
* 如果是源码编译安装的，检查openssl库是否正常加载