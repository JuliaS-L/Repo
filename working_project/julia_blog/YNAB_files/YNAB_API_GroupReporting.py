import json
from pprint import pprint
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np
import re
import os
from dateutil.relativedelta import relativedelta
import requests
from julia_blog.YNAB_files.YNAB_API_pacing import budget,categories,transactions,months,category_groups,emoji_pattern,user_input
import webbrowser
pd.options.display.max_rows = 99
pd.options.display.max_columns = 999
pd.options.display.float_format = '{:,.2f}'.format
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 1000)
### Calling API and authenticating
ALL_month_cats = pd.json_normalize(budget, record_path=['data','budget','months','categories'],meta=[['data','budget','months','month']])

## Table containing only months where the user actively used the budget - months outside of that shouldn't be used in calculating averages
this_month = datetime.now().strftime("%Y-%m-01")
last_month = datetime.today()+ relativedelta(months=-1)
last_month = last_month.strftime("%Y-%m-01")
last_month1 = datetime.today()+ relativedelta(months=-2)
last_month1 = last_month1.strftime("%Y-%m-01")
last_month2 = datetime.today()+ relativedelta(months=-3)
last_month2 = last_month2.strftime("%Y-%m-01")
active_months = months.loc[(months['income']>0) | (months['budgeted']> 0) | (months['activity']>0)]
active_months.reset_index(inplace=True)
active_months.drop('index',axis=1,inplace=True)

## Adding Category Group information to the table
ALL_month_cats = pd.merge(ALL_month_cats, category_groups, left_on='category_group_id', right_on='id')
ALL_month_cats.drop(['hidden_y','hidden_x','original_category_group_id','note','goal_type','goal_creation_month','goal_target_month','goal_percentage_complete','deleted_x','deleted_y','id_y'],axis=1,inplace=True)
ALL_month_cats.rename(columns = {'name_y': 'category_group_name','name_x':'category_name','id_x':'category_id','id_y':'category_group_id','data.budget.months.month':'month'}, inplace = True)


current_month_cats = ALL_month_cats.loc[ALL_month_cats['month']==this_month]
user_group_input = pd.merge(current_month_cats, user_input, on='category_id')

#user_group_input = user_group_input.groupby(['category_group_name'], as_index=False).mean()
user_group_input = user_group_input.groupby(['category_group_name'], as_index=False).agg({'budgeted':'sum',
                                                                                          'activity':'sum',
                                                                                          'balance':'sum',
                                                                                          'goal_target':'sum',
                                                                                          'ideal_contribution':'sum',
                                                                                          'max_amount':'sum',
                                                                                          'savings_contr':'sum',
                                                                                          'fix_cat':'mean',
                                                                                          'cat_group_order':'mean'})
user_group_input.drop(['budgeted','activity','balance','goal_target'],axis=1,inplace=True)

ALL_month_cats['balance'] = ALL_month_cats['balance']/1000
ALL_month_cats['budgeted'] = ALL_month_cats['budgeted']/1000
ALL_month_cats['activity'] = ALL_month_cats['activity']/1000*-1
ALL_month_cats['goal_target'] = ALL_month_cats['goal_target']/1000
ALL_month_cats = ALL_month_cats.loc[~ALL_month_cats['category_group_name'].isin( ['Internal Master Category','Credit Card Payments','Hidden Categories'])]

ALL_active_month_cats = ALL_month_cats.loc[ALL_month_cats['month'].isin(active_months['month'].to_list())]

#### Create new category_name, ID, group_ID using savings
ALL_active_month_savings = pd.merge(ALL_active_month_cats, user_input, on='category_id')
ALL_active_month_savings['budgeted'] = ALL_active_month_savings['budgeted'] * ALL_active_month_savings['savings_contr']
ALL_active_month_savings['activity'] = ALL_active_month_savings['activity'] * ALL_active_month_savings['savings_contr']
ALL_active_month_savings = ALL_active_month_savings.groupby(['month'], as_index=False).sum()
ALL_active_month_savings['category_id'] = 'fake_category_id'
ALL_active_month_savings['category_group_id'] = 'fake_category_group_id'
ALL_active_month_savings['category_name'] = 'Total Savings'
ALL_active_month_savings['category_group_name'] = 'Total Savings'

