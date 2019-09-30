#!/usr/bin/fish

apt-get update
apt-get install --yes --no-install-recommends libfreetype6-dev libopenblas-dev libpng-dev
poetry install
