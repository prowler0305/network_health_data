from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, RadioField


class ContainerForm(FlaskForm):
    container_name = RadioField('', choices=[('dev_container_1', 'Dev Container 1'), ('dev_container_2', 'Dev Container 2')])
    start_date = DateField('Start Date', format='%m/%d/%Y')
    end_date = DateField('End Date', format='%m/%d/%Y')
    poc_name = StringField('Name')
    poc_email = StringField('Email')
    submit = SubmitField('Submit')
