FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y python3 python3-pip wget && \
    wget -q https://www.princexml.com/download/prince_13.5-1_ubuntu18.04_amd64.deb && \
    apt install -y ./prince_13.5-1_ubuntu18.04_amd64.deb && \
    rm prince_13.5-1_ubuntu18.04_amd64.deb && \
    pip3 install dominate pillow python-barcode pyaml && \
    mkdir /data
ADD style /style
ADD examples /examples
ADD README.md /install/README.md
ADD setup.py /install/setup.py
ADD barc /install/barc
RUN cd /install && \
    python3 setup.py install && \
    cd / && \
    rm -rf /install
