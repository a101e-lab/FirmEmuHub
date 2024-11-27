#!/bin/sh

service ssh start 
cd /firmware-analysis-toolkit/
# 获取容器IP地址
local_ip=`ifconfig eth0 | grep "inet addr:" | awk '{print $2}' | cut -c 6-`
local_port=80

# 获取仿真服务IP地址
if [ -z "$REMOTE_IP" ]; then
    # 如果为空，则设置默认值
    remote_ip='192.168.0.1'
else
    remote_ip=${REMOTE_IP}
fi

# 获取仿真服务端口
if [ -z "$REMOTE_PORT" ]; then
    # 如果为空，则设置默认值
    remote_port=80
else
    remote_port=${REMOTE_PORT}
fi


# 创建后台端口转发进程
tmux new -s "local" -d "for i in {1..10} ;do ssh -L ${local_ip}:${local_port}:${remote_ip}:${remote_port} root@${local_ip} -o ConnectTimeout=10 -o StrictHostKeyChecking=no; echo $i; echo 'restart'; sleep 10s ;done"

# tap_name=$(ip link show |awk '{ if(match($0,"tap")) { print substr($0,4,6) }}')
# # 创建后台抓包进程
# tmux new -s "capture_before_pcap" -d "for i in {1..10} ;do tcpdump -i $tap_name -s 0 -w pcap/before.pcap; echo $i; echo 'restart'; sleep 10s ;done"

# 进行仿真
./fat.py firmware.bin
