#!/bin/bash

pushd client
poetry export -f requirements.txt --without-hashes -o requirements.txt
popd

pushd server
poetry export -f requirements.txt --without-hashes -o requirements.txt
popd
