#!/bin/bash

mkdir -p dependencies

pushd submodules/BreezySLAM/python/
python setup.py sdist --formats=gztar
mv ./dist/*.tar.gz ../../../dependencies/
popd

pushd submodules/PyRoboViz/
python setup.py sdist --formats=gztar
python setup.py sdist --formats=gztar
mv ./dist/*.tar.gz ../../dependencies/
popd
