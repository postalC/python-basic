FROM python:2.7

MAINTAINER WeiTah CHAI <wei.tah.chai@sap.com>

LABEL copy-right="SAP MLI SG"
LABEL repo-name="sbc-base"
LABEL version="0.1"
LABEL description="Social Buzz Clustering Backend Setup Images"

ENV http_proxy http://proxy.wdf.sap.corp:8080
ENV https_proxy http://proxy.wdf.sap.corp:8080
ENV no_proxy sap.corp,wdf.sap.corp,localhost,127.0.0.1,moo-repo,169.254.169.254,repo

RUN mkdir -p /opt/sbc
WORKDIR /opt/sbc

RUN \
 apt-get update && \
 apt-get install -y build-essential \
 python-dev python-setuptools \
 python-numpy python-scipy \
 libatlas-dev libatlas3gf-base \
 libopenblas-dev gfortran

RUN update-alternatives --set libblas.so.3 \
 /usr/lib/atlas-base/atlas/libblas.so.3
RUN update-alternatives --set liblapack.so.3 \
 /usr/lib/atlas-base/atlas/liblapack.so.3

COPY requirements.txt /opt/sbc/
RUN pip install --proxy proxy.wdf.sap.corp:8080 --no-cache-dir -r requirements.txt
COPY project/ /opt/sbc

CMD [ "python", "server.py" ]
