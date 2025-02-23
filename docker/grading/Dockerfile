FROM ubuntu:22.04

WORKDIR /app

RUN sed -i "s@http://.*.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
RUN apt-get update && \
    apt-get install -y make g++ git bison flex ccache zip verilator iverilog python3  && \
    apt-get clean

COPY var/labs /app

RUN mkdir -p /scripts
COPY docker/grading/grading.sh /scripts/grading.sh

CMD [ "bash" ]
