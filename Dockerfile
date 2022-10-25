FROM python:3.10-slim-bullseye

WORKDIR /home/api_server

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt gunicorn
RUN apt-get update && apt-get install -y vim nano curl procps net-tools
COPY ./app ./app

EXPOSE 5000

ENTRYPOINT ["/bin/bash"]