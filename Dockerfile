FROM ubuntu:18.04

RUN apt-get update -qq \
  && apt-get install -y curl \
  && apt-get install -y python3-pip python3-dev \
  && apt-get install -y software-properties-common \
  && apt-get install -y unzip \
  && apt-get install -y wget \
  && apt-get install -y xvfb \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN wget -q -O - https://www.charlesproxy.com/packages/apt/PublicKey | apt-key add - \
  && sh -c 'echo deb https://www.charlesproxy.com/packages/apt/ charles-proxy main > /etc/apt/sources.list.d/charles.list' \
  && apt-get update \
  && apt-get install charles-proxy

COPY charles /home/ubuntu
WORKDIR /home/ubuntu
