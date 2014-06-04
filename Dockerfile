FROM alpine:latest
RUN apk add --no-cache make ca-certificates python py-setuptools py-lxml; easy_install-2.7 pip
RUN pip install -U pip; pip install html5lib markdown docutils
ADD . /var/www/yottatsa.name
WORKDIR /var/www/yottatsa.name
RUN rm -rf .git; make
VOLUME /var/www/yottatsa.name
CMD true
