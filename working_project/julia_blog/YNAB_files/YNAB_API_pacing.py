import json
from pprint import pprint
from datetime import datetime
import pandas as pd
import calendar
import numpy as np
import re
import os
from dateutil.relativedelta import relativedelta
import requests
import webbrowser
pd.options.display.max_rows = 99
pd.options.display.max_columns = 999
pd.options.display.float_format = '{:,.2f}'.format
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 1000)
### Calling API and authenticating

# saving sensitive info on the desktop
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
filename = desktop + "/details.txt"
with open(filename, "r") as file1:
    Lines = file1.readlines()
token = Lines[0].strip()
budget_id = Lines[1].strip()

my_headers = {'Authorization' : f'Bearer {token}'}
response = requests.get(f'https://api.youneedabudget.com/v1/budgets/{budget_id}', headers=my_headers)
budget = response.json()


### Set up dataframes for categories, transactions, months and category groups
### Also ingesting manually written User Input data not taken from the API around Max and ideal contributions
categories = pd.json_normalize(budget, record_path=['data','budget','categories'])
transactions = pd.json_normalize(budget, record_path=['data','budget','transactions'])
months = pd.json_normalize(budget, record_path=['data','budget','months'])
category_groups = pd.json_normalize(budget, record_path=['data','budget','category_groups'])
ALL_month_cats = pd.json_normalize(budget, record_path=['data','budget','months','categories'],meta=[['data','budget','months','month']])
accounts = pd.json_normalize(budget, record_path=['data','budget','accounts'])

path_parent = os.path.dirname(os.getcwd())


user_input = pd.read_excel(path_parent+"/working_project/julia_blog/YNAB_files/user_input.xlsx", index_col=0)
user_input.drop(['category_name','category_group_id','category_group_name'],axis=1,inplace=True)



## Table containing only months where the user actively used the budget - months outside of that shouldn't be used in calculating averages
today = datetime.now().strftime("%Y-%m-01")

active_months = months.loc[(months['income']>0) | (months['budgeted']> 0) | (months['activity']>0)]
active_months.reset_index(inplace=True)
active_months.drop('index',axis=1,inplace=True)
#
## create table containing current month's Category detail information only
current_month = active_months.loc[active_months['month']==today]


current_month_cats = ALL_month_cats.loc[ALL_month_cats['data.budget.months.month']==today]

## Adding Category Group information to the table
current_month_cats = pd.merge(current_month_cats, category_groups, left_on='category_group_id', right_on='id')
current_month_cats.drop(['hidden_y','hidden_x','original_category_group_id','note','goal_type','goal_creation_month','goal_target_month','goal_percentage_complete','deleted_x','deleted_y','id_y'],axis=1,inplace=True)
current_month_cats.rename(columns = {'name_y': 'category_group_name','name_x':'category_name','id_x':'category_id','id_y':'category_group_id'}, inplace = True)
current_month_cats = pd.merge(current_month_cats, user_input, on='category_id')

