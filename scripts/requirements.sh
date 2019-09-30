#!/bin/sh

poetry export -f requirements.txt --without-hashes -o requirements.txt
