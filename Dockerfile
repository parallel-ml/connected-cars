ARG BASE_IMAGE=balenalib/raspberrypi3-alpine
ARG BASE_IMAGE_VERSION=latest
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION}

RUN [ "cross-build-start" ]

# install python
RUN apk add --no-cache python3 \
    && ln -s /usr/bin/python3 /usr/local/bin/python

# install pip
RUN apk add --no-cache --virtual .pip-build-deps curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && apk del .pip-build-deps

# print python version
RUN python3 --version

# copy all files
COPY . .

# install dependencies
RUN apk add --no-cache --virtual .build-deps alpine-sdk python3-dev \
    && pip install --requirement requirements.txt \
    && apk del .build-dependencies

RUN [ "cross-build-end" ]

# run the app
CMD python app.py
