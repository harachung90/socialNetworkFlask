from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from flask_login import LoginManager
import forms
import models

app = Flask(__name__)
app.secret_key = 'Dx9mq2xuzGsEmU3WYKwV3OEMTRXEgO5qKlQZLnWP4KvhoJccfBamS'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """CLose the database connection after each request."""
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm
    if form.validate():
        flash("Yay, you're registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/')
def index():
    return "Hey"

# def initialize():
#     DATABASE.connect()
#     DATABASE.create_tables([User], safe=True)
#     DATABASE.close()

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='HaraChung',
            email='harachung90@gmail,com',
            password='passwprd',
            admin=True
        )
    except ValueError:
        pass

    app.run()
