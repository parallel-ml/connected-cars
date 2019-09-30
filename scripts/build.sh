#!/bin/sh

# build app
docker build --rm -f "Dockerfile" -t nimashoghi/lidar-slam:latest .
