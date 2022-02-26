# virt-install






```sh
~] virt-install --help

usage: virt-install --name NAME --memory MB STORAGE INSTALL [options]

Create a new virtual machine from specified install media.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program''s version number and exit 
  --connect URI         Connect to hypervisor with libvirt URI

General Options:
  -n NAME, --name NAME  Name of the guest instance
  --memory MEMORY       Configure guest memory allocation. Ex:
                        --memory 1024 (in MiB)
                        --memory memory=1024,currentMemory=512
  --vcpus VCPUS         Number of vcpus to configure for your guest. Ex:
                        --vcpus 5
                        --vcpus 5,maxvcpus=10,cpuset=1-4,6,8
                        --vcpus sockets=2,cores=4,threads=2
  --cpu CPU             CPU model and features. Ex:
                        --cpu coreduo,+x2apic
                        --cpu host-passthrough
                        --cpu host
  --metadata METADATA   Configure guest metadata. Ex:
                        --metadata name=foo,title="My pretty title",uuid=...
                        --metadata description="My nice long description"

Installation Method Options:
  --cdrom CDROM         CD-ROM installation media
  -l LOCATION, --location LOCATION
                        Distro install URL, eg. https://host/path. See man
                        page for specific distro examples.
  --pxe                 Boot from the network using the PXE protocol
  --import              Build guest around an existing disk image 在已有的磁盘镜像中构建客户机
  -x EXTRA_ARGS, --extra-args EXTRA_ARGS
                        Additional arguments to pass to the install kernel
                        booted from --location
  --initrd-inject INITRD_INJECT
                        Add given file to root of initrd from --location
  --unattended [UNATTENDED]
                        Perform an unattended installation
  --install INSTALL     Specify fine grained install options
  --boot BOOT           Configure guest boot settings. Ex:
                        --boot hd,cdrom,menu=on
                        --boot init=/sbin/init (for containers)
  --idmap IDMAP         Enable user namespace for LXC container. Ex:
                        --idmap uid.start=0,uid.target=1000,uid.count=10

OS options:
  --os-variant OS_VARIANT
                        The OS being installed in the guest.
                        This is used for deciding optimal defaults like virtio.
                        Example values: fedora29, rhel7.0, win10, ...
                        See 'osinfo-query os' for a full list.

Device Options:
  --disk DISK           Specify storage with various options. Ex.
                        --disk size=10 (new 10GiB image in default location)
                        --disk /my/existing/disk,cache=none
                        --disk device=cdrom,bus=scsi
                        --disk=?
  -w NETWORK, --network NETWORK
                        Configure a guest network interface. Ex:
                        --network bridge=mybr0
                        --network network=my_libvirt_virtual_net
                        --network network=mynet,model=virtio,mac=00:11...
                        --network none
                        --network help
  --graphics GRAPHICS   Configure guest display settings. Ex:
                        --graphics spice
                        --graphics vnc,port=5901,listen=0.0.0.0
                        --graphics none
  --controller CONTROLLER
                        Configure a guest controller device. Ex:
                        --controller type=usb,model=qemu-xhci
                        --controller virtio-scsi
  --input INPUT         Configure a guest input device. Ex:
                        --input tablet
                        --input keyboard,bus=usb
  --serial SERIAL       Configure a guest serial device
  --parallel PARALLEL   Configure a guest parallel device
  --channel CHANNEL     Configure a guest communication channel
  --console CONSOLE     Configure a text console connection between the guest
                        and host
  --hostdev HOSTDEV     Configure physical USB/PCI/etc host devices to be
                        shared with the guest
  --filesystem FILESYSTEM
                        Pass host directory to the guest. Ex: 
                        --filesystem /my/source/dir,/dir/in/guest
                        --filesystem template_name,/,type=template
  --sound [SOUND]       Configure guest sound device emulation
  --watchdog WATCHDOG   Configure a guest watchdog device
  --video VIDEO         Configure guest video hardware.
  --smartcard SMARTCARD
                        Configure a guest smartcard device. Ex:
                        --smartcard mode=passthrough
  --redirdev REDIRDEV   Configure a guest redirection device. Ex:
                        --redirdev usb,type=tcp,server=192.168.1.1:4000
  --memballoon MEMBALLOON
                        Configure a guest memballoon device. Ex:
                        --memballoon model=virtio
  --tpm TPM             Configure a guest TPM device. Ex:
                        --tpm /dev/tpm
  --rng RNG             Configure a guest RNG device. Ex:
                        --rng /dev/urandom
  --panic PANIC         Configure a guest panic device. Ex:
                        --panic default
  --memdev MEMDEV       Configure a guest memory device. Ex:
                        --memdev dimm,target.size=1024
  --vsock VSOCK         Configure guest vsock sockets. Ex:
                        --vsock cid.auto=yes
                        --vsock cid.address=7

Guest Configuration Options:
  --iothreads IOTHREADS
                        Set domain <iothreads> and <iothreadids>
                        configuration.
  --seclabel SECLABEL, --security SECLABEL
                        Set domain seclabel configuration.
  --cputune CPUTUNE     Tune CPU parameters for the domain process.
  --numatune NUMATUNE   Tune NUMA policy for the domain process.
  --memtune MEMTUNE     Tune memory policy for the domain process.
  --blkiotune BLKIOTUNE
                        Tune blkio policy for the domain process.
  --memorybacking MEMORYBACKING
                        Set memory backing policy for the domain process. Ex:
                        --memorybacking hugepages=on
  --features FEATURES   Set domain <features> XML. Ex:
                        --features acpi=off
                        --features apic=on,apic.eoi=on
  --clock CLOCK         Set domain <clock> XML. Ex:
                        --clock offset=localtime,rtc_tickpolicy=catchup
  --pm PM               Configure VM power management features
  --events EVENTS       Configure VM lifecycle management policy
  --resource RESOURCE   Configure VM resource partitioning (cgroups)
  --sysinfo SYSINFO     Configure SMBIOS System Information. Ex:
                        --sysinfo host
                        --sysinfo bios.vendor=MyVendor,bios.version=1.2.3,...
  --qemu-commandline QEMU_COMMANDLINE
                        Pass arguments directly to the qemu emulator. Ex:
                        --qemu-commandline='-display gtk,gl=on'
                        --qemu-commandline env=DISPLAY=:0.1
  --launchSecurity LAUNCHSECURITY, --launchsecurity LAUNCHSECURITY
                        Configure VM launch security (e.g. SEV memory encryption). Ex:
                        --launchSecurity type=sev,cbitpos=47,reducedPhysBits=1,policy=0x0001,dhCert=BASE64CERT
                        --launchSecurity sev

Virtualization Platform Options:
  -v, --hvm             This guest should be a fully virtualized guest
  -p, --paravirt        This guest should be a paravirtualized guest
  --container           This guest should be a container guest
  --virt-type VIRT_TYPE
                        Hypervisor name to use (kvm, qemu, xen, ...)
  --arch ARCH           The CPU architecture to simulate
  --machine MACHINE     The machine type to emulate

Miscellaneous Options:
  --autostart           Have domain autostart on host boot up.
  --transient           Create a transient domain.
  --destroy-on-exit     Force power off the domain when the console viewer is
                        closed.
  --wait [WAIT]         Minutes to wait for install to complete.
  --noautoconsole       Don't automatically try to connect to the guest
                        console
  --noreboot            Don't boot guest after completing install.
  --print-xml [XMLONLY]
                        Print the generated domain XML rather than create the
                        guest.
  --dry-run             Run through install process, but do not create devices
                        or define the guest.
  --check CHECK         Enable or disable validation checks. Example:
                        --check path_in_use=off
                        --check all=off
  -q, --quiet           Suppress non-error output
  -d, --debug           Print debugging information

Use '--option=?' or '--option help' to see available suboptions
See man page for examples and full option syntax.
```





