#!/bin/bash

set -eux
set -o pipefail

HERE=$(dirname "$0")
REPOS="${REPOS:-$HERE/..}"
mkdir -p "$REPOS"
pushd "$REPOS"

pip install empy catkin_pkg nose
brew install boost boost-python

[ ! -d googletest ] && git clone git@github.com:google/googletest.git
[ ! -d catkin ] && git clone git@github.com:ros/catkin.git
[ ! -d serial ] && git clone git@github.com:wjwwood/serial.git
[ ! -d ubloxM8 ] && git clone git@github.com:swift-nav/ubloxM8.git

pushd catkin
cmake .
make install
popd # catkin

pushd googletest
cmake .
make install
popd # googletest

pushd serial
cmake .
make install
popd # serial

pushd ubloxM8
cmake .
make all
python setup.py install
popd # ubloxM8

popd # repos dir
