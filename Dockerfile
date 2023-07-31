FROM python:3.10-bullseye

WORKDIR /app

# Get curl
RUN apt update \
    && apt install -y curl

# Bind libcurl
RUN apt-cache search libcurl | grep python \
    && apt install python3-pycurl \
    && apt-cache search libcurl

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin

# Install dependecies
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy all source files
COPY . /app

# Execute application
# ENTRYPOINT ["poetry", "run", "python", "-m", "kube_hound"]