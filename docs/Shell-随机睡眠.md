## 随机睡眠


```sh
function random_sleep() {
    low=10
    up=30
    max=$(($up-$low+1))
    num=$(($RANDOM+1000000000))
    sleep_time=$(($num%$max+$low))
    echo "sleep_time=$sleep_time"
    sleep $sleep_time
}
```


* `$RANDOM` 取值范围`0-32767`

* 如果要取0-9的值, 可以用 $(($RANDOM*10/32767))

* 如果要取10-100的值, 可以用 $(($RANDOM*100/32767))

