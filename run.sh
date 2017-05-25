#!/bin/bash

# If the virutalenv folder does not exist
# create it, and activate it
if [[ -d "./ENV__willy" ]]; then
    virtualenv -p python3.5 ENV__willy

    # Activate virtualenv
    source ENV_willy/bin/activate

fi

# If the virtual env is not active, activate it.
if [[ -z "$VIRTUAL_ENV" ]]; then
    # Activate virtualenv
    source ENV_willy/bin/activate
fi

# Remove pkg resource package from requirements.txt
grep -v "pkg-resources" requirements.txt | tee requirements.txt

# pull down dependencies
pip install -r requirements.txt

# nohup the shit out of the app
nohup python -u main.py > startups.log &
