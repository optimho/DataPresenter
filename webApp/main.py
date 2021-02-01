from flask import Blueprint, render_template, flash, redirect
from webApp.extensions import mongo
from webApp.forms import LoginForm
import webbrowser
import webview
main = Blueprint('main', __name__)

webbrowser.open("127.0.0.1:5000", new=0, autoraise=True)

@main.route('/')
@main.route('/index')
def index():
    title = {'IoT data View'}
    user = {'username': 'Michael'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)


@main.route('/temp')
def listTemp():
    Users_in_db = mongo.db.device.find()
    return render_template("index.html",
                           Users_in_db=list(Users_in_db))


@main.route('/ave')
def listAveTemp():
    counter = 0
    Users_in_db = mongo.db.device.find()
    Users_in_db = list(Users_in_db)
    for item in Users_in_db:
        counter += 1
        total = + item.Temperature
    total = total / counter
    return render_template("ave.html",
                           total=total)


@main.route('/addUser', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        name = form.username.data
        remember_me = form.remember_me.data
        password = form.password.data
        user_collection = mongo.db.users
        user_collection.insert({'name': name, 'remember_me': remember_me, 'password': password})
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)


@main.route('/plot', methods=['GET', 'POST'])
def plot():
    return render_template('plot.html', title='Plot')
