from flask_wtf import FlaskForm
from wtforms import Form, DateTimeField, validators


class ProgramForm(FlaskForm):
    start_time = DateTimeField('Start time', format="%Y-%m-%dT%H:%M:%S", validators=[validators.DataRequired()])
    final_time = DateTimeField('Final time', [validators.DataRequired()])