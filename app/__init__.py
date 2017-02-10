from flask import Flask
import os
import sys
import logging

app = Flask(__name__)

if os.environ.get('HEROKU') is None:
    app.config.from_object('config')
    app.debug = False
else:
    app.secret_key = os.environ.get('SECRET_KEY')
    app.logger.addFilter(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.debug = False

from app import views
