## Cluster configuration file locations:

Redhat Cluster Releases	|Configuration files | Description
--|--|--
Prior to Redhat Cluster 7 | /etc/cluster/cluster.conf | Stores all the configuration of cluster
Redhat Cluster 7 (RHEL 7) | /etc/corosync/corosync.conf | Membership and Quorum configuration
Redhat Cluster 7 (RHEL 7) | /var/lib/heartbeat/crm/cib.xml | Cluster node and Resource configuration.

## Commands:

Configuration Method | Prior to Redhat Cluster 7 | Redhat Cluster 7 (RHEL 7)
--|--|--
Command Line utiltiy | ccs | pcs
GUI tool | luci | PCSD – Pacemaker Web GUI Utility

## Services:

Redhat Cluster Releases | Services | Description
--|--|--
Prior to Redhat Cluster 7 | rgmanager	 | Cluster Resource Manager
Prior to Redhat Cluster 7 | cman	     | Manages cluster quorum and cluster membership.
Prior to Redhat Cluster 7 | ricci	     | To provide access to luci web-Interface.
Redhat Cluster 7 (RHEL 7) | pcsd.service | Cluster  Resource Manager
Redhat Cluster 7 (RHEL 7) | corosync.service | Manages cluster quorum and cluster membership.

## Cluster user:

User Access	| Prior to Redhat Cluster 7 | Redhat Cluster 7 (RHEL 7)
--|--|--
Cluster user name | ricci | hacluster

## How simple to create a cluster on RHEL 7 ?

Redhat Cluster Releases | Cluster Creation | Description
--|--|--
Prior to Redhat Cluster 7 | `ccs -h node1.ua.com –createcluster uacluster` | Create cluster on first node using ccs
Prior to Redhat Cluster 7 | `ccs -h node1.ua.com –addnode node2.ua.com` | Add the second node  to the existing cluster
Redhat Cluster 7 (RHEL 7) | `pcs cluster setup uacluster node1 node2` | Create a cluster on both the nodes using pcs

## Is there any pain to remove a cluster in RHEL 7 ?  No. It’s very simple.

Redhat Cluster Releases | Remove Cluster | Description
--|--|--
Prior to Redhat Cluster 7 | `rm /etc/cluster/cluster.conf` | Remove the cluster.conf file on each cluster nodes
Prior to Redhat Cluster 7 | `service rgmanager stop`<br>`service cman stop`<br> `service ricci stop` | Stop the cluster services on each cluster nodes
Prior to Redhat Cluster 7 | `chkconfig rgmanager off`<br> `chkconfig cman of`<br>`chkconfig ricci off`| Disable the cluster services from startup
Redhat Cluster 7 (RHEL 7) | `pcs cluster destroy` | Destroy the cluster in one-shot using pacemaker
