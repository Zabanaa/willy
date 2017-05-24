#!/bin/bash

# Create virtualenv
if [[ -d "./ENV__willy" ]]; then
    virtualenv -p python3.5 ENV__willy
fi

# Activate virtualenv
source ENV_willy/bin/activate

# pull down dependencies
pip install -r requirements.txt

# nohup the shit out of the app
nohup python -u main.py > startups.log &
