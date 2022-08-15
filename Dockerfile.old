# develop stage
# FROM node:latest as vue-develop-stage
# WORKDIR /app
# COPY ./Neptune-UI/package*.json ./
# RUN yarn install
# COPY ./Neptune-UI/ .

# # build stage
# FROM vue-develop-stage as vue-build-stage
# RUN yarn build

#develop stage for python binarries
# FROM ubuntu:20.04 as lfr-develop-stage
# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get -y update
# RUN apt-get install -y build-essential
# RUN apt-get -y install software-properties-common curl

# RUN apt-get -y update
# RUN apt-get install -y python3-pip
# RUN apt-get install -y graphviz libgraphviz-dev
# # RUN pip3 install pipenv

# # RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
# # RUN /bin/bash -c "source $HOME/.poetry/env"
# # ENV PATH="${PATH}:/root/.poetry/bin"

# #Install pyLFR
# # WORKDIR /pyLFR
# # COPY ./pyLFR ./

# # RUN poetry build

# #build stage for python binaries
# FROM lfr-develop-stage as lfr-build-stage

# RUN pyinstaller cmdline.py --onefile



FROM ubuntu:20.04 as deployment
ARG DEBIAN_FRONTEND=noninteractive

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
RUN apt install -y curl
RUN apt-get install -y build-essential
RUN apt-get -y install software-properties-common

RUN apt-get install -y python3-pip  git make build-essential \
python-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev curl libffi-dev graphviz libgraphviz-dev \
libcairo2-dev pkg-config python3-dev

# Installing Nodejs
RUN curl -sL --location https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get -y install nodejs

# Pyenv for our baseline python environment for poetry later on.
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.8.0
RUN pyenv global 3.8.0

RUN pip install --upgrade pip
RUN pip install setuptools pygraphviz

WORKDIR /pybin

RUN apt install -y 

WORKDIR /pybin

# TODO - Modify this to just pull the packages from pypi
ADD ./pyfluigi ./pyfluigi

WORKDIR /pybin/pyfluigi

RUN chmod +x ./bin/place_and_route

RUN pwd
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip install .

RUN fluigi --help

WORKDIR /var/www/fluigicad.org/

#Install dependencies
ADD Fluigi-Cloud/package.json package.json
RUN npm install

#Add to working directory
ADD ./Fluigi-Cloud/ .

#Modify the permissions so that we can create the job files
RUN chown -R $USER:$GROUP ./jobs/

#Copy Neptune-UI
# COPY --from=vue-build-stage /app/dist ./dist/
ADD ./Neptune-UI/dist/ ./dist/

ADD start.sh .

EXPOSE 3000
EXPOSE 8080
CMD ["sh", "start.sh"]





