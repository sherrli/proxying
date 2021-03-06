ARG BASE_IMG

FROM ${BASE_IMG}

RUN apt-get update -qq \
  && apt-get install -y curl \
  && apt-get install -y python3-pip python3-dev \
  && apt-get install -y software-properties-common \
  && apt-get install -y unzip \
  && apt-get install -y wget \
  && apt-get install -y xvfb \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && pip3 install --no-cache-dir requests \
  selenium \
  xvfbwrapper

RUN apt-get install -y firefox
ENV GECKODRIVER_VERSION 0.25.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-${GECKODRIVER_VERSION} \
  && chmod 755 /opt/geckodriver-${GECKODRIVER_VERSION} \
  && ln -fs /opt/geckodriver-${GECKODRIVER_VERSION} /usr/bin/geckodriver \
  && ln -fs /opt/geckodriver-${GECKODRIVER_VERSION} /usr/bin/wires
  
RUN wget -q -O - https://www.charlesproxy.com/packages/apt/PublicKey | apt-key add - \
  && sh -c 'echo deb https://www.charlesproxy.com/packages/apt/ charles-proxy main > /etc/apt/sources.list.d/charles.list' \
  && apt-get update \
  && apt-get install charles-proxy

COPY . /home/ubuntu
WORKDIR /home/ubuntu
