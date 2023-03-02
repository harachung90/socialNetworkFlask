from flask import Flask, g
from flask_login import LoginManager

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

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

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

def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()

if __name__ == '__main__':
    models.initialise()
    models.User.create_user(
        name='HaraChung',
        email='harachung90@gmail,com',
        password='passwprd',
        admin=True
    )
    app.run()
