#!/bin/bash
# filename: ltpstress_config.sh
# Author: lufei
# Date: 20191011 17:53:15
# for ltpstress running configuration.



url="http://192.168.45.37:8000/sw_64/ltp-20180926-1.isoft.sw_64.rpm"
yum install -y $url

setup(){

    yum install numactl numactl-devel \
        gcc expect mkisofs libaio libaio-devel \
        libcap-devel libattr-devel keyutils-libs-devel \
        rsh rsh-server -y

    [ -f /bin/exportfs ] || ln /usr/sbin/exportfs /bin/
    [ -f /bin/rpc.nfsd ] || ln /usr/sbin/rpc.nfsd /bin/

##  services configration
    echo -ne 'rsh\nrlogin\nrexec' >> /etc/securetty
    echo localhost >> /root/.rhosts
    systemctl start rsh.socket
    systemctl start rlogin.socket
    systemctl start nfs
    systemctl stop firewalld
    systemctl disable firewalld
    systemctl enable rsh.socket
    systemctl enable rlogin.socket
    systemctl enable nfs
}


setup


