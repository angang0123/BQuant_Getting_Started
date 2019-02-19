#*******************************Grouped Analysis**********************************

# Import the BQL and bqplot libraries
import bql
from bqplot import pyplot as plt

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Set the analysis universe to the members of the index
universe = bq.univ.members("SPX Index")

# Define a dictionary for the parameters
# that we will pass to all of the data items
# used in the analysis
params = {'currency' : 'USD', 
          'fa_period_reference' : bq.func.range('2006','2015'), 
          'fa_period_type' : 'Q', 
          'fa_period_year_end' : 'C'
}

# Define the debt data items,
# passing the parameters defined above
long_term_debt = bq.data.bs_lt_borrow(**params)
short_term_debt = bq.data.bs_st_borrow(**params)
# Calculate total debt from long- and short-term debt,
# using the znav function to return 0s for nulls values
tot_debt = bq.func.znav(long_term_debt + short_term_debt)
# Group and sum the total debt values by period end date
tot_debt_agg = bq.func.group(tot_debt, by = tot_debt['period_end_date']).sum()

# Define the assets data item,
# passing the parameters defined above
total_assets = bq.data.bs_tot_asset(**params)
# Group and sum the total asset values by period end date
tot_assets_agg = bq.func.group(total_assets, by = total_assets['period_end_date']).sum()

# Calculate the debt-to-assets ratio
grouped_leverage = tot_debt_agg / tot_assets_agg

# Generate the BQL request using index universe and ratio variable
request = bql.Request(universe, {"grouped_leverage": grouped_leverage})
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame
data = response[0].df()

# Use the pyplot API with the bqplot library to chart the result
plt.figure(title='S&P 500 Debt Ratio')
plt.plot(data['PERIOD_END_DATE'].dropna(), data['grouped_leverage'])
plt.axes(options={'x': {'label': 'Year', 
                                'grid_lines': 'solid'},
                  'y': {'label': 'Total Debt to Total Assets', 
                                'grid_lines': 'solid'}})
plt.show()





#***************Combining Historical and Estimate Data******************

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a list of securities for the query
securities = ['IBM US Equity', 'AAPL US Equity']

# Define the data item, passing the parameter overrides
sales_rev_turn = bq.data.sales_rev_turn(fa_period_offset=bq.func.range('-1', '3'),
                                       fa_period_type='A',
                                       as_of_date='2016-06-30') / 1000000000

# Generate the BQL request using security list and data item
request = bql.Request(securities, {"Sales in Billions" : sales_rev_turn})
# Execute the request
response = bq.execute(request)
# Convert the response to a dataframe
response[0].df()


'''
Point-in-Time Data 
The date and period parameters in BQL allows us to construct and interpret a true representation of point-in-time data. First, let's take a look at a few key terms:

AS_OF_DATE: The date when a given value was retrieved. This is particularly important when retrieving point-in-time data. With this override we're able to find specific values that were known at a specific date in the past. The AS_OF_DATE can either be before or after the PERIOD_END_DATE depending on whether we're looking at estimates or historical (reported) values.
FA_PERIOD_REFERENCE: The fiscal year and period which is the anchor for offset reference.
REVISION_DATE: The most recent date a given value was reported/revised/reiterated. It's important to note, especially with estimates, that the revision date could change often even though a given value didn't change from the previous period. Bloomberg consensus estimates are a composite of many different brokers. As such, if one of the brokers published a new report, and even if the estimate didn't change, the REVISION_DATE will change accordingly to reflect the new report date. The REVISION_DATE will be the same as or before the AS_OF_DATE.
PERIOD_END_DATE: The date associated with the accounting period for a given value. For most firms PERIOD_END_DATE are quarter end dates such as March 31, June 30, September 30 and December 31.
'''

#Example: Point-In-Time Historical Revenue
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the query security
security = 'IBM US Equity'

# Define the data item, passing the parameter overrides
sales = bq.data.sales_rev_turn(fa_period_reference='2014',
                               fa_period_type='A',
                               as_of_date='2016-06-30') / 1000000000

# Generate the BQL request using security variable and data item
request = bql.Request(security, {"Sales in Billions" : sales})
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame
response[0].df()



#Example: Historical Change in Forward Sales Estimates
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the query security
security = 'IBM US Equity'

