from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Наименование товара', validators=[DataRequired()])
    content = TextAreaField("Описание")
    submit = SubmitField('Применить')
