#!/bin/bash
git clone https://github.com/matthew-brett/multibuild
source multibuild/osx_utils.sh
get_macpython_environment $TRAVIS_PYTHON_VERSION venv
