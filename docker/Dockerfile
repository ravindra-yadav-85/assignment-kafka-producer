FROM python:3.7.11-slim-buster as base_image

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ARG HOME_DIR=/usr/local/python
WORKDIR ${HOME_DIR}
RUN apt-get update -yqq \
    && apt-get upgrade -yqq
COPY . .
RUN pip install -r ${HOME_DIR}/requirements.txt
FROM base_image as consumer
ENTRYPOINT ["python", "./kafka_consumer.py"]
FROM base_image as producer
ENTRYPOINT ["python", "./kafka_producer.py"]