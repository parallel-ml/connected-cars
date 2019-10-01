FROM python:alpine

# install numpy and matplotlib
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing py3-matplotlib py3-numpy

# install python dependencies
RUN pip install --requirement requirements.txt

# copy all files
WORKDIR /app
COPY . .

# flask app name
ENV FLASK_APP=app.py

# run the app
CMD flask run