# Define the data item, passing the parameter overrides
sales = bq.data.sales_rev_turn(fa_period_reference='2015-12-31',
                               fa_period_type='A',
                               fill='prev',
                               as_of_date=bq.func.range('2014-01-01','2015-12-31')) / 1000000000

# Generate the BQL request using security variable and data item
request = bql.Request(security, {"Sales in Billions" : sales})
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame and
# display the first 10 row to check the results
estimates_df = response[0].df()
estimates_df.head(10)


from bqplot import pyplot as plt
import numpy as np

plt.figure(title='IBM - Estimated Revenue (Bloomberg Consensus)')
plt.plot(estimates_df['AS_OF_DATE'], estimates_df['Sales in Billions'])
plt.axes(options={'x': {'label': 'Date (Jan 2014 to Dec 2015)', 
                                'grid_lines': 'solid'},
                  'y': {'label': 'Revenue (Billions)', 
                                'grid_lines': 'solid'}})

# Add a label to highlight the actual sales value of $81B.
plt.label(['12/31/15 Actual Sales $81.7B'], 
          x=[np.datetime64(estimates_df['AS_OF_DATE'].iloc[-400])], 
          y=[estimates_df['Sales in Billions'].iloc[-50]], 
          colors=['yellow'],
          scales={'x': plt._get_context_scale('x'), 
                  'y': plt._get_context_scale('y')})


plt.show()



#***********************Calendarization************************

#Calendar-Year and Fiscal-Year Sales

# Import the required libraries
import bql
from collections import OrderedDict

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the query security
security = 'MSFT US Equity'

# Define a data item for the calendar year sales values
calendar_year_sales = bq.data.sales_rev_turn(fa_period_year_end='C',
                                             fa_period_type='A',
                                             fa_period_reference=bq.func.range('2014', '2015')) / 1000000000

# Define a data item for the fiscal year sales values
fiscal_year_sales = bq.data.sales_rev_turn(fa_period_year_end='F',
                                           fa_period_type='A',
                                           fa_period_reference=bq.func.range('2014', '2015')) / 1000000000

# Create an ordered dictionary with the data items and labels
sales_fields = OrderedDict()
sales_fields["Sales Calendar in Billions"] = calendar_year_sales
sales_fields["Sales Fiscal in Billions"] = fiscal_year_sales

# Generate the BQL request using security variable
# and ordered dictionary
request = bql.Request(security, sales_fields)
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame
bql.combined_df(response)


#Quarterly Sales

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the query security
security = 'MSFT US Equity'

# Define a data item for quarterly sales
calendar_quarterly_sales = bq.data.sales_rev_turn(fa_period_type='Q',
                                                  fa_period_reference=bq.func.range('2013Q1', '2015Q4')) / 1000000000

# Generate the BQL request using security variable and data item
request = bql.Request(security, {"Quarterly Sales": calendar_quarterly_sales})
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame
df = response[0].df()
df


#Reconciliation

# Import the datetime library
import datetime

# Define start and end dates
start = datetime.date(2014, 1, 1)
end = datetime.date(2014, 12, 31)

# Set the index of the DataFrame to PERIOD_END_DATE
df = df.set_index('PERIOD_END_DATE')

# Use the pandas loc method with the
# start and end date labels to slice 
# the DataFrame on the index 
# and then sum the sliced values
df.loc[start:end].sum()


#Fundamentals in Different Currencies

# Import the required libraries
import bql
from collections import OrderedDict

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the query security
security = 'IBM US Equity'

# Define the sales data items, specifying a currency
sales_eur = bq.data.sales_rev_turn(currency='EUR') / 1000000000
sales_usd = bq.data.sales_rev_turn(currency='USD') / 1000000000

# Define the assets data items, specifying a currency
assets_eur = bq.data.bs_tot_asset(currency='EUR') / 1000000000
assets_usd = bq.data.bs_tot_asset(currency='USD') / 1000000000

# Create an ordered dictionary with the data items and labels
currency_fields = OrderedDict()
currency_fields["Sales in EUR"] = sales_eur
currency_fields["Sales USD"] = sales_usd
currency_fields["Assets in EUR"] = assets_eur
currency_fields["Assets USD"] = assets_usd

# Generate the BQL request using security variable and data item
request = bql.Request(security, currency_fields)
# Execute the request
response = bq.execute(request)
# Convert the response to a DataFrame
bql.combined_df(response)
