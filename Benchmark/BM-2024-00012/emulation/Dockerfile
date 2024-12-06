FROM fitzbc/fat_ubuntu1604:v6

ADD sources.list /etc/apt/

RUN apt-get update
RUN apt-get install -y apache2 python tmux net-tools ssh tcpdump qemu qemu-user-static qemu-system bridge-utils uml-utilities vim inetutils-ping unzip curl


RUN mkdir /qemu_arm

#ADD ${FIRMWARE_PATH} /qemu_arm/firmware.bin
ADD firmware/tenda_ac9.zip /qemu_arm/firmware.bin
ADD run.sh /qemu_arm/run.sh
ADD interfaces /etc/network/interfaces
ADD qemu-ifup /etc/qemu-ifup

WORKDIR /qemu_arm/

RUN chmod a+x /etc/qemu-ifup

# RUN systemctl restart networking

RUN ssh-keygen -b 2048 -f /root/.ssh/id_rsa -t rsa -q -N "" && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN chmod +x run.sh

RUN mkdir /pcap

EXPOSE 80
ENTRYPOINT ["./run.sh"]