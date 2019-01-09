from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, Email


class ShipmentForm(FlaskForm):
    waybill = StringField('waybill', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])
    notes = StringField('notes', validators=[DataRequired()])




