FROM centos:7
MAINTAINER  Andrew Spear andrew.speare@uscellular.com

RUN yum -y install epel-release
RUN yum -y install python36 python36-devel python36-pip
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && clean all
COPY localpkgs/* /tmp/
RUN yum -y localinstall --nogpgcheck /tmp/*

RUN mkdir -p /neh_main
RUN mkdir -p /neh_main/common

ADD common/common.py /neh_main/common/
ADD network_health_main.py /neh_main/
ADD requirements.txt /neh_main/

ADD oracle.conf /etc/ld.so.conf.d

RUN cd /usr/lib64 && \
    ln -s libodbcinst.so.2.0.0 libodbcinst.so.1 && \
    ldconfig

RUN pip3.6 install -r /neh_main/requirements.txt

ENV LANG en_US.UTF-8

WORKDIR /neh_main

USER root

CMD ["python3", "network_health_main.py"]
