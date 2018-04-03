from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired


class ImsiForm(FlaskForm):
    imsis = StringField('Imsi(s)', validators=[InputRequired()])
    imsi_filter = StringField('Search:')
    add_delete_radio = RadioField('', choices=[('A', 'Add'), ('D', 'Delete')])
    submit = SubmitField('Submit')
