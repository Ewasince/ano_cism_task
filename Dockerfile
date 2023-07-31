FROM python:3.11-slim-buster

#
WORKDIR /app
COPY . /app

#
RUN mkdir -p /app/logs

# deps
RUN cd /app/migrations \
    && pip install -r requirements.txt \
    && cd /app \
    && pip install -r requirements.txt


# rest port
EXPOSE 7777

#
CMD chmod a+x ./run_service_in_docker.sh && /bin/sh ./run_service_in_docker.sh
