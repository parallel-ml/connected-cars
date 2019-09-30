ARG BASE_IMAGE=balenalib/raspberrypi3-alpine
ARG BASE_IMAGE_VERSION=latest
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION}

RUN ["cross-build-start"]

# install python
RUN apk add --no-cache python3 \
    && ln -s /usr/bin/python3 /usr/local/bin/python

# install pip
RUN apk add --no-cache --virtual .pip-build-deps curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && rm get-pip.py \
    && apk del .pip-build-deps

# copy all files
WORKDIR /app
COPY . .

# install system dependencies
RUN apk add --no-cache py3-numpy freetype-dev libpng-dev openblas-dev

# install python dependencies
RUN apk add --no-cache --virtual .build-deps alpine-sdk python3-dev \
    && pip install --requirement requirements.txt \
    && apk del .build-deps

RUN ["cross-build-end"]

# run the app
CMD python app.py
