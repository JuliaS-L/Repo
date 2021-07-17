import json
from pprint import pprint
from datetime import datetime
import pandas as pd
import calendar
import numpy as np
import re

from dateutil.relativedelta import relativedelta
import requests
from io import StringIO
pd.options.display.max_rows = 99
pd.options.display.max_columns = 999
pd.set_option('display.width', 1000)


today = datetime.now().strftime("%Y-%m-01")
date_after_month = datetime.today()+ relativedelta(months=-1)
date_after_month = date_after_month.strftime("%Y-%m-01")
print (today)
print (date_after_month)