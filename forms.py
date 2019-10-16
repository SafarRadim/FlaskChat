from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    message = wtf.StringField('Message', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = wtf.StringField('Username', validators=[DataRequired()])
