#!/usr/bin/env python

# Imports
from bottle import *

# App
app = Bottle()
debug(True)

@app.get('/')
def default():
  return static_file('index.html','.')

