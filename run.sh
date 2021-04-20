#!/bin/bash

# check if venv exists, if not create
if [ ! -d "./env" ]; then
    echo "create venv"
    python3 -m venv env
fi   

# activate environment
echo "Activating environment.."
source env/bin/activate

# update pip
echo "Installing.."
python -m pip install -U pip

# install setup.py
pip install -e .

# run application
run -f $1