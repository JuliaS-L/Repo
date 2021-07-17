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
user_input_data = {'category_id': [
        "1100a8cc-2073-4e2b-9bba-3c594faa91de","88544615-450e-43a6-acbb-f2b253d160f5","dca4fcf5-ca77-4274-b70a-e115e0df1b72","2a76296b-d65e-4fec-a84e-60b6a4d5b87a","a3538e62-cdf7-462a-84d1-a40f311adf7b","4c839e72-d5f1-4100-9dc8-ea04f67b4b56","5de4c47e-132e-4d8c-b1e4-c1310e3d2853","f1a9e570-f69b-4cf5-86e8-69c790c18797","9f3c6b44-493f-4467-b9e4-96773cd4a4c9","ef884921-68ad-4255-bf70-c9451017c204","a85e5acf-058d-4995-b3f2-3a6402bef4b6","cfa2b061-158e-4e04-a267-de91a62c4934","8bbe50a4-1414-4bbb-8a0c-62c1f12eb271","d68a0f76-6764-40e5-9b39-bd865a777850","c8efd4c0-cd43-44f0-9d45-a456d018c342","4497eb7b-4377-4ff2-97fd-924b36a7b94b","4e333126-5759-46fc-9b2d-fe4491740600","eda4a99f-1acc-400c-a3c1-2c285963529c","293fca17-d5df-4fba-8d27-63b75909d1ce","c04e3d76-fe15-4b64-bb86-30aff7a614d0","1ecb11d4-74de-4b59-ae18-6071c85b9286","47ff1263-b0a6-4b03-9ad8-90d1245933ee","6562513d-69df-4b75-b23a-3c18fecbe692","f9d94116-98a7-4ff3-9c6b-9902a884f9e3","9d498318-0e2e-478b-b841-6f5f194c2191","c21fd623-e5de-44b5-9108-fc4cf3f8a816","5f566b2a-7124-4b46-8c14-efbb77252d71",
        "295f6b23-679c-4075-9c17-00c43a1902e9","5207cfd8-69e7-4255-80f2-19576d852e68","e31b4e2a-53e8-4862-b7e6-4f354a8323da","029b74b2-54e4-43bf-a653-c24e013fb1a6","33bcad48-4696-4923-9fd2-363848b765df","ee23858f-d4ce-49d0-818c-e9a5f332bb25","574ed1bf-cf94-49a5-aa12-b83469e19f0d","0b914479-b8f3-46ae-b282-b4cebc71c147","f54531ea-0461-4b10-9e94-dac37f1a70ea","259accab-e9b0-448b-90b2-1422b975bd5d","f8fb1bf7-8e87-42ef-9be9-11c2f7e65c09","c080446c-9e69-481d-a8ba-94e8f2697328","05799504-05ad-4d8a-bae2-a1f65f5af27a","fb90b5dd-5e4d-4248-b3e2-1afa9e35494f","f0c02971-75d4-41b7-b532-2715c756ac10","e995b4cb-44d0-462b-9e27-ef30d029bb75","a3071766-7614-4993-a311-a4145758cf11","405965e0-c8d0-47da-9cfa-ebf14b4a152c","21538dcc-3a56-4e7a-a5b0-542c4995971f","8526ffdb-c6f9-402f-a44e-85481ae66fe2","f14708e1-cb35-46ca-bade-d1650753580c","395ce48b-ada9-4dce-8298-73b3c2d8c548","0984c3c3-269c-431e-9df7-c42b609136d7","6fa78d69-2cc8-480f-8ec5-f06cd29f9155","51478321-fb2a-4e8a-8e5c-6bc2e6d0b177","2a4a26c9-5b5a-4960-9bee-0d7b5c132666","277ded4a-228f-4dcf-b64a-865bb9530710",
        "c8bcf0aa-d277-4474-9e8c-12b3099da7b2","f2e0c9d2-bc01-4484-9ab8-a1ae1a9b9e1c","c41ed1ad-fcea-4f73-9eff-fe4ef3a617cd","9dde1280-572d-4984-9147-691cc28352c2","1627c8f5-9211-48f5-b2e8-ea9771c559fb","7e8c071c-c490-407f-852b-1de9178e1d90","4b286947-37e3-41b6-82b7-c415f0397192","586ff74f-f221-4475-9e87-d4641edadedc","9eadbbd4-d95e-4aa7-a9fd-93915c520368","a03b4e6a-26f7-4cb8-aa47-c301b1c7f30c","f96b5456-250d-4426-b3e9-51379ddb3d63","3ff8d351-89d0-491e-ac78-05be5db5c7b2","6c9d77a1-608c-4b41-b5ff-f5d757c33231","9b4e1f00-b8b8-43b3-9c5f-63fe654394d9","3366919c-0517-4821-911d-0255a99c43c7","9b47d621-616f-4f04-a605-5cc7c1d9f94e","1e372dbf-86bd-4de3-be3b-183207d98564","20e5bcb1-b5c6-4ff1-abf4-81bd6e551f67","ef8a3a4f-117f-4550-afc1-ff8d2ecb9e95","c8164ac8-3d2a-4804-91b1-2f54f40ccef0","5bc28ac3-3648-4df9-a7d5-428c774ab835","ea189d40-f65c-41d2-bf7b-a67f69b9f35a","4e5216c0-7be2-4d65-ac84-4844d23bc49d","650376c3-03e9-4ca3-a58d-13da332f498b","9c3911b0-66ac-458a-9225-52a85e3930c5","03a92d7a-202e-4811-9870-7e1b1af01ef6","bf16a2df-4531-4086-81a2-456123d8e79e",
        "fc3e3f44-d985-44a7-8ccd-8982374a4b09","ec81ebbb-9b97-4302-a1fe-00ac9f927d78","43c95bdf-857e-4124-875b-ec6c8f527066","ea97e02e-8151-4bc0-b375-12d513e1d89b","b5dd4a14-7145-4611-9059-6ff2a3327d14","b05d704e-09de-4431-9a56-fc97e64d2dba","7218c326-7d5f-4e04-be94-f89e9ecae2da","5c76a8d3-6000-4c64-97e4-cb7d8adfa5a3","443ded41-ef90-4c64-851c-ae77a282d700","cf01ff33-ee1e-4f47-98e5-7228e676cd97","60428de0-341c-4b2a-88d8-56b4b1bcb931","e27e8c50-a279-4b5e-a5f6-8c2c1417fc1c","4cdbf337-6d7a-4ff4-b500-638dd0c26692","972cf97a-1861-4422-ba3a-78c039dfa6cc","a7c8e6b9-1d6c-4a99-8e9d-c6bff6d79497","b0ca0692-078b-4793-9091-2d34e5dd9aeb","14f441f9-7db9-45d2-af1d-cf0edd8e9a32","4c5122b7-8d46-4be1-a867-da2514a371f0","78436321-a87d-44bc-bf24-ae0632acdbbd","5ba96935-b73d-43e4-bba3-dd325261869a","91bad4a6-8522-49d6-bc94-52d7f91442dd","e3be9ef3-b71e-4842-bdd8-8c4f81071a55","66a6d5b8-d8bb-4abd-a83f-db3f8e0ab241","6ec46481-92c6-48df-ae79-8b4f1872f54b","0a94d862-6847-4a27-a040-94a9fdd5ad01","08675a7c-31ae-4103-a2f1-78523bcf62de","e52d82c7-bf99-4bdf-a81c-70ff8c1b8f79",
        "6de80c36-9b53-41ac-82e6-e84f3eff832e","4e1acb98-2196-4373-955f-da614c146986","f2e7cc49-f89b-4997-9cc3-d24ad127aec1","5f100fbd-a5fe-447c-803d-029df0a32eb4","d90baf15-1b8d-4228-b111-be18ced093e6","2e3f8530-b07d-44e1-b411-100bfc293be4","4c246343-5546-42e8-882a-3cdfb0404a84","347f52d1-775c-4322-9d3c-6f1a22269280","ee47ce46-344b-4f58-a8a8-fdd9643aa57b","8a8e14af-e7e3-4271-87ff-eed6c1b72403","ba9a7f7d-bf1f-432c-8da9-6d359a77eec3","b447048b-70e7-4b35-a247-dd88029f0535","eaf84560-017f-49cc-92e2-b45d54b8b9c7","5bfb0016-a5a3-4298-83a2-ab55156e714c","263cef7a-7ad0-451a-af17-ce914f997f42","11c252e7-3195-4c71-be8a-c1d767e151ba","56c4df89-a93b-4a9a-b47f-8549354d3039","3add3b8f-b648-47c1-b725-f1dc34a7882a","11d000bf-c2c6-4640-a635-70ce716e6cd3","d2c6baa0-4214-4a9c-b1a4-02db202424f7"]
, 'ideal_contribution': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,33.3333333333333,50,15,35,90,0,0,0,0,0,250,500,160,9,60,30,50,280,40,0,1260.62,4.65,0,3,25,13.09,120,25,45,50,10,15,10,20,20,40,30,50,30,20,0,200,200,0,60,20,15,20,30,20,0,350,50,100,200,0]
, 'max_amount': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,800,0,0,5000,0,200,0,0,0,0,0,50,150,0,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,400,500,100,300,1000,0,0,0,11065.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,50,0,0,0,800,800,500,100,150,100,250,300,500,300,500,300,300,0,2000,2000,0,400,200,150,250,300,300,0,0,0,0,0,0]
, 'savings_contr': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0.682539682539683,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
, 'fix_cat': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,0.5,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.8,0,0,0,0.9,0.9,0.5,0.8,0]
, 'cat_group_order': [14,14,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,8,8,8,8,8,8,8,8,8,8,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,9,9,9,9,9,9,9,9,9,9,9,13,5,5,5,5,5,5,8,8,8,7,7,7,7,2,2,2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,6,6,6,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,12]}

