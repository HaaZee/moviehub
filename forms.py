from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from markupsafe import Markup
