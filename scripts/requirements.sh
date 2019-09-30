#!/bin/sh

poetry export -f requirements.txt | sed "s/^-e //g" > ./requirements.txt
