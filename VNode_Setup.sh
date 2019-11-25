#!/bin/bash

sudo yum install wget;
sudo yum install unzip;
wget https://github.com/PBSPro/pbspro/releases/download/v18.1.3/pbspro_18.1.3.centos7.zip;
unzip pbspro_18.1.3.centos7.zip;
rm -rf pbspro_18.1.3.centos7.zip;
cp pbspro_18.1.3.centos7/pbspro-execution-18.1.3-0.x86_64.rpm ~;
yum install pbspro-execution-18.1.3-0.x86_64.rpm;
sed -i 's/CHANGE_THIS_TO_PBS_PRO_SERVER_HOSTNAME/cluster/g' /etc/pbs.conf;
sed -i 's/CHANGE_THIS_TO_PBS_PRO_SERVER_HOSTNAME/cluster/g' /var/spool/pbs/mom_priv/config;
echo "Please enter the IP Address of your server for configuring /etc/hosts on execution node"
read response1
echo "Please enter the hostname of your server for configuring /etc/hosts on execution node"
read response2
echo $response1 $response2 >> /etc/hosts
a=$(hostname -I | awk '{print $1}')
b=$(hostname | cut -d '.' -f 1)
echo $a $b >> /etc/hosts
/etc/init.d/pbs start
exit