# Flask-WTF forms (e.g., LoginForm, CertificationForm)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Simple login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class HCPForm(FlaskForm):
    """Form for creating a health care professional."""
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')


class ClientForm(FlaskForm):
    """Form for creating a client."""
    initials = StringField('Initials', validators=[DataRequired()])
    is_primary = BooleanField('Primary Client')
    submit = SubmitField('Save')
