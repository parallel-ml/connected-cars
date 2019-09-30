ARG BASE_IMAGE=lidar-slam-python
ARG BASE_IMAGE_VERSION=latest
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION}

# copy all files
COPY . .

# install dependencies
RUN pip install --requirement requirements.txt

# run the app
CMD python app.py
