from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Наименование товара', validators=[DataRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    src = TextAreaField("Путь к картинке для товара", validators=[DataRequired()])
    price = TextAreaField("Цена товара", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])
