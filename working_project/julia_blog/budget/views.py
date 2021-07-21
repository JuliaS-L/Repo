from flask import render_template,url_for,flash,redirect,request,Blueprint
from julia_blog import db
from flask_login import current_user,login_required
from julia_blog.YNAB_files.YNAB_API_GroupReporting import group_analysis,category_analysis
from julia_blog.YNAB_files.YNAB_API_pacing import pacing_report

budgets = Blueprint('budgets',__name__)

@budgets.route('/budget')
@login_required
def budget():
    #page = request.args.get('page',1,type=int)
    #budget_list = Project.query.order_by(Project.project_date.desc()).paginate(page=page,per_page=5)
    return render_template('budget.html')

@budgets.route('/budget/reporting')
@login_required
def reporting():
    # group_analysis.to_sql(name='group_analysis', con=db.engine, index=False)
    # for index, row in group_analysis.iterrows():
    #     group_analysis_add = group_analysis(group_analysis=row[1], shack=row[2])
    #     db.session.add(client_add)
    #     db.session.commit()
    return render_template('YNAB_API_group_reporting.html')