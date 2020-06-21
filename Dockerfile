FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y python3 python3-pip wget && \
    wget -q https://www.princexml.com/download/prince_13.5-1_ubuntu18.04_amd64.deb && \
    apt install -y ./prince_13.5-1_ubuntu18.04_amd64.deb && \
    rm prince_13.5-1_ubuntu18.04_amd64.deb && \
    pip3 install dominate pillow python-barcode pyaml && \
    mkdir /data
ADD barc.py /barc.py
ADD run-barc.sh /run-barc.sh
ADD style /style
WORKDIR /data
CMD /run-barc.sh