ALL_active_month_savings.drop(['ideal_contribution', 'max_amount', 'savings_contr', 'fix_cat', 'cat_group_order'],axis=1,inplace=True)

ALL_active_month_savings['spending_this_month'] = np.where(ALL_active_month_savings['month']==this_month,ALL_active_month_savings['activity'],0)
ALL_active_month_savings['spending_last_month'] = np.where(ALL_active_month_savings['month']==last_month,ALL_active_month_savings['activity'],0)
ALL_active_month_savings['budgeting_this_month'] = np.where(ALL_active_month_savings['month']==this_month,ALL_active_month_savings['budgeted'],0)
ALL_active_month_savings['budgeting_last_month'] = np.where(ALL_active_month_savings['month']==last_month,ALL_active_month_savings['budgeted'],0)
ALL_active_month_savings['spending_this_month-1'] = np.where(ALL_active_month_savings['month']==last_month1,ALL_active_month_savings['activity'],0)
ALL_active_month_savings['spending_this_month-2'] = np.where(ALL_active_month_savings['month']==last_month2,ALL_active_month_savings['activity'],0)
ALL_active_month_savings['budgeting_this_month-1'] = np.where(ALL_active_month_savings['month']==last_month1,ALL_active_month_savings['budgeted'],0)
ALL_active_month_savings['budgeting_this_month-2'] = np.where(ALL_active_month_savings['month']==last_month2,ALL_active_month_savings['budgeted'],0)

