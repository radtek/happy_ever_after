
```sh
\[\e[31;1m\][Linux-SUSE-SP5]\[\e[0m\]\[\e[32;1m\]\u@$BIGIP:\w\n($?)[\[\e[0m\]`if [ $? -eq "0" ]; then echo "\[\033[7;32m\]";else echo "\[\033[7;35m\]"; fi`\D{%Y-%m-%d-%H-%M-%S }\[\e[0m\]\[\e[32;1m\]]\[\033[m\]`[ $UID -eq 0 ] && echo -n "# " || echo -n "$ "`


LOCAL_HOSTNAME=`hostname | tr 'a-z' 'A-Z'`
LOCAL_IP=`ip -4 -o addr | grep -aPo '(?<=inet\s)[0-9.]*' | grep -v '127.0.0.1' | head -n 1`
PS1='\[\e[31;1m\][$LOCAL_HOSTNAME]\[\e[0m\]\[\e[32;1m\]\u@$LOCAL_IP:\w\n($?)[\[\e[0m\]`if [ $? -eq 0 ]; then echo "\[\033[7;32m\]"; else echo "\[\033[7;35m\]"; fi`\D{%Y-%m-%d-%H:%M:%S}\[\e[0m\]\[\e[32;1m\]]\[\e[0m\]`[ $UID -eq 0 ] && echo -n "# " || echo -n "$ "`'

LOCAL_HOSTNAME=`hostname | tr 'a-z' 'A-Z'`
LOCAL_IP=`ip -4 -o addr | grep -aPo '(?<=inet\s)[0-9.]*' | grep -v '127.0.0.1' | head -n 1`
PS1='\[\e[31;1m\][$LOCAL_HOSTNAME]\[\e[0m\]\[\e[32;1m\]\u@$LOCAL_IP:\w\n($?)[\[\e[0m\]`if [ $? -eq 0 ]; then echo "\[\033[1;32m\]"; else echo "\[\033[1;35m\]"; fi`\D{%Y-%m-%d-%H:%M:%S}\[\e[0m\]\[\e[32;1m\]]\[\e[0m\]`[ $UID -eq 0 ] && echo -n "# " || echo -n "$ "`'

LOCAL_HOSTNAME=`hostname | tr 'a-z' 'A-Z'`
LOCAL_IP=`ip -4 -o addr | grep -aPo '(?<=inet\s)[0-9.]*' | grep -v '127.0.0.1' | head -n 1`
PS1='\[\e[31;1m\][$LOCAL_HOSTNAME]\[\e[0m\]\u\[\e[32;1m\]@$LOCAL_IP:\w\n($?)[\[\e[0m\]`if [ $? -eq 0 ]; then echo "\[\033[1;32m\]"; else echo "\[\033[1;35m\]"; fi`\D{%Y-%m-%d-%H:%M:%S}\[\e[0m\]\[\e[32;1m\]]\[\e[0m\]`[ $UID -eq 0 ] && echo -n "# " || echo -n "$ "`'
```

效果：


```
[Linux-SUSE-SP5]root@10.67.132.221:~
(0)[2021-06-23-17-18-04 ]#

[Linux-SUSE-SP5]root@10.67.132.221:~
(130)[2021-06-23-17-13-11 ]#
```

