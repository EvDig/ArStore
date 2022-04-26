import datetime

from data import db_session
from flask import Flask, render_template, redirect, helpers, request, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms.products import ProductForm
from flask import jsonify, url_for

from data import db_session
from data.products import Products
from data.applications import Application
from data.users import User
from forms.users import UserForm
from forms.application import RegisterForm
from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Products)
    return render_template("index.html", products=products)


@app.route('/info')
def info():
    db_sess = db_session.create_session()
    info = db_sess.query(User)
    return render_template("info.html", info=info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/products',  methods=['GET', 'POST'])
@login_required
def add_products():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = Products()
        products.title = form.title.data
        products.content = form.content.data
        db_sess.add(products)
        db_sess.commit()
        return redirect('/')
    return render_template('products.html', title='Добавление продукта',
                           form=form)


@app.route('/products/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_products(id):
    form = ProductForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id).first()
        if products:
            form.title.data = products.title
            form.content.data = products.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id).first()
        if products:
            products.title = form.title.data
            products.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('products.html',
                           title='Редактирование информации о товаре',
                           form=form
                           )


@app.route('/products_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def products_delete(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.id == id).first()
    if products:
        db_sess.delete(products)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/workers', methods=['GET', 'POST'])
@login_required
def worker_add():
    form = UserForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('workers.html', title='Регистрация работника',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('workers.html', title='Регистрация работника',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('workers.html', title='Регистрация работника', form=form)


@app.route('/application_send', methods=['GET', 'POST'])
def application_send():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        application = Application(
            name=form.name.data,
            about=form.about.data,
            email=form.email.data,
            phone_num=form.phone_num.data

        )
        db_sess.add(application)
        db_sess.commit()
        return redirect('/')
    return render_template('application_send.html', title='Отправка заявки', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
