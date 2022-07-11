#Dockerized Fluigi Cloud
FROM ubuntu:trusty

MAINTAINER Priya Kapadia <priyak@bu.edu>

ENV java_version 1.8.0_51
ENV filename jdk-8u51-linux-x64.tar.gz
ENV JAVA_HOME /opt/java-oracle/jdk$java_version
ENV PATH $JAVA_HOME/bin:$PATH

RUN apt-get update; \
  apt-get install -y git curl; \
  curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -; \
  curl https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - ; \
  sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'; \
  apt-get update && apt-get install -y google-chrome-stable nodejs Xvfb; \
  wget --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u51-b16/$filename -O /tmp/$filename --progress=bar:force; \
  mkdir -p /opt/java-oracle && tar -zxf /tmp/$filename -C /opt/java-oracle/;  \
  update-alternatives --install /usr/bin/java java $JAVA_HOME/bin/java 20000; \
  update-alternatives --install /usr/bin/javac javac $JAVA_HOME/bin/javac 20000; \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD xvfb.sh /etc/init.d/xvfb
ADD entrypoint.sh /entrypoint.sh

ENV DISPLAY :99.0
ENV CHROME_BIN /usr/bin/google-chrome

#Install dependencies
ADD package.json package.json
RUN npm install

#Add to working directory
ADD . .

#Set startup command
CMD [ "npm", "start" ]
