# develop stage
FROM node:latest as vue-develop-stage
WORKDIR /app
COPY ./Neptune-UI/package*.json ./
RUN yarn install
COPY ./Neptune-UI/ .

# build stage
FROM vue-develop-stage as vue-build-stage
RUN yarn build




FROM ubuntu:trusty as deployment


RUN apt-get -y update
RUN apt-get install -y curl
RUN apt-get install -y build-essential
RUN apt-get -y install software-properties-common

RUN add-apt-repository ppa:openjdk-r/ppa
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get -y update

# Installing Nodejs
RUN curl -sL --location https://deb.nodesource.com/setup_13.x | sudo bash -
RUN apt-get -y install nodejs

#installing Java
RUN apt-get install -y openjdk-8-jre-headless

# Installing python
RUN apt-get -y install python3.7

#Installing forever
RUN npm install forever -g

#Install dependencies
ADD Fluigi-Cloud/package.json package.json
RUN npm install
#Add to working directory
ADD ./Fluigi-Cloud/ .

#Copy Neptune-UI
COPY --from=vue-build-stage /app/dist ./dist/

EXPOSE 3000
EXPOSE 8080
CMD ["npm", "start", "app.js"]





