'''
Start and End Dates
The dates parameter and range function allow you to retrieve a time series of historical data points.

Syntax

String Interface
get(field(dates=RANGE(YYYY-MM-DD, YYYY-MM-DD))) for (['Ticker'])

Object Model
date_range = bq.func.range('YYYY-MM-DD', 'YYYY-MM-DD')
bq.data.field(dates=date_range)
'''


#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string with the date range
request = "get(DROPNA(PX_LAST(dates=RANGE(2018-01-01,2018-01-10)))) for(['IBM US Equity'])"

# Execute the request
response = bq.execute(request)

# Display the response in a data frame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the date range
date_range = bq.func.range('2018-01-01','2018-01-10')

# Define the request ticker, start, and end date
px_last = bq.data.px_last(dates=date_range)
px_last_dropped_na = bq.func.dropna(px_last)
ticker = 'IBM US Equity'

# Execute the request
request = bql.Request(ticker, px_last_dropped_na)
response = bq.execute(request)

# Display the response in a data frame
response[0].df()
