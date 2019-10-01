#!/bin/bash

# build client
docker build --rm -f "./client/Dockerfile" -t nimashoghi/lidar-slam-client:latest ./client/

# build server
docker build --rm -f "./server/Dockerfile" -t nimashoghi/lidar-slam-server:latest ./server/
