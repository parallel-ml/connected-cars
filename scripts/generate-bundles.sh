#!/bin/bash

mkdir -p dependencies

pushd submodules/BreezySLAM/python/
python setup.py bdist_wheel
mv ./dist/*.tar.gz ../../../dependencies/
popd

pushd submodules/PyRoboViz/
python setup.py bdist_wheel
mv ./dist/*.tar.gz ../../dependencies/
popd
