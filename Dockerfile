FROM python:3.11-alpine

RUN mkdir -p /etc/apt/sources.list.d
RUN apk add gnupg
RUN apk add python3-dev
RUN apk add gcc
RUN apk add make
RUN apk add musl-dev
RUN apk add linux-headers

RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list \
  && gpg --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apk update
RUN apk upgrade

ENV PYTHONPATH=/usr/lib/python3/dist-packages

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]
