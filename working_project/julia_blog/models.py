#project and blog model
from julia_blog import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.

    posts = db.relationship('BlogPost', backref='author', lazy=True)
    projects = db.relationship('Project', backref='author', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"



class Project(db.Model):
    __tablename__ = 'projects'
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    project_image = db.Column(db.String(20),nullable=False,default = 'default_project.png')
    project_title = db.Column(db.String(64),nullable=False,unique=True,index=True)
    project_description = db.Column(db.String(128),nullable=False,unique=True,index=True)
    project_text = db.Column(db.Text,nullable=False)
    project_code = db.Column(db.Text,nullable=False,default = "None")
    project_trinket_code = db.Column(db.String(64),default = "None")
    project_github_code = db.Column(db.String(64),default = "None")
    project_date = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    #username = db.relationship('User',backref = 'project',lazy=True)

    def __init__(self,project_title,project_description,project_text,project_code,user_id,project_github_code,project_trinket_code):
        self.project_title = project_title
        self.project_description = project_description
        self.project_text = project_text
        self.project_code = project_code
        self.project_github_code = project_github_code
        self.project_trinket_code = project_trinket_code
        self.user_id=user_id

    def __repr__(self):
        return f"Project {self.project_title} is {self.id}"

class BlogPost(db.Model ):
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    date = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    blog_title = db.Column(db.String(64),nullable=False,unique=True,index=True)
    blog_text = db.Column(db.Text,nullable=False)

    def __init__(self,blog_title,blog_text,user_id):
        self.blog_title = blog_title
        self.blog_text = blog_text
        self.user_id=user_id

    def __repr__(self):
        return f"Blog {self.blog_title} is {self.id}."



# db steps:
# flask db init
# flask db stamp head
# flask db migrate -m "message"
# flask db upgrade
