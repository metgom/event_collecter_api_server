FROM nginx:latest

WORKDIR /etc/nginx/conf.d

COPY ./nginx.conf ./apiserver.conf

RUN apt-get update && apt-get install -y vim nano curl procps

RUN "service nginx start"
ENTRYPOINT ["/bin/bash"]