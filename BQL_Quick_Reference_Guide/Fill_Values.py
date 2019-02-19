'''
Fill Values
The Fill parameter allows you to apply a specified replacement when a requested value is not available.

Syntax
String Interface
get(field(dates=RANGE(YYYY-MM-DD, YYYY-MM-DD),fill='next')) for (['ticker'])
Object Model

bq.data.field(dates=date_range, fill='next')

********Reference*********
Filler Value	Example	
Last available value	fill=prev	
Next available value	fill=next	
NA	fill=na	(default)

'''

#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string and fill Value 
request = "get(PX_LAST(dates=RANGE(2018-01-01,2018-01-10), fill='prev')) for (['EBAY US Equity'])"

# Execute the request
response= bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request object and the fill value
date_range = bq.func.range('2018-01-01', '2018-01-10')
field =  bq.data.px_last(dates=date_range, fill='next')
ticker = 'EBAY US Equity'

# Execute the request
request = bql.Request(ticker, field)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
