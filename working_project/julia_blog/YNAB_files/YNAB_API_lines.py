import json
from pprint import pprint
from datetime import datetime
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from dateutil.relativedelta import relativedelta
import requests
from YNAB_API_GroupReporting import ALL_active_month_cats,user_group_input,emoji_pattern
from YNAB_API_pacing import budget,categories,transactions,months,category_groups,user_input,today,active_months
import webbrowser
pd.options.display.max_rows = 99
pd.options.display.max_columns = 999
pd.options.display.float_format = '{:,.2f}'.format
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 1000)
ALL_active_month_cats = ALL_active_month_cats.groupby(['category_group_name','month'], as_index=False).sum()
ALL_active_month_cats = ALL_active_month_cats.loc[(ALL_active_month_cats['budgeted']> 0) | (ALL_active_month_cats['activity']>0)]
ALL_active_month_cats = pd.merge(ALL_active_month_cats, user_group_input, on='category_group_name')
ALL_active_month_cats.sort_values(by=['cat_group_order','month'],inplace=True)
ALL_active_month_cats = ALL_active_month_cats.loc[:, ['category_group_name','month','budgeted','activity']]
ALL_active_month_cats['activity'] = ALL_active_month_cats['activity']*-1
ALL_active_month_cats_spending = ALL_active_month_cats.loc[(ALL_active_month_cats['activity']>0)]
ALL_active_month_cats_budgeting = ALL_active_month_cats.loc[(ALL_active_month_cats['budgeted']>0)]

months  = ALL_active_month_cats_spending['month'].tolist()
groups  = set(ALL_active_month_cats_spending['category_group_name'].tolist())

#https://canvasjs.com/javascript-charts/multi-series-line-chart/

html_file = """<!DOCTYPE HTML><html><head><script>window.onload = function () {var chart = new CanvasJS.Chart("chartContainer", {
	title: {text: "Spending over time"},axisX: {valueFormatString: "MMM YYYY"},
	axisY: {title: "Amount Spent",prefix: "",suffix: ""},toolTip: {shared: true},legend: {cursor: "pointer",verticalAlign: "top",horizontalAlign: "center",dockInsidePlotArea: true,itemclick: toogleDataSeries},
	data: ["""
for x in groups:
    html_file += """
	{type:"line",axisYType: "primary",name: """
    html_file += "'"
    html_file += x
    html_file +="'"
    html_file += """,showInLegend: true,markerSize: 0,yValueFormatString: "",dataPoints: 
	["""
    for y in months:
        html_file += """
	        { x: new Date("""
        html_file += str(y[:4])
        html_file += ", "
        html_file += str(int(y[5:7])-1)
        html_file += ", 01), y: "
        if len(ALL_active_month_cats_spending['activity'].loc[((ALL_active_month_cats_spending['category_group_name'] == x)&(ALL_active_month_cats_spending['month']==y))].tolist())==0:
            html_file += "0"
        else:
            html_file += str(abs(ALL_active_month_cats_spending['activity'].loc[((ALL_active_month_cats_spending['category_group_name'] == x)&(ALL_active_month_cats_spending['month']==y))].tolist()[0]))
        html_file += "},"
    html_file += "]},"
html_file += """]});chart.render();function toogleDataSeries(e){
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;} else{e.dataSeries.visible = true;}chart.render();}}
</script></head><body><div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script></body></html>"""

output = emoji_pattern.sub(r'', html_file)
output = output.replace(u'\U0001F3A2','')
output = output.replace(u'\U0001f7e1','')
output = output.replace(u'\U0001f9f7','')
output = output.replace(u'\U0001f9af','')
output = output.replace(u'\u2016','')
output = output.replace(u'\u26ea','')
output = output.replace(u'\U0001f7e2','')

path_parent = os.path.dirname(os.getcwd())
text_file = open(path_parent+"/templates/YNAB_API_lines_S.html", "w")
text_file.write(output)
text_file.close()



months  = ALL_active_month_cats_budgeting['month'].tolist()
groups  = set(ALL_active_month_cats_budgeting['category_group_name'].tolist())

#https://canvasjs.com/javascript-charts/multi-series-line-chart/

html_file = """<!DOCTYPE HTML><html><head><script>window.onload = function () {var chart = new CanvasJS.Chart("chartContainer", {
	title: {text: "Budgeting over time"},axisX: {valueFormatString: "MMM YYYY"},
	axisY: {title: "Amount Budgeted",prefix: "",suffix: ""},toolTip: {shared: true},legend: {cursor: "pointer",verticalAlign: "top",horizontalAlign: "center",dockInsidePlotArea: true,itemclick: toogleDataSeries},
	data: ["""
for x in groups:
    html_file += """
	{type:"line",axisYType: "primary",name: """
    html_file += "'"
    html_file += x
    html_file +="'"
    html_file += """,showInLegend: true,markerSize: 0,yValueFormatString: "",dataPoints: 
	["""
    for y in months:
        html_file += """
	        { x: new Date("""
        html_file += str(y[:4])
        html_file += ", "
        html_file += str(int(y[5:7])-1)
        html_file += ", 01), y: "
        if len(ALL_active_month_cats_budgeting['activity'].loc[((ALL_active_month_cats_budgeting['category_group_name'] == x)&(ALL_active_month_cats_budgeting['month']==y))].tolist())==0:
            html_file += "0"
        else:
            html_file += str(abs(ALL_active_month_cats_budgeting['activity'].loc[((ALL_active_month_cats_budgeting['category_group_name'] == x)&(ALL_active_month_cats_budgeting['month']==y))].tolist()[0]))
        html_file += "},"
    html_file += "]},"
html_file += """]});chart.render();function toogleDataSeries(e){
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;} else{e.dataSeries.visible = true;}chart.render();}}
</script></head><body><div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script></body></html>"""

output = emoji_pattern.sub(r'', html_file)
output = output.replace(u'\U0001F3A2','')
output = output.replace(u'\U0001f7e1','')
output = output.replace(u'\U0001f9f7','')
output = output.replace(u'\U0001f9af','')
output = output.replace(u'\u2016','')
output = output.replace(u'\u26ea','')
output = output.replace(u'\U0001f7e2','')

path_parent = os.path.dirname(os.getcwd())
text_file = open(path_parent+"/templates/YNAB_API_lines_B.html", "w")
text_file.write(output)
text_file.close()
