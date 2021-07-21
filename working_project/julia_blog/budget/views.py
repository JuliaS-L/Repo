from flask import render_template,url_for,flash,redirect,request,Blueprint
from julia_blog import db
from flask_login import current_user,login_required

budgets = Blueprint('budgets',__name__)


@budgets.route('/budget')
@login_required
def budget():
    #page = request.args.get('page',1,type=int)
    #budget_list = Project.query.order_by(Project.project_date.desc()).paginate(page=page,per_page=5)
    return render_template('budget.html')

@budgets.route('/budget/reporting')
def reporting():
    return render_template('YNAB_API_group_reporting.html')