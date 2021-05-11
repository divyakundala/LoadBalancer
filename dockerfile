FROM ubuntu

MAINTAINER divya kundala

RUN apt-get update
RUN apt-get -y --force-yes install iproute2
RUN apt-get -y --force-yes install curl
RUN apt-get -y --force-yes install telnet
RUN apt-get -y --force-yes install openssh-server
RUN apt-get -y --force-yes install iptables
RUN apt-get -y --force-yes install iputils-ping
RUN apt-get -y --force-yes install traceroute
RUN apt-get -y --force-yes install tcpdump
RUN apt-get -y --force-yes install iperf
RUN apt-get -y --force-yes install vim
RUN apt-get -y --force-yes install python3
RUN apt-get -y --force-yes install python3-pip
RUN apt-get -y --force-yes install python3-pexpect
RUN pip3 install paramiko
RUN apt-get -y --force-yes install nano

RUN apt-get -y --force-yes install libc-ares2
RUN apt-get -y --force-yes install libpci3
RUN apt-get -y --force-yes install libsnmp-base




RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump
RUN ln -s /usr/bin/tcpdump /usr/sbin/tcpdump

RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config



