#!/bin/bash

function create() {

    source .env

    if [[ -z "$FILEPATH" || -z "$USERNAME" || -z "$GITHUB_TOKEN" ]]; then
        echo "❌ Missing environment variables. Check your .env file."
        return 1
    fi

    if [ -z "$1" ]; then
        echo "Please provide a project name. Usage: create <project_name>"
        return 1
    fi

    # Run Python script to create GitHub repo and local folder
    python3 pyauto.py "$1"

    # Move into new project directory
    cd "$FILEPATH$1" || { echo "Failed to cd into $FILEPATH$1"; return 1; }

    # Initialize git and push to GitHub using SSH
    git init
    git remote add origin git@github.com:$USERNAME/$1.git
    touch README.md
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git push -u origin main
    code .
}
