#! /usr/bin/env bash

#=============================================
# Script Name: tstack_process_check
#      Author: Wenger Chan
#     Version: V 1.0
#        Date: 2021-04-09
# Description: Check information of Tstack
#=============================================

# 1、检查中间件和数据库
source /root/keystonerc_admin

## rabbitmq集群状态：rabbitmqctl cluster_status
read rabbitmq_running_nodes rabbitmq_partitions < <(rabbitmqctl cluster_status 2>/dev/null | \
    sed 's/[[:space:]]*//g' | sed ':label;N;s/\n/;/g;b label' | \
    grep -aPo '((?<=running_nodes,)\[.*\](?=\}\,\{cluster_name))|((?<=partitions,)\[.*\](?=\}\,\{alarms))')

## MySQL数据库状态：mysql -uroot -p -e show status like ‘%wsrep%’;
read wsrep_cluster_size wsrep_incoming_addresses < <(mysql -uroot -e "show status like '%wsrep%';" 2>/dev/null | \
    grep -E 'wsrep_cluster_size|wsrep_incoming_addresses' | \
    awk '{print $NF}')

# 2、检查openstack服务
## OpenStack nova服务状态：nova service-list（所有state状态up）

## OpenStack neutron服务状态：neutron agent-list(alive笑脸，没有显示xxx)
## OpenStack cinder服务状态：cinder service-list（state状态up）