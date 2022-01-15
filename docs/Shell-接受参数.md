## 接受参数

```sh
while getopts "t:a:u:h" opt
do
   case "$opt" in
      t ) TOKEN="$OPTARG" ;;
      a ) ACCOUNT_TYPE="$OPTARG" ;;
      u ) ACCOUNT_NAME="$OPTARG" ;;
      h ) help ;;
      ? ) help ;;
   esac
done
```

```sh
usage() {

cat <<EOF

rh_iso_extract.sh [ options ]

Valid options are:
	-h | --help	This help
	-a | --arch	The architecture to work with [ default i386 ]
	-d | --dest-dir	The destination dir prefix    [ default /var/ftp ]
	-i | --iso-dir	The source iso dir prefix     [ default /var/ftp ]
	-r | --release  The release name              [ default beta/null ]

If you cannot loop mount a file on an NFS filesystem,
e.g. 2.2.x kernel based systems, you should copy your
iso images to a local directory and override the iso-dir
and dest-dir defaults.

e.g.
   # mkdir -p /mnt/scratch/ftp/pub/redhat/linux/RELEASE/en/iso/i386/

   # cp /var/ftp/pub/redhat/linux/RELEASE/en/iso/i386/*.iso \\
              /mnt/scratch/ftp/pub/redhat/linux/RELEASE/en/iso/i386/

   # rh_iso_extract.sh -i /mnt/scratch/ftp/pub -d /var/ftp/pub

EOF
exit 1
}

TEMP=`getopt -o ha:d:i:r: --long help,arch:,dest-dir:,iso-dir:,release: -n 'rh_iso_extract.sh' -- "$@"`

eval set -- "$TEMP"

while true ; do
	case "$1" in 
		-h|--help) usage ;;
		-a|--arch)
			ARCH=$2
			shift 2
			;;
		-d|--dest-dir) 
			DESTPREFIX=$2
			shift 2
			;;
		-i|--iso-dir) 
			ISOPREFIX=$2
			shift 2
			;;
		-r|--release) 
			RELEASE=$2
			shift 2
			;;
		--) shift ; break;;
		*) echo "Internal error!" ; exit 1;;
	esac
done
```