### `${parameter:+expression}` 和 `${parameter+expression}`

- 当 `parameter` **未定义**时，直接使用`parameter`的值(null)
- 当 `parameter` 定义为null时
    * `${parameter:+expression}`直接使用`parameter`的值(null)
    * `${parameter+expression}`临时将`expression`的值赋给`parameter`
- 当 `parameter` 已定义且不为null时，临时将`expression`的值赋给`parameter`

### `${parameter:-expression}` 和 `${parameter-expression}`

- 当 `parameter` **未定义**时，则临时将`expression`的值赋给`parameter` 
- 当 `parameter` 定义为null时
    * `${parameter:-expression}`临时将`expression`的值赋给`parameter`
    * `${parameter-expression}`直接使用`parameter`的值
- 当 `parameter` 已定义且不为null时，则直接使用`parameter`的值

 
### `${parameter:=expression}` 和 `${parameter=expression}`

- 当 `parameter` **未定义**时，则将`expression`的值赋给`parameter` 
- 当 `parameter` 定义为null时
    * `${parameter:=expression}`将`expression`的值赋给`parameter`
    * `${parameter=expression}`则直接使用`parameter`的值(不做操作)
- 当 `parameter` 已定义且不为null时，则直接使用`parameter`的值(不做操作)



### 1. 基本参数扩展: `${parameter}`

### 2. 间接参数扩展: `${!parameter}`

其中引用的参数并不是`parameter`, 而是`parameter`的实际值

```sh
shell> parameter="var"
shell> var="helloworld"
shell> echo ${!parameter}
helloworld
```

### 3. 大小写修改

| 写法  | 作用 |
| --   | :-- |
| `${a^}`   | 替换变量a中的第一个小写字母为大写 |
| `${a^^}`  | 替换变量a中的所有小写字母为大写 |
| `${a,}`   | 替换变量a中的第一个大写字母为小写 |
| `${a,,}`  | 替换变量a中的所有大写字母为小写 |
| `${a~}`   | 替换变量a中的第一个字母: 大写=>小写, 小写=>大写 |
| `${a~~}`  | 替换变量a中的全部字符: 大写=>小写, 小写=>大写 |

### 4. 空参数处理

- `${parameter:-word}`, `${parameter-word}`
- `${parameter:+word}`, `${parameter+word}`
- `${parameter:=word}`, `${parameter=word}`
- `${parameter:?word}`, `${parameter?word}`

#### 4.1 `${parameter:-word}` 和 `${parameter-word}`

```sh
# 1. 定义两个变量para01,para02, para03不定义
shell> para01=""
shell> para02="something"
shell> set | grep para
para01=
para02=something

# 2. para01定义为空, 此时${para01:-otherthing}输出otherthing, para01的值未被修改
shell> echo ${para01:-otherthing}
otherthing
shell> echo ${para01}
            # <= 为空

# 3. para02定义为something, 此时${para02:-otherthing}输出something, para02的值未被修改
shell> echo ${para02:-otherthing}
something
shell> echo ${para02}
something

# 3. para03未定义, 此时${para03:-otherthing}输出otherthing, para03的值未被修改, 同时也没有变量para03
shell> echo ${para03:-otherthing}
otherthing
shell> echo ${para03}
            # <= 为空
shell> set | grep para
para01=
para02=something
```

观察 `${parameter-word}`, `para01` 和 `para02` 都没有输出otherthing, 说明使用的是本身的值

```sh
shell> set | grep para
para01=
para02=something
shell> echo ${para01-otherthing}

shell> echo ${para01}

shell> echo ${para02-otherthing}
something
shell> echo ${para02}
something
shell> echo ${para03-otherthing}
otherthing
shell> echo ${para03}

shell> set | grep para
para01=
para02=something
```

**总结-1**: 
- 当 **变量未定义** 或者 **变量定义为空** 时, `${parameter:-word}` 会临时使用 `word` 作为变量解析结果 
- 当 **变量定义不为空** 时, `${parameter:-word}` 会取 `parameter` 的值作为解析结果
- `${parameter-word}`只会检查**变量是否定义**, 无论定义为何值: **变量已定义**=> `${parameter-word}`取 `parameter` 的值作为变量解析结果; 相反, 取 `word` .
- 两种写法均不会对 `parameter` 做任何操作


#### 4.2 `${parameter:+word}` 和 `${parameter+word}`

