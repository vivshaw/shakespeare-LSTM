from flask import Flask
import os

app = Flask(__name__)
if os.environ.get('HEROKU') is None:
    app.config.from_object('config')
else:
    app.secret_key = os.environ.get('SECRET_KEY')

from app import views

