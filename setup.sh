#! /bin/bash

cp config.json.dist config.json

brew install pyenv
brew install pipenv

pyenv install
pipenv install

mkdir sql
touch src/databaseb.sqlite