```sh
shell> set | grep para
para01=
para02=something

# 1. ${parameter:+word} 相关验证结果
shell> echo ${para01:+otherthing}
            # <= 为空
shell> echo ${para01}
            # <= 为空
shell> echo ${para02:+otherthing}
otherthing
shell> echo ${para02}
something
shell> echo ${para03:+otherthing}
            # <= 为空
shell> echo ${para03}
            # <= 为空
shell> set | grep para
para01=
para02=something

# 2. ${parameter+word} 相关验证结果
shell> echo ${para01+otherthing}
otherthing
shell> echo ${para01}
            # <= 为空
shell> echo ${para02+otherthing}
otherthing
shell> echo ${para02}
something
shell> echo ${para03+otherthing}
            # <= 为空
shell> echo ${para03}
            # <= 为空
shell> set | grep para
para01=
para02=something
```

**总结-2**: 
- 当 **变量未定义** 或者 **变量定义为空** 时, `${parameter:+word}` 会使用 `parameter` 的值作为变量解析结果 
- 当 **变量定义不为空** 时, `${parameter:+word}` 会临时使用 `word` 作为解析结果
- `${parameter+word}`只会检查**变量是否定义**, 无论定义为何值: **变量已定义**=> `${parameter+word}`取 `word` 作为变量解析结果; 相反, 取 `parameter` 的值.
- 两种写法均不会对 `parameter` 做任何操作

#### 4.3 `${parameter:=word}` 和 `${parameter=word}`

```sh
shell> set | grep para
para01=
para02=something

# 1. ${parameter:=word} 相关验证结果
shell> echo ${para01:=otherthing}
otherthing
shell> echo ${para01}
otherthing
shell> echo ${para02:=otherthing}
something
shell> echo ${para02}
something
shell> echo ${para03:=otherthing}
otherthing
shell> echo ${para03}
otherthing
shell> set | grep para
para01=otherthing
para02=something
para03=otherthing

# 2. ${parameter=word} 相关验证结果
shell> set | grep para
para01=
para02=something
shell> echo ${para01=otherthing}
            # <= 为空
shell> echo ${para01}
            # <= 为空
shell> echo ${para02=otherthing}
something
shell> echo ${para02}
something
shell> echo ${para03=otherthing}
otherthing
shell> echo ${para03}
otherthing
shell> set | grep para
para01=
para02=something
para03=otherthing
```

**总结-3**: 
- 当 **变量未定义** 或者 **变量定义为空** 时, `${parameter:=word}` 会使用 `word` 作为变量解析结果,
- 当 **变量定义不为空** 时, `${parameter:=word}` 会使用 `parameter` 的值作为解析结果
- `${parameter=word}`只会检查**变量是否定义**, 无论定义为何值: **变量已定义**=> `${parameter=word}`取 `parameter` 作为变量解析结果; 相反, 取 `word` 的值.
- 以上两种写法, 只要取了 `word` 的值, 那么 `parameter` 值会被同步的修改为 `word`; `parameter` 未定义时, 会将其定义.

#### 4.4 `${parameter:?word}` 和 `${parameter?word}`

```sh
shell> set | grep para
para01=
para02=something
shell> echo ${para01:?otherthing}
-bash: para01: otherthing
shell> echo ${para02:?otherthing}
something
shell> echo ${para03:?otherthing}
-bash: para03: otherthing
shell> echo ${para01?otherthing}
           # <= 为空
shell> echo ${para02?otherthing}
something
shell> echo ${para03?otherthing}
-bash: para03: otherthing
shell> set | grep para
para01=
para02=something
```

**总结-4**: 
- 当 **变量未定义** 或者 **变量定义为空** 时, `${parameter:?word}` 会抛出异常 `-bash: parameter: word`,
- 当 **变量定义不为空** 时, `${parameter:?word}` 会使用 `parameter` 的值作为解析结果
- `${parameter?word}`只会检查**变量是否定义**, 无论定义为何值: **变量已定义**=> `${parameter=word}`取 `parameter` 作为变量解析结果; 相反, 取 `word` 的值.
- 两种写法均不会对 `parameter` 做任何操作


|       参数扩展形式          | `parameter`未定义 | `parameter`定义为NULL | `parameter`定义不为NULL | 备注     | 
| :------------------------- | :-------------- | :------------------ | :-------------- | :----------------- |
| `${parameter:+expression}` | word        | word           | parameter  |                                  |
| `${parameter+expression}`  | word        | parameter      | parameter  |                                  |
| `${parameter:-expression}` | parameter   | parameter      | word       |                                  |
| `${parameter-expression}`  | parameter   | word           | word       |取值为word时,将同步修改parameter的值|
| `${parameter:=expression}` | word        | word           | parameter  |取值为word时,将同步修改parameter的值|
| `${parameter=expression}`  | word        | parameter      | parameter  |                                  |
| `${parameter:?expression}` | 抛出异常     | 抛出异常        | parameter  |                                  |
| `${parameter?expression}`  | 抛出异常     | parameter      | parameter  |                                  |