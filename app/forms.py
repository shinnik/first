# from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms import Form


class SearchUsersForm(Form):
    query = StringField('query', validators=[DataRequired()])
    limit = IntegerField('limit', validators=[DataRequired()])
