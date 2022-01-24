## 1.1 OracleServiceORCL(必须启动)

OracleServiceORCL：数据库服务(数据库实例)，是 Oracle 核心服务该服务是数据库启动的基础，只有该服务启动，Oracle 数据库才能正常启动。

## 1.2 OracleOraDb11g_home1TNSListener(必须启动)

OracleOraDb11g_home1TNSListener：监听器服务，服务只有在数据库需要远程访问的时候 或者使用 PL/SQL Developer 等第三方工具时才需要。

## 1.3 OracleORCLVSSWriterService(非必须启动)

Oracle ORCLVSS Writer Service：Oracle 卷映射拷贝写入服务，VSS(Volume Shadow Copy Service)能够让存储基础设备(比如磁盘，阵列等)创建高保真的时间点映像，即映射拷贝 (shadow copy)。它可以在多卷或者单个卷上创建映射拷贝，同时不会影响到系统的系统能。

## 1.4 OracleDBConsoleorcl(非必须启动)

OracleDBConsoleorcl：Oracle 数据库控制台服务，orcl 是 Oracle 的实例标识，默认的实例为 orcl。在运行 Enterprise Manager(企业管理器 OEM)的时候，需要启动这个服务。

## 1.5 OracleJobSchedulerORCL(非必须启动)

OracleJobSchedulerORCL：Oracle 作业调度(定时器)服务，ORCL 是 Oracle 实例标识。

## 1.6 OracleMTSRecoveryService(非必须启动)

OracleMTSRecoveryService：服务端控制。该服务允许数据库充当一个微软事务服务器 MTS、COM/COM+对象和分布式环境下的事务的资源管理器。