#!/usr/bin/env bash

# install dependencies
pip install -r requirements.txt
npm install

# build webpack
npx webpack --mode=development

# run db relations (currently doesn't do anything)
python manage.py migrate
