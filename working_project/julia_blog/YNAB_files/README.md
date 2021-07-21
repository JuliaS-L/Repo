# YNAB API 

* goals
* source
* setup
* unused but helpful links


## Goals
Pacing for current month



Bars Comparing Category Groups: 

in percentage and absolutes
* !!! Total savings category MUST be excluded from spending %
* Networth Report
*   allow notes to be added to months
* Income vs Expense Report 
* biggest payees in amount & transaction
* savings/needs/wants categorisation
* daily report/weekly/monthly for a single cat/cat group
* ability to report on a search criteria (hashtag, flag, etc eg for travels

Line chart for category groups over time

* in Percentages and Absolutes
* Spending over time
* Spending rolling averages over time
* Budgeting over time
* Budgeting rolling averages over time
    
Salary Planning

* Using ideal spend and latest contribution
* depending on user input of future expected income
* how should the funds be allocated
    * maintaining savings share (or increase to 55%)
    * keeping fix categories
* time to reach target balance in months with new contributions
* for weekly goals - left to spend should only include current weeks
* target should adjust to half weeks at the end
        
Budgeting Help

* use ideal spend
* adjust to availabe tbb
* adjust to allow setting monthly contribution with a fix max
* time to reach target balance in months with current contributions

Category groups

* set different category groups
* drag and drop into buckets
* give category group settings different names
* allow reporting drop down based on different groupings

Process for ingesting new categories

prompt user to enter against each category
    * an ideal amount
    * a fix %
    * a savings %
    * a need/want/save??
    
    
### Completed Goals    
Pacing
* ~~at this point in the month ~~
* ~~ideal spend ~~
* ~~my spend ~~
* ~~% of category spent ~~
* ~~absolute difference ~~
* ~~Excluding categories where activity=0, balance is 0 of category ~~
* ~~if category has a max_amount - pacing as % of max_amount ~~
*    ~~or set as fixed ~~
* ~~daily amount left in the category ~~
* ~~based on avg transaction amount in the category - number of transactions left? ~~
* ~~Avg transaction size recently vs longterm avg ~~

Bars Comparing Category Groups: 
* ~~spending this month ~~
* ~~spending last month ~~
* ~~budgeting this month ~~
* ~~budgeting last month ~~
* ~~Spending difference month-on-month ~~
* ~~Budgeting difference month-on-month ~~
* ~~Spending vs 3-month rolling avg ~~
* ~~Budgeting vs 3-month rolling avg ~~
* ~~Ideal Monthly contribution ~~
* ~~savings category based on user input ~~

## Source
currently using my own authentification - need to change ot OAuth

##Setup
my_headers = {'Authorization' : 'Bearer token'}

response = requests.get('https://api.youneedabudget.com/v1/budgets/budget_id', headers=my_headers)

https://api.youneedabudget.com/v1

#unused lines

accounts = pd.DataFrame(columns=['id', 'name', 'type', 'on_budget', 'closed', 'note', 'balance', 'cleared_balance', 'uncleared_balance', 'transfer_payee_id', 'deleted'])

subtransactions = pd.DataFrame(columns=['id', 'transaction_id', 'amount', 'memo', 'payee_id', 'category_id', 'transfer_account_id', 'deleted'])

scheduled_transactions = pd.DataFrame(columns=['id', 'date_first', 'date_next', 'frequency', 'amount', 'memo', 'flag_color', 'account_id', 'payee_id', 'category_id', 'transfer_account_id', 'deleted'])

print (budget.keys())
