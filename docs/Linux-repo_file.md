## Red Hat Enterprise Linux

* 6.4

    ```conf
    [RHEL64-HighAvailability]
    name=RHEL64-HighAvailability
    enabled=1
    baseurl=http://192.168.1.1/RHEL64/HighAvailability
    gpgcheck=0

    [RHEL64-LoadBalancer]
    name=RHEL64-LoadBalancer
    enabled=1
    baseurl=http://192.168.1.1/RHEL64/LoadBalancer
    gpgcheck=0

    [RHEL64-ResilientStorage]
    name=RHEL64-ResilientStorage
    enabled=1
    baseurl=http://192.168.1.1/RHEL64/ResilientStorage
    gpgcheck=0

    [RHEL64-ScalableFileSystem]
    name=RHEL64-ScalableFileSystem
    enabled=1
    baseurl=http://192.168.1.1/RHEL64/ScalableFileSystem
    gpgcheck=0

    [RHEL64-Server]
    name=RHEL64-Server
    enabled=1
    baseurl=http://192.168.1.1/RHEL64/Server
    gpgcheck=0

    [RHEL64]
    name=RHEL64
    enabled=1
    baseurl=http://192.168.1.1/RHEL64
    gpgcheck=0
    ```

* 7.9

    ```conf
    [RHEL79-addons-HighAvailability]
    name=RHEL79-addons-HighAvailability
    enabled=1
    baseurl=http://192.168.1.1/RHEL79/addons/HighAvailability
    gpgcheck=0

    [RHEL79-addons-ResilientStorage]
    name=RHEL79-addons-ResilientStorage
    enabled=1
    baseurl=http://192.168.1.1/RHEL79/addons/ResilientStorage
    gpgcheck=0

    [RHEL79]
    name=RHEL79
    enabled=1
    baseurl=http://192.168.1.1/RHEL79
    gpgcheck=0
    ```

* 8.3

    ```conf
    [RHEL83-BaseOS]
    name=RHEL83-BaseOS
    enabled=1
    baseurl=http://192.168.1.1/RHEL83/BaseOS
    gpgcheck=0

    [RHEL83-AppStream]
    name=RHEL83-AppStream
    enabled=1
    baseurl=http://192.168.1.1/RHEL83/AppStream
    gpgcheck=0

    ```

* 5.11

    ```conf
    [RHEL511-Cluster]
    name=RHEL511-Cluster
    enabled=1
    baseurl=http://192.168.1.1/RHEL511/Cluster
    gpgcheck=0

    [RHEL511-ClusterStorage]
    name=RHEL511-ClusterStorage
    enabled=1
    baseurl=http://192.168.1.1/RHEL511/ClusterStorage
    gpgcheck=0

    [RHEL511-Server]
    name=RHEL511-Server
    enabled=1
    baseurl=http://192.168.1.1/RHEL511/Server
    gpgcheck=0

    [RHEL511-VT]
    name=RHEL511-VT
    enabled=1
    baseurl=http://192.168.1.1/RHEL511/VT
    gpgcheck=0
    ```