ALL_active_month_cats['spending_this_month'] = np.where(ALL_active_month_cats['month']==this_month,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_this_month_perc'] = ALL_active_month_cats['spending_this_month']/ALL_active_month_cats['spending_this_month'].sum()*100
ALL_active_month_cats['spending_last_month'] = np.where(ALL_active_month_cats['month']==last_month,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_last_month_perc'] = ALL_active_month_cats['spending_last_month']/ALL_active_month_cats['spending_last_month'].sum()*100
ALL_active_month_cats['budgeting_this_month'] = np.where(ALL_active_month_cats['month']==this_month,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_this_month_perc'] = ALL_active_month_cats['budgeting_this_month']/ALL_active_month_cats['budgeting_this_month'].sum()*100
ALL_active_month_cats['budgeting_last_month'] = np.where(ALL_active_month_cats['month']==last_month,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_last_month_perc'] = ALL_active_month_cats['budgeting_last_month']/ALL_active_month_cats['budgeting_last_month'].sum()*100
ALL_active_month_cats['spending_this_month-1'] = np.where(ALL_active_month_cats['month']==last_month1,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_this_month-2'] = np.where(ALL_active_month_cats['month']==last_month2,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['budgeting_this_month-1'] = np.where(ALL_active_month_cats['month']==last_month1,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_this_month-2'] = np.where(ALL_active_month_cats['month']==last_month2,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats = pd.concat([ALL_active_month_cats,ALL_active_month_savings])
ALL_active_month_cats['spending_this_month_perc'] = np.where(ALL_active_month_cats['category_name']=='Total Savings',ALL_active_month_cats['spending_this_month']/ALL_active_month_cats['spending_this_month'].sum()*100,ALL_active_month_cats['spending_this_month_perc'])
ALL_active_month_cats['spending_last_month_perc'] = np.where(ALL_active_month_cats['category_name']=='Total Savings',ALL_active_month_cats['spending_last_month']/ALL_active_month_cats['spending_last_month'].sum()*100,ALL_active_month_cats['spending_last_month_perc'])
ALL_active_month_cats['budgeting_this_month_perc'] = np.where(ALL_active_month_cats['category_name']=='Total Savings',ALL_active_month_cats['budgeting_this_month']/ALL_active_month_cats['budgeting_this_month'].sum()*100,ALL_active_month_cats['budgeting_this_month_perc'])
ALL_active_month_cats['budgeting_last_month_perc'] = np.where(ALL_active_month_cats['category_name']=='Total Savings',ALL_active_month_cats['budgeting_last_month']/ALL_active_month_cats['budgeting_last_month'].sum()*100,ALL_active_month_cats['budgeting_last_month_perc'])

group_analysis = ALL_active_month_cats.groupby(['category_group_name'], as_index=False).sum()

group_analysis['spending_diff_mom'] = np.where(group_analysis['spending_last_month']==0,0,(group_analysis['spending_this_month']/group_analysis['spending_last_month']-1)*100)
group_analysis['budgeting_diff_mom'] = np.where(group_analysis['budgeting_last_month']==0,0,(group_analysis['budgeting_this_month']/group_analysis['budgeting_last_month']-1)*100)
group_analysis = pd.merge(group_analysis, user_group_input, on='category_group_name',how='left')
group_analysis['ideal_contribution_perc'] = group_analysis['ideal_contribution']/group_analysis['ideal_contribution'].sum()*100
group_analysis['spending_3m_diff'] = (group_analysis['spending_this_month']/((group_analysis['spending_last_month']+group_analysis['spending_this_month-1']+group_analysis['spending_this_month-2'])/3)-1)*100
group_analysis['budgeting_3m_diff'] = (group_analysis['budgeting_this_month']/((group_analysis['budgeting_last_month']+group_analysis['budgeting_this_month-1']+group_analysis['budgeting_this_month-2'])/3)-1)*100
group_analysis.sort_values(by=['cat_group_order'],inplace=True)
group_analysis.drop(['cat_group_order','savings_contr','fix_cat','max_amount','budgeting_this_month-2','budgeting_this_month-1','spending_this_month-2','spending_this_month-1','budgeted','activity','goal_target','balance'],axis=1,inplace=True)
group_analysis.reset_index(inplace=True)
group_analysis.fillna(0,inplace=True)
group_analysis.drop('index',axis=1,inplace=True)

total_analysis = group_analysis.copy()
total_analysis = total_analysis.loc[total_analysis['category_group_name']!= 'Total Savings']
total_analysis['category_group_name'] = "OVERALL"
total_analysis = total_analysis.groupby(['category_group_name'], as_index=False).sum()

total_analysis['spending_this_month_perc'] = 0
total_analysis['spending_last_month_perc'] = 0
total_analysis['budgeting_this_month_perc'] = 0
total_analysis['budgeting_last_month_perc'] = 0
total_analysis['ideal_contribution_perc'] = 0


group_analysis = pd.concat([group_analysis,total_analysis])
group_analysis.reset_index(inplace=True)
group_analysis.drop('index',axis=1,inplace=True)

category_analysis = ALL_active_month_cats.groupby(['category_name','category_id'], as_index=False).sum()
category_analysis['spending_diff_mom'] = np.where(category_analysis['spending_last_month']==0,0,(category_analysis['spending_this_month']/category_analysis['spending_last_month']-1)*100)
category_analysis['budgeting_diff_mom'] = np.where(category_analysis['budgeting_last_month']==0,0,(category_analysis['budgeting_this_month']/category_analysis['budgeting_last_month']-1)*100)
category_analysis = pd.merge(category_analysis, user_input, on='category_id')
category_analysis['ideal_contribution_perc'] = category_analysis['ideal_contribution']/category_analysis['ideal_contribution'].sum()*100
category_analysis['spending_3m_diff'] = (category_analysis['spending_this_month']/((category_analysis['spending_last_month']+category_analysis['spending_this_month-1']+category_analysis['spending_this_month-2'])/3)-1)*100
category_analysis['budgeting_3m_diff'] = (category_analysis['budgeting_this_month']/((category_analysis['budgeting_last_month']+category_analysis['budgeting_this_month-1']+category_analysis['budgeting_this_month-2'])/3)-1)*100
category_analysis.sort_values(by=['cat_group_order','budgeted'],ascending=[True,False],inplace=True)
category_analysis = category_analysis.loc[(category_analysis['balance']>0)]
category_analysis = category_analysis.loc[(category_analysis['budgeted']>0)]
category_analysis = category_analysis.loc[(category_analysis['activity']>0)]
category_analysis.drop(['category_id','cat_group_order','savings_contr','fix_cat','max_amount','budgeting_this_month-2','budgeting_this_month-1','spending_this_month-2','spending_this_month-1','budgeted','activity','goal_target','balance'],axis=1,inplace=True)
category_analysis.reset_index(inplace=True)
category_analysis.fillna(0,inplace=True)
category_analysis.drop('index',axis=1,inplace=True)

# output = emoji_pattern.sub(r'', group_analysis.to_html())
# output = output.replace(u'\U0001F3A2','')
# output = output.replace(u'\U0001f7e1','')
# output = output.replace(u'\U0001f9f7','')
# output = output.replace(u'\U0001f9af','')
# output = output.replace(u'\u26ea','')
# output = output.replace(u'\u2016','')
# output = output.replace(u'\U0001f7e2','')
# output = output.replace(u'\U0001f3a2','')
# output = output.replace('class="dataframe"','class="table table-striped table-hover')
# output = str(output.encode('utf-8').strip())
# path_parent = os.path.dirname(os.getcwd())
# text_file = open(path_parent+"/templates/YNAB_API_group_reporting.html", "w")
# text_file.write(output)
# text_file.close()
#
#
# output = emoji_pattern.sub(r'', category_analysis.to_html())
# output = output.replace(u'\U0001F3A2','')
# output = output.replace(u'\U0001f7e1','')
# output = output.replace(u'\U0001f9f7','')
# output = output.replace(u'\U0001f9af','')
# output = output.replace(u'\u26ea','')
# output = output.replace(u'\u2016','')
# output = output.replace(u'\U0001f7e2','')
# output = output.replace(u'\U0001f3a2','')
# output = output.replace('class="dataframe"','class="table table-striped table-hover')
#
#
# text_file = open(path_parent+"/templates/YNAB_API_group_reporting.html", "a")
# text_file.write(output)
# text_file.close()
#
# #ax = group_analysis.plot.barh(x='category_group_name', y='spending_this_month', rot=0)
# #plt.title('Spending this month')
# #ax.invert_yaxis()
#
# def html_bar(column):
#     html_string = "<br><br><h4>"
#     html_string += column
#     html_string += "</h4>"
#     html_string += "<table>"
#     for x in range(len(group_analysis['category_group_name'])):
#         html_string += "<tr><td>"
#         html_string += group_analysis['category_group_name'][x]
#         html_string += "</td><td><div style='background-color:blue;height:20px; width:"
#         html_string += str(group_analysis[column][x]/5)
#         html_string += "px'>"
#         html_string += group_analysis['category_group_name'][x]
#         html_string += "</div></td></tr>"
#     html_string +="</table>"
#
#     html_string = emoji_pattern.sub(r'', html_string)
#     html_string = html_string.replace(u'\U0001F3A2','')
#     html_string = html_string.replace(u'\U0001f7e1','')
#     html_string = html_string.replace(u'\U0001f9f7','')
#     html_string = html_string.replace(u'\U0001f9af','')
#     html_string = html_string.replace(u'\u26ea','')
#     html_string = html_string.replace(u'\u2016', '')
#     html_string = html_string.replace(u'\U0001f7e2','')
#     html_string = html_string.replace(u'\U0001f3a2','')
#     #html_string = html_string.replace('class="dataframe"','class="table table-striped table-hover')
#   #  html_string = str(html_string.encode('utf-8').strip())
#     with open(path_parent+"/templates/YNAB_API_group_reporting.html", "a") as file_object:
#         file_object.write( html_string)
#
# html_bar('spending_this_month')
# html_bar('spending_this_month_perc')
# html_bar('budgeting_this_month')
# html_bar('budgeting_this_month_perc')
# html_bar('spending_last_month')
# html_bar('spending_last_month_perc')
# html_bar('budgeting_last_month')
# html_bar('budgeting_last_month_perc')
# html_bar('spending_diff_mom')
# html_bar('budgeting_diff_mom')
# html_bar('ideal_contribution')
# html_bar('ideal_contribution_perc')
# html_bar('spending_3m_diff')
# html_bar('budgeting_3m_diff')



