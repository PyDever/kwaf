#!/bin/bash

# this script will install kwaf on android
# only works using termux shell

function cleanup_installation {
  rm --force --recursive build/
  rm --force --recursive dist/
  rm --force --recursive *.egg-info

  rm --force --recursive *.pyc
  rm --force --recursive *.pyo
}

if [[ $(pwd) == *"/com.termux/"* ]]; then 

  # note the implicit use of python2 as per android linux syntax
  python2 setup.py build install # run python setuptools control script
  # install dependencies from requirements file
  python2 -m pip install -r requirements.txt
else
  echo '[ERR] It seems you are not using termux.';
  echo 'Quitting now.'; 
  exit
fi

cleanup_installation # run cleanup
exit


