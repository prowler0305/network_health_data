from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, RadioField
from wtforms.validators import InputRequired


class ContainerForm(FlaskForm):
    add_delete_radio = RadioField('', choices=[('dev1', 'Dev Container 1'), ('dev2', 'Dev Container 2')])
    requested_start_date = DateField('Start Date', format='%m-%d-%Y')
    requested_end_date = DateField('End Date', format='%m-%d-%Y')
    point_of_contact_name = StringField('Name')
    point_of_contact_email = StringField('Email')
    submit = SubmitField('Submit')
