# develop stage
FROM node:latest as vue-develop-stage
WORKDIR /app
COPY ./Neptune-UI/package*.json ./
RUN yarn install
COPY ./Neptune-UI/ .

# build stage
FROM vue-develop-stage as vue-build-stage
RUN yarn build

#develop stage for python binarries
FROM ubuntu:18.04 as lfr-develop-stage

RUN apt-get -y update
RUN apt-get install -y build-essential
RUN apt-get -y install software-properties-common

RUN apt-get -y update
RUN apt-get install -y python3-pip
RUN apt-get install -y graphviz libgraphviz-dev
RUN pip3 install pipenv

#Install pyLFR
WORKDIR /pyLFR
COPY ./pyLFR ./

RUN pip3 install -r requirements.txt

#build stage for python binaries
FROM lfr-develop-stage as lfr-build-stage

RUN pyinstaller cmdline.py --onefile



FROM ubuntu:18.04 as deployment

RUN apt-get -y update
RUN apt-get install -y curl
RUN apt-get install -y build-essential
RUN apt-get -y install software-properties-common

# RUN add-apt-repository ppa:openjdk-r/ppa
# RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get -y update

#Remove this later on
RUN apt-get -y install redis-server

# Installing Nodejs
RUN curl -sL --location https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get -y install nodejs

#installing Java
RUN apt-get install -y openjdk-8-jre-headless

# # Installing python
# RUN apt-get -y install python3.7

#Installing forever
RUN npm install forever -g

WORKDIR /var/www/fluigicad.org/

#Install dependencies
ADD Fluigi-Cloud/package.json package.json
RUN npm install

#Add to working directory
ADD ./Fluigi-Cloud/ .

#Modify the permissions so that we can create the job files
RUN chown -R $USER:$GROUP ./jobs/

#Copy Neptune-UI
COPY --from=vue-build-stage /app/dist ./dist/


#Install LFR Dependencies
RUN apt-get install -y graphviz libgraphviz-dev

#Copy pyLFR
COPY --from=lfr-build-stage /pyLFR/dist/cmdline ./jobs/pyLFR/

ADD start.sh .

EXPOSE 3000
EXPOSE 8080
CMD ["sh", "start.sh"]





