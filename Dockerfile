FROM rhel7:latest
MAINTAINER  Andrew Spear andrew.speare@uscellular.com

RUN yum repolist --disablerepo=* && \
    yum-config-manager --enable rhel-7-server-rpms > /dev/null && \
    yum-config-manager --enable rhel-7-server-extras-rpms > /dev/null && \
    yum-config-manager --enable rhel-7-server-optional-rpms > /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum makecache && \
    yum install gcc rh-python36-python rh-python36-python-devel rh-python36-python-pip rh-python36-python-libs rh-python36-python-setuptools -y

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

ENV PYTHON_HOME /opt/rh/rh-python36/root/usr/bin
RUN $PYTHON_HOME/pip install -r /neh_main/requirements.txt

ENV LANG en_US.UTF-8

WORKDIR /neh_main

USER root

CMD ["/opt/rh/rh-python36/root/usr/bin/python", "network_health_main.py" ]
