'''
Syntax
String Interface
get(ID) for (filter (MEMBERS('ticker'), (PX_LAST >= X )))"
Object Model
criteria = bq.data.px_last() >= 100 
filtered_univ = bq.univ.filter(univ, criteria)
'''

#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string filtering to only return results
# that have a PX_LAST value greater than or equal to 100
request = "get(PX_LAST) for (filter( MEMBERS('INDU Index'), (PX_LAST >= 100)))"

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

#Set the Field 
price = bq.data.px_last()

# Set the universe and the function 
univ = bq.univ.members('INDU Index')

# Define and apply the filter criteria to only return results
# that have a PX_LAST value greater than or equal to 100
criteria = bq.data.px_last() >= 100 
filtered_univ = bq.univ.filter(univ, criteria)

# Execute the request 
request = bql.Request(filtered_univ, price)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
