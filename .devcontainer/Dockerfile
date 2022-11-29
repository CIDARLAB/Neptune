# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.194.3/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: hirsute, bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.14


# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl build-essential \
      software-properties-common python3-pip make build-essential \
      python-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
      libsqlite3-dev curl libffi-dev redis-server openjdk-8-jre-headless \
      graphviz libgraphviz-dev libcairo2-dev pkg-config python3-dev python3.8-venv \
      python3-setuptools liblzma-dev \
      python3-pygraphviz apt-utils


RUN pip install "poetry==$POETRY_VERSION"

# # Pyenv for our baseline python environment for poetry later on.
RUN git clone https://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

ENV PATH /root/.pyenv/bin:$PATH
RUN command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
RUN eval "$(pyenv init -)"

RUN pyenv install 3.8.0
RUN pyenv global 3.8.0

RUN poetry config virtualenvs.create false
RUN pip install --upgrade pip
RUN pip install setuptools pygraphviz

# Installing Nodejs
RUN curl -sL --location https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get -y install nodejs


