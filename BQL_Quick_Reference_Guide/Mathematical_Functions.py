'''
abs(best_target_price - px_last)
sign(best_target_price - px_last)
floor(px_last)
ceil(px_last)
square(px_ask - px_bid)
sqrt(px_ask - px_bid)
mod(px_last,7)
ln(px_last/px_last(start=-1D,end=-1D)-1)
log(px_last/px_last(start=-1D,end=-1D)-1)
pow(px_ask - px_bid,2)
exp(px_last)
'''

#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string to return the power of 
# the bid-ask spread for the members of the INDU Index 
request = "get(pow(px_ask - px_bid,2)) for (MEMBERS('INDU Index'))"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the fields 
px_ask = bq.data.px_ask()
px_bid = bq.data.px_bid()

# Define the universe 
univ = bq.univ.members('INDU Index')

# Define the request object to return the power of 
# the bid-ask spread for the members of the INDU Index
power = bq.func.pow(px_ask-px_bid, 2) 

# Execute the request 
request = bql.Request(univ, power)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
