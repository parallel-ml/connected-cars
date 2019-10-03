FROM alpine

# install python and pip
RUN apk add --no-cache curl python3 \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py

# install numpy and matplotlib
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing py3-matplotlib py3-numpy

# install py3-qt5
RUN apk add --no-cache py3-qt5

# copy all files
WORKDIR /app
COPY . .

# install python dependencies
RUN pip install --requirement requirements.txt

# flask app name
ENV FLASK_APP=app.py

# run the app
CMD flask run -h 0.0.0.0 -p 5000
