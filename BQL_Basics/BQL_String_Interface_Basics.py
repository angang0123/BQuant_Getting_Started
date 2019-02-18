#Example A: Requesting a Single Data Item 
#=============================================================================
'''
Request syntax:
  `get(data fields)for([security or universe])`
BQL execute function:
  `bq.execute(request)`
  
'''

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string 
request = "get(PX_LAST)for(['AAPL US Equity'])"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Example B: Requesting Multiple Data Items
#=============================================================================
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string
request = """
get(PX_LAST, PX_HIGH, PX_LOW)
for(['AAPL US Equity'])
"""

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
# Use the combined_df function to display the three returned values in a single DataFrame 
bql.combined_df(response)

# Note that you can also display a single data item from the response 
# by running response[0].df(), response[1].df(), or response[2].df(),



#Example C: Requesting Time Series and Point-In-Time Data
#=============================================================================
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string, specifying the date range for each field
# Since we're using the same range for all of the fields, we can use
# a BQL let clause to define a local variable 
request = """
let(
    #date_range = RANGE(2017-06-05, 2017-06-09);
    )
get(
    PX_LAST(dates=#date_range),
    PX_HIGH(dates=#date_range), 
    PX_LOW(dates=#date_range)
    )
for(
    ['AAPL US Equity']
    )
"""

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
# Use the combined_df function to display 
# the three returned values in a single DataFrame 
bql.combined_df(response)



#Example D: Requesting Data for Multiple Securities
#=============================================================================
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string, specifying the date range for each field
# Since we're using the same range for all of the fields, we can use
# a BQL let clause to define a local variable 
request = """
let(
    #date_range = RANGE(2017-06-05, 2017-06-09);
    )
get(
    PX_LAST(dates=#date_range),
    PX_HIGH(dates=#date_range), 
    PX_LOW(dates=#date_range)
    )
for(
    ['AAPL US Equity', 'AMZN US Equity', 'TSLA US Equity']
    )
"""

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
# Use the combined_df function to display 
# the three returned values in a single DataFrame
# To verify the output, use tail(3) to show the last three rows of the response
bql.combined_df(response).tail(3)
