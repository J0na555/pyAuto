#!/bin/bash

function create() {
    source .env
    source ~/Documents/projects/pyAuto/pypy/bin/activate
    python pyauto.py $1
    cd $FILEPATH$1
    git init
    git remote add origin git@github.com:$USERNAME/$1.git
    touch README.md
    git add README.md
    git commit -m "Initial commit"
    git push -u origin main

    code .
}
