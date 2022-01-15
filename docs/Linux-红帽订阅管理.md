## 注册

- (1) 执行以下命令，输入用户名和密码将系统注册到rhn。

```bash
subscription-manager register
```

- (2) 列出系统所有可用的订阅，并记录你在系统激活的订阅池Id。

```bash
subscription-manager list --available --all
```

- (3) 使用订阅池id激活订阅。

```bash
subscription-manager attach --pool=8a85f98154ef8eb40154f1b1d3620670
```

- (4) 关闭系统所有仓库。 

```bash
subscription-manager repos --disable="*"
```

- (5) 仅打开系统rhel6仓库。

```bash
subscription-manager repos --enable=rhel-7-server-rpms
```

- (6) 列出系统所有仓库。

```bash
yum repolist
```

- (7) 重新注册

```bash
sudo subscription-manager remove --all
sudo subscription-manager unregister
sudo subscription-manager clean
sudo subscription-manager register
sudo subscription-manager refresh
sudo subscription-manager attach --auto
```

## 使用

```sh
yum install ntp --downloadonly --downloaddir=/tmp/
```

```sh
# 7及以下版本
reposync --plugins --newest-only --delete --download_path=<download_path> --repoid=<repo_id>
# 8版本
dnf reposync --newest-only --delete --download-metadata --download-path=<download_path> --repoid=<repo_id>
```


## 附: 关于repodata

### `repodata/`目录下的文件信息

执行 `createrepo` 会在当前目录下生成一个 `repodata` 的文件夹, 里面一般有以下几个文件:
- `primary.xml.gz`: 包含所有rpm文件列表、依赖关系、软件包安装列表 
- `filelists.xml.gz`: 包含所有rpm包的配置文件列表  
- `other.xml.gz`: 包含软件包其他信息，比如更改记录  
- `comps.xml`: 包含软件包组的列表，控制软件包group安装  
- `repomd.xml`: 包含primary/filelist/other文件的时间戳、检验等等之类   

### yum安装rpm包执行过程

- (1) 在 `primary.xml` 里找到需要安装的包  
- (2) 在 `primary.xml` 中获取到安装包完整名词和依赖包列表  
- (3) 在 `primary.xml` 中根据 `<location href=xxx/>`获取安装包路径
- (4) 在 `primary.xml` 中获取依赖包名和对应的`pkgid`，并在 `filelists.xml` 中获取到配置文件
- (5) 根据已有信息获取rpm包并安装  

### 需要特别注意的"路径问题"

> yum命令去读取 `repodata/primary.xml` 中记录的 `<location href=/>` 是以 `repodata` 目录所在那一级目录为基准点的，而执行`createrepo` 命令生成repodata所在目录以及primary.xml，是由我们指定的路径决定的。

> `createrepo` 默认在当前目录下生成 `repodata/`目录, 可通过 `-o` 指定

> `baseurl` : Must be a URL to the directory where the yum repository's `repodata' directory lives. Can be an ++http://++, ++ftp://++ or ++file://++ URL.

yum命令下载rpm包的路径由两部分组成:

```
"repodata目录所在的那一级目录(baseurl)"/"文件repomd.xml中<location href=xxx>路径"

#eg.
#   > /tmp/repodata
#   > <location href="t/tree-1.6.0-10.el7.x86_64.rpm">
#   > yum下载rpm包完整路径: /tmp/t/tree-1.6.0-10.el7.x86_64.rpm
```

例如：`/tmp/package/dir1` 存放着rpm包, `cd /tmp`进入`/tmp`: 

- 当执行 `createrepo /tmp/package` 时:  
    * 当前路径: `/tmp`
    * repodata路径: `/tmp/repodata/`;  
    * `repodata/primary.xml`中记录的rpm包路径:`<location href="dir1/xxx.rpm"/>`;  
    * 此时yum的repo文件配置路径需要指向 `repodata/` 所在路径: `baseurl=file:///tmp/`;  
    * 
    * 安装时, `yum` 无法找到`/tmp/dir1/`, 提示`Error downloading packages`;  

- 当执行 `createrepo /tmp/` 时:  
    * 当前路径: `/tmp`
    * repodata路径: `/tmp/repodata/`;  
    * `repodata/primary.xml`中记录的rpm包路径:`<location href="package/dir1/xxx.rpm"/>`;  
    * 此时yum的repo文件配置路径需要指向 `repodata/` 所在路径: `baseurl=file:///tmp/`;  
    * 安装时, `yum` 能过准确的找到`/tmp/package/dir1/xxx.rpm`; 

- 综上, 最佳实践为:  

    ```bash
    createrepo /path/of/package -o /path/of/package
    createrepo .
    ```