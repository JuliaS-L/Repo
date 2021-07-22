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

class budget_group_analysis(db.Model):
    category_group_name = db.Column(db.String(64),nullable=False,unique=True,index=True,primary_key=True)
    spending_this_month = db.Column(db.Float)
    spending_this_month_perc = db.Column(db.Float)
    spending_last_month = db.Column(db.Float)
    spending_last_month_perc = db.Column(db.Float)
    budgeting_this_month = db.Column(db.Float)
    budgeting_this_month_perc = db.Column(db.Float)
    budgeting_last_month = db.Column(db.Float)
    budgeting_last_month_perc = db.Column(db.Float)
    spending_diff_mom = db.Column(db.Float)
    budgeting_diff_mom = db.Column(db.Float)
    ideal_contribution = db.Column(db.Float)
    ideal_contribution_perc = db.Column(db.Float)
    spending_3m_diff = db.Column(db.Float)
    budgeting_3m_diff = db.Column(db.Float)

    def __init__(self,category_group_name,spending_this_month,spending_this_month_perc,spending_last_month,spending_last_month_perc,budgeting_this_month,budgeting_this_month_perc,budgeting_last_month,budgeting_last_month_perc,spending_diff_mom,budgeting_diff_mom,ideal_contribution,ideal_contribution_perc,spending_3m_diff,budgeting_3m_diff):
        self.category_group_name = category_group_name
        self.spending_this_month = spending_this_month
        self.spending_this_month_perc=spending_this_month_perc
        self.spending_last_month = spending_last_month
        self.spending_last_month_perc=spending_last_month_perc
        self.budgeting_this_month = budgeting_this_month
        self.budgeting_this_month_perc=budgeting_this_month_perc
        self.budgeting_last_month = budgeting_last_month
        self.budgeting_last_month_perc=budgeting_last_month_perc
        self.spending_diff_mom = spending_diff_mom
        self.budgeting_diff_mom=budgeting_diff_mom
        self.ideal_contribution = ideal_contribution
        self.ideal_contribution_perc=ideal_contribution_perc
        self.spending_3m_diff = spending_3m_diff
        self.budgeting_3m_diff=budgeting_3m_diff




class budget_category_analysis(db.Model):
    category_name = db.Column(db.String(64),nullable=False,unique=True,index=True,primary_key=True)
    spending_this_month = db.Column(db.Float)
    spending_this_month_perc = db.Column(db.Float)
    spending_last_month = db.Column(db.Float)
    spending_last_month_perc = db.Column(db.Float)
    budgeting_this_month = db.Column(db.Float)
    budgeting_this_month_perc = db.Column(db.Float)
    budgeting_last_month = db.Column(db.Float)
    budgeting_last_month_perc = db.Column(db.Float)
    spending_diff_mom = db.Column(db.Float)
    budgeting_diff_mom = db.Column(db.Float)
    ideal_contribution = db.Column(db.Float)
    ideal_contribution_perc = db.Column(db.Float)
    spending_3m_diff = db.Column(db.Float)
    budgeting_3m_diff = db.Column(db.Float)

    def __init__(self,category_group_name,spending_this_month,spending_this_month_perc,spending_last_month,spending_last_month_perc,budgeting_this_month,budgeting_this_month_perc,budgeting_last_month,budgeting_last_month_perc,spending_diff_mom,budgeting_diff_mom,ideal_contribution,ideal_contribution_perc,spending_3m_diff,budgeting_3m_diff):
        self.category_group_name = category_group_name
        self.spending_this_month = spending_this_month
        self.spending_this_month_perc=spending_this_month_perc
        self.spending_last_month = spending_last_month
        self.spending_last_month_perc=spending_last_month_perc
        self.budgeting_this_month = budgeting_this_month
        self.budgeting_this_month_perc=budgeting_this_month_perc
        self.budgeting_last_month = budgeting_last_month
        self.budgeting_last_month_perc=budgeting_last_month_perc
        self.spending_diff_mom = spending_diff_mom
        self.budgeting_diff_mom=budgeting_diff_mom
        self.ideal_contribution = ideal_contribution
        self.ideal_contribution_perc=ideal_contribution_perc
        self.spending_3m_diff = spending_3m_diff
        self.budgeting_3m_diff=budgeting_3m_diff


class budget_pacing(db.Model):
    category_name = db.Column(db.String(64),nullable=False,unique=True,index=True,primary_key=True)
    category_group_name = db.Column(db.String(64))
    activity = db.Column(db.Float)
    paced_ideal_spend = db.Column(db.Float)
    daily_amount_target = db.Column(db.Float)
    daily_amount_left = db.Column(db.Float)
    pacing = db.Column(db.Float)
    pacing_perc = db.Column(db.Float)
    average_transaction_amount = db.Column(db.Float)
    transactions_left = db.Column(db.Integer)
    month_progress = db.Column(db.Float)
    transaction_amount_change_perc = db.Column(db.Float)
    transaction_count = db.Column(db.Integer)

    def __init__(self,category_group_name,category_name,activity,paced_ideal_spend,daily_amount_target,daily_amount_left,pacing,pacing_perc,average_transaction_amount,transactions_left,month_progress,transaction_amount_change_perc,transaction_count):
        self.category_group_name = category_group_name
        self.category_name = category_name
        self.activity=activity
        self.paced_ideal_spend = paced_ideal_spend
        self.daily_amount_target=daily_amount_target
        self.daily_amount_left = daily_amount_left
        self.pacing=pacing
        self.pacing_perc = pacing_perc
        self.average_transaction_amount=average_transaction_amount
        self.transactions_left = transactions_left
        self.month_progress=month_progress
        self.transaction_amount_change_perc = transaction_amount_change_perc
        self.transaction_count=transaction_count


class user_input(db.Model):
    category_id = db.Column(db.String(64),nullable=False,unique=True,index=True,primary_key=True)
    category_group_id = db.Column(db.String(64))
    category_name = db.Column(db.String(64))
    category_group_name = db.Column(db.String(64))
    ideal_contribution = db.Column(db.Float)
    max_amount = db.Column(db.Float)
    savings_contr = db.Column(db.Float)
    fix_cat = db.Column(db.Float)
    cat_group_order = db.Column(db.Integer)

    def __init__(self,category_id,category_group_id,category_name,category_group_name,ideal_contribution,max_amount,savings_contr,fix_cat,cat_group_order):
        self.category_group_name = category_group_name
        self.category_name = category_name
        self.category_id=category_id
        self.category_group_id = category_group_id
        self.ideal_contribution=ideal_contribution
        self.max_amount = max_amount
        self.savings_contr=savings_contr
        self.fix_cat = fix_cat
        self.cat_group_order=cat_group_order


# db steps:
# flask db init
# flask db stamp head
# flask db migrate -m "message"
# flask db upgrade
