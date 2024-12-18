from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import *
from app.repository import PostgresQLRepository


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'User'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    account = None
    repository = PostgresQLRepository()
    if form.validate_on_submit():
        account = repository.get_user(form.username.data, form.password.data)
        if account:
            flash('Вошёл {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('index'))
        else:
            flash('Неправильные логин или пароль')
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    repository = PostgresQLRepository()
    if form.validate_on_submit():
        if repository.register_user(form.username.data, form.password.data, form.first_name.data, form.last_name.data, form.birth_date.data):
            flash('Пользователь {} зарегистрирован'.format(form.username.data))
            return redirect(url_for('login'))
        else:
            flash('Что-то пошло не так')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)
