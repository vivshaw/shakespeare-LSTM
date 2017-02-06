from flask_wtf import Form
from wtforms import StringField, HiddenField


class SonnetForm(Form):
    seed_phrase = StringField('seed_phrase')
    seed = StringField('seed')
    seed_tag = StringField('seed_tag')
