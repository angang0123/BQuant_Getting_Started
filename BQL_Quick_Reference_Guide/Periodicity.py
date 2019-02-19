'''

Periodicity
The per parameter allows you to set the interval within a fixed period of time for a data request.

Syntax

String Query
get(field(dates=RANGE(YYYY-MM-DD, YYYY-MM-DD),per='M')) for (['ticker'])

Object Model
bq.data.field(dates=date_range, per='M')


Reference
per = D/W/M/Q/S/Y
'''



#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string
request = "get(DROPNA(PX_LAST(dates=RANGE(2017-01-01, 2017-12-31), per='M', fill='prev'))) for (['IBM US Equity'])"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request object with the periodicity and fill value
date_range = bq.func.range('2017-01-01', '2017-12-31')
last = bq.data.px_last(dates=date_range, per='M', fill='prev')
last_dropped_na = bq.func.dropna(last)
ticker = 'IBM US Equity'

# Execute the request
request = bql.Request(ticker, last_dropped_na)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
