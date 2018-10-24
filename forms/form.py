from flask_wtf import Form
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, Email


class MemberForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    name = StringField('name', validators=[DataRequired()])
    gender =  RadioField('Label', choices=[('male','Male'),('female','Female')], validators=[DataRequired()])

