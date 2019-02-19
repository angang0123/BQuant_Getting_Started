'''
Relative Dates
You can use relative date values with the range function to construct flexible data sets with dates that are relative to specific points in time.

Syntax

String Interface
get(field(dates=RANGE(relative_start_date, relative_end_date), per='Periodicity')) for (['ticker'])

Object Model
date_range = bq.func.range('relative_start_date', 'relative_end_date')
bq.data.field(dates=date_range, per='Periodicity')
'''



#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string with the relative dates
request = "get(PX_LAST(dates=RANGE(-2Y,0D),per='Q')) for (['VOD LN Equity'])"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request object with the relative date 
date_range = bq.func.range('-2Y','0D')
last = bq.data.px_last(dates=date_range, per='Q')
ticker = 'VOD LN Equity'

# Execute the request
request = bql.Request(ticker, last)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
