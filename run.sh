#!/bin/bash

WORKDIR=/home/zabana/projects/willy
REQUIREMENTS_FILE=$WORKDIR/requirements.txt

# If the virutalenv folder does not exist, create and activate it.
if [[ ! -d "./ENV__willy" ]]; then
    echo "[log] Creating virtualenv and activating it ..."
    cd "$WORKDIR"; virtualenv -p python3.5 ENV__willy; source ENV__willy/bin/activate; cd ~
    echo "[log] Virtualenv successfully created and activated"
fi

# If the virtual env is not active, activate it.
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "[log] Virtualenv is not active. Activating it ..."
    cd "$WORKDIR"
    source ENV__willy/bin/activate
    cd ~
    echo "[log] Virtualenv is now active !"
fi

# Remove pkg resource package from requirements.txt
echo "[log] Removing pkg-resources package from requirements.txt."
cd "$WORKDIR"
grep -v "pkg-resources" requirements.txt > requirements_new.txt

# Temporary hack until I get tee to fuckin work properly
rm requirements.txt
mv requirements_new.txt requirements.txt

cd ~
echo "[log] Package successfully removed."

# pull down dependencies
echo "[log] Pulling down dependencies ..."
cd "$WORKDIR"
pip install -r requirements.txt
cd ~
echo "[log] Dependencies downloaded !"

# nohup the shit out of the app
echo "[log] Running Script ... "
cd "$WORKDIR"
nohup python -u main.py > startups.log &
