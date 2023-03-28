from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=1, max=10)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=1, max=100)],
    )
    login = SubmitField("Login")
