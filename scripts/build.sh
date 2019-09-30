#!/bin/sh

# generate requirements.txt
./scripts/requirements.sh

# build Python base
docker build --rm --build-arg BASE_IMAGE=alpine -f "docker/python.Dockerfile" -t lidar-slam-python:latest .

# build app
docker build --rm -f "docker/app.Dockerfile" -t lidar-slam-python:latest .
