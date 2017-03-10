FROM daocloud.io/python:3.6
MAINTAINER livingworld <455412741@qq.com>

RUN mkdir -p /app
COPY . /app
WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["docker-entrypoint.sh"]
CMD [""]