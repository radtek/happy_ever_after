# Parted

## Warning: The resulting partition is not properly aligned for best performance.

由于在分区时起始扇区设置不合理，导致了出现这样的警告. 只是个警告，但是事关性能的问题.

如何设定这个起始扇区的位置?

```sh
~] cat /sys/block/sdb/queue/optimal_io_size
1048576

~] cat /sys/block/sdb/queue/minimum_io_size
262144

~] cat /sys/block/sdb/alignment_offset
0

~] cat /sys/block/sdb/queue/physical_block_size
512
```

* 如果 `optimal_io_size` 不为 0，

`(optimal_io_size + alignment_offset) / physical_block_size` 为起始扇区的位置了，如上面的例子中，可以用这个公式算出来起始扇区的设定值：

```bc
(1048576 + 0) / 512 = 2048
```

* 如果 `optimal_io_size` 为 0，那么我们最好直接使用起始扇区的默认值2048。


最后在分区的时候使用以下的命令就可以了：

```sh
mkpart primary 2048s 100%   # <= 注意: "2048s" 后有个 "s"
```