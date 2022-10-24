FROM python:3.10-slim-bullseye

WORKDIR /home/api_server

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt gunicorn
RUN apt-get update && apt-get install -y vim nano curl procps net-tools
COPY ./app .

EXPOSE 5000

RUN "gunicorn main:app -b 0.0.0.0:5000 -k uvicorn.workers.UvicornWorker --access-logfile ./access.log --daemon"]
ENTRYPOINT ["/bin/bash"]