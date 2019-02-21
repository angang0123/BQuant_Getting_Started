'''
list(['VOD LN Equity', 'RBS LN Equity', 'SBRY LN Equity'])
members('UKX Index')
bonds('VOD LN Equity')
loans('TSCO LN Equity')
'''


#String Interface Example (Equity)

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()
 
# Define the request string to return PX_LAST for 
# for all members of the INDU Index
request = "get(PX_LAST) for (MEMBERS('INDU Index'))"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example (Equity)

# Import the BQL library 
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the a data field 
price = bq.data.px_last() 

# Use the members function to define the universe
# as all members of the INDU Index 
univ = bq.univ.members('INDU Index')

# Define the request 
request = bql.Request(univ, price)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#String Interface Example (Fixed Income)

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a request string to the IDs, coupon 
# and coupon type for all VOD LN bonds
request = "get(CPN) for (Bonds(['VOD LN Equity']))"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example (Fixed Income)

# Import the BQL library and Datetime
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the data item for the request
coupon = bq.data.cpn()

# Define a universe for all VOD LN bonds
univ = bq.univ.bonds('VOD LN Equity')

# Execute the request
request = bql.Request(univ, coupon)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
