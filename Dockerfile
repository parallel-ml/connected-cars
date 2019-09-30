ARG BASE_IMAGE=arm32v7/alpine
ARG BASE_IMAGE_VERSION=3.10
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION}

# install python
RUN apk add --no-cache python3 \
    && ln -s /usr/local/bin/python /usr/bin/python3

# install pip
RUN apk add --no-cache --virtual .build-deps curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && apk del .build-deps

# copy all files
COPY . .

# install dependencies
RUN pip install --requirement requirements.txt

# run the app
CMD python app.py
