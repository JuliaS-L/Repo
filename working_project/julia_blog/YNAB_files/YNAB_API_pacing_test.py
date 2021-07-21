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
print(os.getcwd())
path_parent = os.path.dirname(os.getcwd())

print (path_parent+'/templates')
#path_parent = path_parent+"./Tableau-Outputs/{0} Bupa".format(lastMonth_title)
print(os.getcwd())