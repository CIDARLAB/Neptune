FROM --platform=linux/amd64 python:3.8-buster as runner

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
RUN apt-get install -y \ 
software-properties-common make build-essential python3-pip \
python-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev curl libffi-dev graphviz libgraphviz-dev \
libcairo2-dev pkg-config python3-dev \
graphviz libgraphviz-dev
#python3-pygraphviz pygraphviz




RUN pip install -U celery

WORKDIR /main
ADD ./pyfluigi ./pyfluigi
RUN pip install ./pyfluigi/pylfr
RUN pip install ./pyfluigi

WORKDIR /runner/
# ADD ./job-runner /main/runner
COPY ./job-runner /runner/
RUN pip install .

# RUN pip install



RUN fluigi --help




