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
print (filename)
with open(filename, "r") as file1:
    Lines = file1.readlines()
print (Lines[0])
token = Lines[0].strip()
budget_id = Lines[1].strip()

my_headers = {'Authorization' : f'Bearer {token}'}
response = requests.get(f'https://api.youneedabudget.com/v1/budgets/{budget_id}', headers=my_headers)
budget = response.json()
print (budget)
