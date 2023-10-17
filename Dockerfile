FROM ubuntu:focal

ARG PYTHON_VERSION=3.9
ARG PYLUCENE_VERSION=9.1.0

# Uncomment to install specific version of poetry
ENV LANG=C.UTF-8

# ADD Python PPA Repository
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        software-properties-common gpg-agent && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get remove -y software-properties-common && \
    apt-get purge --auto-remove -y && \
    apt-get clean

RUN which gpg-agent

# Install Python
RUN apt-get install -y --no-install-recommends \
        "python$PYTHON_VERSION-dev" \
        python3-setuptools \
        python3-pip && \
    apt-get remove -y gpg-agent && \
    apt-get purge --auto-remove -y && \
    apt-get clean

# ======================== START OF ADDITIONAL INSTALLATION ========================

# Install Java
RUN apt-get install -y --no-install-recommends \
    build-essential \
    ant \
    jcc \
    curl \
    git \
    default-jdk 
    
RUN ls /usr/bin/ | grep "python"
RUN ln -s $(which python3.9) /usr/bin/python

RUN which python3.9 && which python && python --version

WORKDIR /usr/lib/jvm/default-java/jre/lib
RUN ln -s ../../lib amd64

# Java 11
RUN java --version && javac --version


# Installing PyLucene
RUN which ant && ant -version

RUN apt-get install -y --no-install-recommends \
    libffi-dev \
    zlib1g-dev

ENV PREFIX_PYTHON=/usr \
    JCC_JDK=/usr/lib/jvm/default-java \
    ANT=ant \
    JCC='python -m jcc' \
    NUM_FILES=10 \
    PYTHON=python \
    NO_SHARED=1

WORKDIR /usr/src/pylucene
RUN curl https://dlcdn.apache.org/lucene/pylucene/pylucene-9.1.0-src.tar.gz | tar -xz

RUN cd "pylucene-$PYLUCENE_VERSION/jcc" && \
    ls -la && \
    NO_SHARED=1 JCC_JDK=/usr/lib/jvm/default-java python setup.py build && \
    NO_SHARED=1 JCC_JDK=/usr/lib/jvm/default-java python setup.py install && \
    cd .. && \
    make JCC="python -m jcc" ANT=ant PYTHON=python NUM_FILES=8&& \
    make install JCC="python -m jcc" ANT=ant PYTHON=python NUM_FILES=8 && \
    cd ../../

RUN apt-get remove -y gpg-agent ant jcc build-essential && \
    apt-get purge --auto-remove -y && \
    apt-get clean

WORKDIR /usr/src
RUN rm -rf pylucene

RUN python -c "import lucene; lucene.initVM()"

# ======================== END OF ADDITIONAL INSTALLATION ========================

WORKDIR /app
COPY . .