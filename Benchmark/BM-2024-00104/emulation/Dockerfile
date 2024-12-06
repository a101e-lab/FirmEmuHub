FROM fitzbc/fat_ubuntu1604:v6

ADD ./firmware /firmware-analysis-toolkit/firmware.bin
ADD run.sh /firmware-analysis-toolkit/run.sh

WORKDIR /firmware-analysis-toolkit/

RUN apt-get install -y tmux net-tools ssh tcpdump

RUN ssh-keygen -b 2048 -f /root/.ssh/id_rsa -t rsa -q -N "" && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN chmod +x run.sh && sed -i 's/input/print/' ./fat.py

RUN mkdir /pcap

EXPOSE 80
ENTRYPOINT ["./run.sh"]