user_input = pd.DataFrame.from_dict(user_input_data)


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
#print (user_group_input)
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
ALL_active_month_cats = pd.concat([ALL_active_month_cats,ALL_active_month_savings])


ALL_active_month_cats['spending_this_month'] = np.where(ALL_active_month_cats['month']==this_month,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_this_month%'] = ALL_active_month_cats['spending_this_month']/ALL_active_month_cats['spending_this_month'].sum()*100
ALL_active_month_cats['spending_last_month'] = np.where(ALL_active_month_cats['month']==last_month,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_last_month%'] = ALL_active_month_cats['spending_last_month']/ALL_active_month_cats['spending_last_month'].sum()*100
ALL_active_month_cats['budgeting_this_month'] = np.where(ALL_active_month_cats['month']==this_month,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_this_month%'] = ALL_active_month_cats['budgeting_this_month']/ALL_active_month_cats['budgeting_this_month'].sum()*100
ALL_active_month_cats['budgeting_last_month'] = np.where(ALL_active_month_cats['month']==last_month,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_last_month%'] = ALL_active_month_cats['budgeting_last_month']/ALL_active_month_cats['budgeting_last_month'].sum()*100
ALL_active_month_cats['spending_this_month-1'] = np.where(ALL_active_month_cats['month']==last_month1,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['spending_this_month-2'] = np.where(ALL_active_month_cats['month']==last_month2,ALL_active_month_cats['activity'],0)
ALL_active_month_cats['budgeting_this_month-1'] = np.where(ALL_active_month_cats['month']==last_month1,ALL_active_month_cats['budgeted'],0)
ALL_active_month_cats['budgeting_this_month-2'] = np.where(ALL_active_month_cats['month']==last_month2,ALL_active_month_cats['budgeted'],0)
#print (ALL_active_month_cats.columns)
group_analysis = ALL_active_month_cats.groupby(['category_group_name'], as_index=False).sum()

group_analysis['spending_diff_mom'] = np.where(group_analysis['spending_last_month']==0,0,(group_analysis['spending_this_month']/group_analysis['spending_last_month']-1)*100)
#group_analysis['spending_diff_mom%'] = np.where(group_analysis['spending_last_month%']==0,0,group_analysis['spending_this_month%']/group_analysis['spending_last_month%'])
group_analysis['budgeting_diff_mom'] = np.where(group_analysis['budgeting_last_month']==0,0,(group_analysis['budgeting_this_month']/group_analysis['budgeting_last_month']-1)*100)
#group_analysis['budgeting_diff_mom%'] = np.where(group_analysis['budgeting_last_month%']==0,0,group_analysis['budgeting_this_month%']/group_analysis['budgeting_last_month%'])
group_analysis = pd.merge(group_analysis, user_group_input, on='category_group_name')
group_analysis['ideal_contribution%'] = group_analysis['ideal_contribution']/group_analysis['ideal_contribution'].sum()*100

group_analysis['spending_3m_diff'] = (group_analysis['spending_this_month']/((group_analysis['spending_last_month']+group_analysis['spending_this_month-1']+group_analysis['spending_this_month-2'])/3)-1)*100
#group_analysis['spending_3m_diff%']
group_analysis['budgeting_3m_diff'] = (group_analysis['budgeting_this_month']/((group_analysis['budgeting_last_month']+group_analysis['budgeting_this_month-1']+group_analysis['budgeting_this_month-2'])/3)-1)*100
#group_analysis['budgeting_3m_diff%']

group_analysis.sort_values(by=['cat_group_order'],inplace=True)

group_analysis.drop(['cat_group_order','savings_contr','fix_cat','max_amount','budgeting_this_month-2','budgeting_this_month-1','spending_this_month-2','spending_this_month-1','budgeted','activity','goal_target','balance'],axis=1,inplace=True)
group_analysis.reset_index(inplace=True)
group_analysis.fillna(0,inplace=True)
group_analysis.drop('index',axis=1,inplace=True)

# spending diff vs 3-month previous avg
# budgeting diff vs 3-month previous avg
# + Savings category extra

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
output = emoji_pattern.sub(r'', group_analysis.to_html())
output = output.replace(u'\U0001F3A2','')
output = output.replace(u'\U0001f7e1','')
output = output.replace(u'\U0001f9f7','')
output = output.replace(u'\U0001f9af','')
output = output.replace(u'\u26ea','')
output = output.replace(u'\U0001f7e2','')
text_file = open("YNAB_API_group_reporting.html", "w")
text_file.write(output)
text_file.close()