### Calculated fields & Cleanup for information of current Months Category Info
current_month_cats['balance'] = current_month_cats['balance']/1000
current_month_cats['budgeted'] = current_month_cats['budgeted']/1000
current_month_cats['activity'] = current_month_cats['activity']/1000
current_month_cats['goal_target'] = current_month_cats['goal_target']/1000
current_month_cats['starting_balance'] = current_month_cats['balance']-current_month_cats['activity']
current_month_cats['month_progress'] = int(datetime.now().strftime("%d"))/int(calendar.monthrange(int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m")))[1])
current_month_cats['paced_ideal_spend'] = current_month_cats['starting_balance']*current_month_cats['month_progress']
current_month_cats['pacing'] = np.where(((current_month_cats['balance']==0)|(current_month_cats['activity']==0)|(current_month_cats['starting_balance']==0)),0, current_month_cats['paced_ideal_spend']+ current_month_cats['activity'])

### New table to limit information to only those categories to be shown in pacing
current_month_pacing = current_month_cats.loc[current_month_cats['pacing']!=0]
current_month_pacing = current_month_pacing.loc[current_month_pacing['category_name']!='Inflow: Ready to Assign']
current_month_pacing = current_month_pacing.loc[current_month_pacing['category_name']!='Credit card']
current_month_pacing = current_month_pacing.loc[current_month_pacing['fix_cat']!=1]
current_month_pacing['pacing_perc'] = current_month_pacing['activity']*-1/current_month_pacing[['starting_balance', 'max_amount']].values.max(1)*100
current_month_pacing['daily_amount_left'] = current_month_cats['balance']/((int(calendar.monthrange(int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m")))[1])-int(datetime.now().strftime("%d")))+1)
current_month_pacing['daily_amount_target'] = current_month_cats['starting_balance']/(int(calendar.monthrange(int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m")))[1]))
current_month_pacing['paced_ideal_spend'] = np.where(current_month_pacing['max_amount']>0,0,current_month_pacing['paced_ideal_spend'])
current_month_pacing['pacing'] = np.where(current_month_pacing['max_amount']>0,0,current_month_pacing['pacing'])
current_month_pacing['daily_amount_left'] = np.where(current_month_pacing['max_amount']>0,0,current_month_pacing['daily_amount_left'])
current_month_pacing['daily_amount_target'] = np.where(current_month_pacing['max_amount']>0,0,current_month_pacing['daily_amount_target'])
current_month_pacing.sort_values(by=['max_amount','pacing_perc'],inplace=True)
current_month_pacing.reset_index(inplace=True)


## average transaction value per catgory to estimate avg transactions
transactions.sort_values(by=['date'],ascending=False,inplace=True)
transactions_top10=transactions.groupby('category_id').head(10).reset_index(drop=True)
transactions_top10 = transactions_top10.loc[:, ['amount', 'category_id']]
transactions_top10["amount"] = pd.to_numeric(transactions_top10["amount"], downcast="float")
transactions_top10=transactions_top10.groupby(['category_id']).mean()
transactions_top10['average_transaction_amount'] = transactions_top10['amount']/1000*-1


transactions_top50=transactions.groupby('category_id').head(50).reset_index(drop=True)
transactions_top50 = transactions_top50.loc[:, ['amount', 'category_id']]
transactions_top50["amount"] = pd.to_numeric(transactions_top50["amount"], downcast="float")
transactions_top50=transactions_top50.groupby(['category_id']).mean()
transactions_top50['average_transaction_50_amount'] = transactions_top50['amount']/1000*-1


transactions_top50.drop(['amount'],axis=1,inplace=True)
transactions_top50.reset_index(inplace=True)

transactions_count = transactions
transactions['date'] = transactions_count['date'].apply(lambda x: x[:7])
this_month= datetime.now().strftime("%Y-%m")
transactions_count = transactions_count.loc[(transactions_count['date']==this_month)]
transactions_count = transactions_count.groupby(['category_id']).count()
transactions_count['transaction_count'] = transactions_count['amount']
transactions_count.drop(['id','amount','date','memo','cleared','approved','flag_color','account_id','payee_id','transfer_account_id','transfer_transaction_id','matched_transaction_id','import_id','deleted'],axis=1,inplace=True)
transactions_count.reset_index(inplace=True)
## add transaction info to pacing tabel and calculate transactions left

current_month_pacing = pd.merge(current_month_pacing, transactions_top10, on='category_id')
current_month_pacing = pd.merge(current_month_pacing, transactions_top50, on='category_id')
current_month_pacing = pd.merge(current_month_pacing, transactions_count, on='category_id')

current_month_pacing.drop(['amount'],axis=1,inplace=True)
current_month_pacing['transactions_left'] = current_month_pacing['balance']//current_month_pacing['average_transaction_amount']
current_month_pacing['transaction_amount_change_perc'] = (current_month_pacing['average_transaction_amount']/current_month_pacing['average_transaction_50_amount']-1)*100


### New Table to remove unused columns
pacing_report = current_month_pacing.loc[:, ['category_group_name', 'category_name', 'activity','paced_ideal_spend','daily_amount_target','daily_amount_left','pacing','pacing_perc','average_transaction_amount','transactions_left','month_progress','cat_group_order','transaction_amount_change_perc','transaction_count']]
pacing_report['activity'] = pacing_report['activity']*-1
pacing_report['month_progress2'] = pacing_report['month_progress']*100

pacing_report['paced_ideal_spend'] = pacing_report['paced_ideal_spend']
pacing_report.sort_values(by=['cat_group_order'],inplace=True)

pacing_report['month_progress'] = ''
pacing_report['month_progress'].iloc[[0]] = pacing_report['month_progress2'][0]
pacing_report.drop(['month_progress2','cat_group_order'], axis=1, inplace=True)
#pacing_report.drop('cat_group_order',axis=1,inplace=True)
pacing_report.reset_index(inplace=True)
pacing_report.drop('index',axis=1,inplace=True)


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
# output = emoji_pattern.sub(r'', pacing_report.to_html())
# output = output.replace(u'\U0001F3A2','')
# output = output.replace(u'\U0001f7e1','')
# output = output.replace(u'\U0001f9f7','')
# output = output.replace(u'\U0001f9af','')
# output = output.replace(u'\u26ea','')
# output = output.replace(u'\u2016','')
# output = output.replace(u'\U0001f7e2','')
# output = output.replace(u'\U0001f3a2','')
# output = output.replace('class="dataframe"','class="table table-striped table-hover')
# path_parent = os.path.dirname(os.getcwd())
# text_file = open(path_parent+"/templates/YNAB_API_pacing.html", "w")
# text_file.write(output)
# text_file.close()
#webbrowser.open_new_tab("YNAB_API_pacing.html")

