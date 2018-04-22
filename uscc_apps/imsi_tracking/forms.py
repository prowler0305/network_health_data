from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, HiddenField
from wtforms.validators import InputRequired


class ImsiForm(FlaskForm):
    imsis = StringField('Imsi(s)')
    email = StringField('Email')
    imsi_filter = StringField('Search:')
    art = HiddenField("hidden1")
    userid = HiddenField("hidden2")
    add_delete_radio = RadioField('', choices=[('A', 'Add'), ('D', 'Delete')])
    submit = SubmitField('Submit')
