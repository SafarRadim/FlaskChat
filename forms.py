from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = wtf.StringField('Username', validators=[DataRequired()])
    password = wtf.PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = wtf.StringField('Username', validators=[DataRequired()])
    password = wtf.PasswordField('Password', validators=[DataRequired()])
