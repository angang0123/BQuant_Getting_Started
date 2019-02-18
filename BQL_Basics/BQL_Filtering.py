#Example A: Filtering an Index
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a starting universe
start_univ = bq.univ.members('MXWO Index')

# Define the filter criteria

# Market Cap greater than or equal to 50B
criteria_1 = bq.data.cur_mkt_cap(currency='USD') >= 50*10**9

# Market Cap less than or equal to 60B
criteria_2 = bq.data.cur_mkt_cap(currency='USD') <= 60*10**9

# P/E Ratio below the sector average
sector = bq.data.gics_sector_name()
pe_ratio = bq.data.pe_ratio()
sector_avg_pe_ratio = pe_ratio.groupavg(sector)
criteria_3 = pe_ratio < sector_avg_pe_ratio

#*********************Create a list of the criteria using the and_() function*****************************
criteria_list = bq.func.and_(criteria_1,criteria_2).and_(criteria_3)

# Define the filtered universe
filtered_univ = bq.univ.filter(start_univ, criteria_list)

# Define a data item to return with the security results
mkt_cap = bq.data.cur_mkt_cap(currency='USD')

# Generate the request using the filtered universe and data item
request =  bql.Request(filtered_univ, mkt_cap)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()



#Example B: Filtering an Issuer's Bonds
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a starting universe
start_univ = bq.univ.bonds(['IBM US Equity'])

# Define the filter criteria
criteria_1 = bq.data.cpn_typ() == 'FIXED'
criteria_2 = bq.data.payment_rank() == 'Sr Unsecured'

# Create a list of the criteria using the and_() function
criteria_list = bq.func.and_(criteria_1,criteria_2)

# Define the filtered universe
filtered_univ = bq.univ.filter(start_univ, criteria_list)

# Define a data item to return with the security results
coupon = bq.data.cpn()

# Generate the request using the filtered universe and data item
request =  bql.Request(filtered_univ, coupon)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
