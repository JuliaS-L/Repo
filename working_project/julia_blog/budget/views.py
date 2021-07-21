from flask import render_template,url_for,flash,redirect,request,Blueprint
from julia_blog import db
from flask_login import current_user,login_required
from julia_blog.models import budget_group_analysis
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
    rows = budget_group_analysis.query.all()
    for x in range(len(group_analysis)):
        category_group_name = group_analysis['category_group_name'][x]
        spending_this_month = group_analysis['spending_this_month'][x]
        spending_this_month_perc = group_analysis['spending_this_month_perc'][x]
        spending_last_month = group_analysis['spending_last_month'][x]
        spending_last_month_perc = group_analysis['spending_last_month_perc'][x]
        budgeting_this_month = group_analysis['budgeting_this_month'][x]
        budgeting_this_month_perc = group_analysis['budgeting_this_month_perc'][x]
        budgeting_last_month = group_analysis['budgeting_last_month'][x]
        budgeting_last_month_perc = group_analysis['budgeting_last_month_perc'][x]
        spending_diff_mom = group_analysis['spending_diff_mom'][x]
        budgeting_diff_mom = group_analysis['budgeting_diff_mom'][x]
        ideal_contribution = group_analysis['ideal_contribution'][x]
        ideal_contribution_perc = group_analysis['ideal_contribution_perc'][x]
        spending_3m_diff = group_analysis['spending_3m_diff'][x]
        budgeting_3m_diff = group_analysis['budgeting_3m_diff'][x]
        record = budget_group_analysis(category_group_name,spending_this_month,spending_this_month_perc,spending_last_month,spending_last_month_perc,budgeting_this_month,budgeting_this_month_perc,budgeting_last_month,budgeting_last_month_perc,spending_diff_mom, budgeting_diff_mom, ideal_contribution, ideal_contribution_perc, spending_3m_diff, budgeting_3m_diff)
        db.session.add(record)
        db.session.commit()
    rows = budget_group_analysis.query.all()
    return render_template('budget_group_analysis.html',
                           title='Category Group Spending',
                           rows=rows)
    # clean table
    # add rows
    # represent table

    # group_analysis.to_sql(name='group_analysis', con=db.engine, index=False)
    # for index, row in group_analysis.iterrows():
    #     group_analysis_add = group_analysis(category_group_name=row[0], spending_this_month=row[1],spending_this_month_perc =row[2],spending_last_month =row[3],spending_last_month_perc =row[4],budgeting_this_month =row[5],budgeting_this_month_perc =row[6],budgeting_last_month =row[7],budgeting_last_month_perc =row[8],spending_diff_mom =row[9],budgeting_diff_mom =row[10],ideal_contribution =row[11],ideal_contribution_perc =row[12] ,spending_3m_diff =row[13] ,budgeting_3m_diff =row[14])
    #     db.session.add(group_analysis_add)
    #     db.session.commit()
    return render_template('YNAB_API_group_reporting.html')
