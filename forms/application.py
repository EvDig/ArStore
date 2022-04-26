from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    phone_num = TextAreaField("Номер телефона", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])

    submit = SubmitField('Отправить')


