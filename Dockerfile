FROM python:3.9-alpine


RUN mkdir -p /usr/src
# create the app user
RUN addgroup -S app && adduser -S app -G app

ENV HOME=/user/src
ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install necessary required modules for the Alpine linux
RUN apk add --update --virtual .tmp gcc py3-grpcio g++ libc-dev linux-headers \
	&& apk add tcl-dev tiff-dev musl-dev python3-dev postgresql-dev libpq nano libffi-dev py-cffi \
	&& apk add openssl-dev curl-dev coreutils cargo dos2unix postgresql-client openssh-client rustup certbot certbot-nginx gfortran openblas-dev lapack-dev

RUN pip install --upgrade pip
RUN pip install cryptography


COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

# delete the .tmp installation folder file
RUN apk del .tmp

COPY ./entrypoint.sh .

# convert windows file ending to linux
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN chmod +x entrypoint.sh

RUN mkdir -p media
RUN mkdir -p staticfiles

RUN chmod -R 755 media
RUN chmod -R 755 staticfiles

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]