* The simplest invocation to interactively install a Fedora 29 KVM VM with recommended defaults. virt-viewer(1) will be launched to graphically interact with the VM install:

> Note: 启动virt-viewer图形窗口安装; 此操作需要安装virt-viewer; 

    ```sh
    sudo virt-install --install fedora29

    # 'fedora29' 为操作系统类型, 可通过 'osinfo-query os' 查询支持的选项
    ```

* Similar, but use libosinfo's unattended install support, which will perform the fedora29 install automatically without user intervention:

> Note: 使用 libosinfo 无人值守安装

    ```sh
    sudo virt-install --install fedora29 --unattended
    ```

* Install a Windows 10 VM, using 40GiB storage in the default location and 4096MiB of ram, and ensure we are connecting to the system libvirtd instance:

    ```sh
    virt-install \
        --connect qemu:///system \
        --name my-win10-vm \
        --memory 4096 \
        --disk size=40 \
        --os-variant win10 \
        --cdrom /path/to/my/win10.iso
    ```

* Install a CentOS 7 KVM from a URL, with recommended device defaults and default required storage, but specifically request VNC graphics instead of the default SPICE, and request 8 virtual CPUs and 8192 MiB of memory:

    ```sh
    virt-install \
              --connect qemu:///system \
              --memory 8192 \
              --vcpus 8 \
              --graphics vnc \
              --os-variant centos7.0 \
              --location http://mirror.centos.org/centos-7/7/os/x86_64/
    ```

* Create a VM around an existing debian9 disk image:

    ```sh
    virt-install \
              --import \
              --memory 512 \
              --disk /home/user/VMs/my-debian9.img \
              --os-variant debian9
    ```

