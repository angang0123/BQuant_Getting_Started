'''

if(px_last > px_bid, px_last,px_bid

not(px_last == px_high)

znav(eqy_dvd_yld_12m)

avail(bdvd_proj_12m_yld, eqy_dvd_yld_12m)
'''

#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string to return the last traded price if the last trade 
# is higher than the trailing 10D average price,
# otherwise return the text 'Below 10D Average'
request = "get(if(px_last > avg(px_last(-10D)), px_last, 'Below 10D Average')) for(MEMBERS('INDU Index'))"

# Execute the request
response = bq.execute(request)

# Display the response in a data frame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the data fields
px_last = bq.data.px_last()
date_range = bq.func.range('-10D','0D')
px_avg = bq.data.px_last(start='-10D').avg()

# Define the universe 
univ = bq.univ.members('INDU Index')

# Define the if clause to return the last traded price if the last trade 
# is higher than the trailing 10D average price,
# otherwise return the text 'Below 10D Average'
return_if = bq.func.if_((px_last > px_avg), px_last, 'Below 10D Average')

# Execute the request 
request = bql.Request(univ, return_if)
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
