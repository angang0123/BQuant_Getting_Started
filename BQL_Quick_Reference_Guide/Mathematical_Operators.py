'''
Syntax

String Interface
get((field1-field2)) for (['ticker'])

Object Model
field1 = bq.data.field1
field2 = bq.data.field2
spread = field1 - field2
'''


#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with th BQL service
bq = bql.Service()

# Define the request string to calculate the bid/ask spread 
request = "get((PX_ASK()-PX_BID())) for (['GE US Equity'])"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# define the data fields and use mathematical operators 
# to calculate the bid/ask spread 
ask = bq.data.px_ask()
bid = bq.data.px_bid()
spread = ask - bid

# Define the security
tickers = 'GE US Equity'

# Execute the request 
request = bql.Request(tickers, spread)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
