- awk指定输入、输出分隔符
- awk输出多列

## awk指定输出分隔符

用法 | 解释
-- | --
`-F','` | 指定输入分隔符为"`,`"
`-v FS=',' -v OFS=':'` | 指定输入分隔符为"`,`"，输出分隔符为"`:`"

```sh
shell> echo "chrony,postfix" | awk -v FS=',' -v OFS=':' '{print $1,$2}'
chrony:postfix
```

> `$0` is the whole record 

注意， 使用`$0`时，`OFS`未生效：

```sh
shell> echo "chrony,postfix,sshd" | awk -v FS=',' -v OFS=':' '{print $0}'
chrony,postfix,sshd
```

## awk输出多列

- 使用 `$1`, `$2`, ...形式

- 使用 `$0` 搭配 `$1`,`$2`

```
shell> cat a
1 2 3 4 5 6 7 8 9 0
1 2 3 4 5 6 7 8 9 0

shell> cat a | awk '{$1=""; print $0}'  #输出第2列到最后一列, 实际是将第一列替换成空
 2 3 4 5 6 7 8 9 0
 2 3 4 5 6 7 8 9 0

shell> cat a | awk '{$2=""; print $0}'  #将第二列替换成空
1  3 4 5 6 7 8 9 0
1  3 4 5 6 7 8 9 0

shell> cat a | awk '{for(i=1; i<=5; i++){ $i=""};print $0}' #输出第6列到最后一列, 实际是将第前5列替换成空
     6 7 8 9 0
     6 7 8 9 0
```

- 使用函数

```sh
shell> cat a | awk '{for (i=4;i<=NF;i++)printf("%s ", $i);print ""}' #输出第4列到最后一列, 使用空格作为分隔符
4 5 6 7 8 9 0 
4 5 6 7 8 9 0 

shell> cat a | awk '{for (i=4;i<=NF;i++)printf("%s,", $i);print ""}' #输出第4列到最后一列, 使用","作为分隔符
4,5,6,7,8,9,0,
4,5,6,7,8,9,0,
```

> **注**: 以上用法需要处理掉每行尾部多余的分隔符