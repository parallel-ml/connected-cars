FROM python:alpine

# copy all files
WORKDIR /app
COPY . .

# install python dependencies
RUN pip install --requirement requirements.txt

# flask app name
ENV FLASK_APP=app.py

# run the app
CMD flask run
