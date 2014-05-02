#!/usr/bin/env python


# Imports
from modules.bottle import Bottle, template

# App
app = Bottle()


@app.get('/')
def default():
  return static_file('index.html','.')

