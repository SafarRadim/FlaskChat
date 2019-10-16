from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired

class Form(FlaskForm):
    message = wtf.StringField('message', validators=[DataRequired()])