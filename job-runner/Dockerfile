FROM --platform=linux/amd64 python:3.8-buster as base

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.14

RUN apt-get update
RUN apt-get install -y \ 
software-properties-common make build-essential python3-pip \
python-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev curl libffi-dev graphviz libgraphviz-dev \
libcairo2-dev pkg-config python3-dev python3-pygraphviz apt-utils
# pygraphviz

RUN pip install "poetry==$POETRY_VERSION"

# Project initialization:
RUN poetry config virtualenvs.create false
  

FROM base as runner

WORKDIR /main
ADD ./pyfluigi ./pyfluigi
WORKDIR /main/pyfluigi

RUN poetry install --no-dev --no-interaction --no-ansi 

WORKDIR /runner/
COPY ./job-runner .
RUN pip install .

RUN fluigi --help




