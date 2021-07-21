from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app= Flask (__name__)


app.config['SECRET_KEY'] = 'mysecret'
###### DB Setup#####
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlight')

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
db = SQLAlchemy(app)
Migrate(app,db,render_as_batch=True)

### LOGIN HANDLER ######

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

### Blueprints ###
from julia_blog.core.views import core
from julia_blog.error_pages.handlers import error_pages
from julia_blog.users.views import users
from julia_blog.blog_posts.views import blog_posts
from julia_blog.projects.views import projects
from julia_blog.budget.views import budgets

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(projects)
app.register_blueprint(budgets)
