from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class GameForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=1, max=50)],
    )
    genre = StringField(
        "Genre",
        validators=[DataRequired(), Length(min=1, max=40)],
    )
    platform = StringField(
        "Platform",
        validators=[DataRequired(), Length(min=1, max=20)],
    )
    save = SubmitField("Save")
