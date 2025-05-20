#!/bin/bash

function create() {
    cd
    python pyauto.py $1
    cd /home/jonas/Documents/projects/pyAuto/$1
    git init
    touch README.md
    git add .
    git commit -m 'Initial Commit'
    git remote add origin https://github.com/J0na555/$1.git
    git push -u origin master
    code .
}
