from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, Regexp

from yacut.constants import MAX_LENGHT_SHORT, REGULAR


class URLForm(FlaskForm):
    original_link = StringField(
        "Длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            URL(message="Некорректный URL"),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Length(max=MAX_LENGHT_SHORT, message="Максимум 16 символов"),
            Regexp(REGULAR, message="Только латинские буквы и цифры"),
        ],
    )
    submit = SubmitField("Создать")
