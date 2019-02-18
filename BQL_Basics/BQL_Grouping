#Example A: Grouping

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the security universe
univ = ['WMT US Equity', 'PG US Equity', 'KO US Equity']

# Define a data item for fcf yield
fcf_yield = bq.data.free_cash_flow_yield(fill='prev')

# Define a data item for average fcf yield for the group
#=======================================================================
#avg_fcf_yield = bq.data.free_cash_flow_yield(fill='prev').group().avg()

# Generate the request using the universe variable and data item
request =  bql.Request(univ, fcf_yield)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()


#Grouping by Sector
'''
univ = bq.univ.members('INDU Index')

# Define a data item for the grouping field
grouping_item = bq.data.gics_sector_name()

# Define a data item for the average fcf yield, passing the
# grouping field as a parameter to the group() function
avg_fcf_yield = bq.data.free_cash_flow_yield(fill='prev').group(grouping_item).avg()
# Define a dictionary to modify the column name
avg_fcf_yield_dict = {'Average Free Cash Flow Yield': avg_fcf_yield}

# Generate the request using the universe variable and dictionary
request =  bql.Request(univ, avg_fcf_yield_dict)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
'''



#Example B: Operation-Specific Grouping
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the security universe
univ = bq.univ.members('INDU Index')

# Define a data item for the grouping field
grouping_item = bq.data.gics_sector_name()

# Define a data item for the average fcf yield, passing 
# the grouping field as a parameter to the groupavg() 
# function to return the average values of for the 
# individual members of the universe
avg_fcf_yield = bq.data.free_cash_flow_yield(fill='prev').groupavg(grouping_item)
# Define a dictionary to modify the column name
avg_fcf_yield_dict = {'Average Free Cash Flow Yield': avg_fcf_yield}

# Generate the request using the universe variable and dictionary
request =  bql.Request(univ, avg_fcf_yield_dict)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame, because yield is stored in dictionary format
response[0].df()



#Example C: Multiple Levels of Grouping
# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define a variable for the security universe
univ = bq.univ.members('BE500 Index')

# Define datas item for the two grouping fields
grouping_item_1 = bq.data.gics_sector_name()
grouping_item_2 = bq.data.country_full_name()

# Define a data item for the market cap sum, passing the
# grouping fields as parameters to the group() function
grouped_data = bq.data.cur_mkt_cap(currency='EUR').group([grouping_item_1,grouping_item_2]).sum()
# Define a dictionary to modify the column name
grouped_data_dict = {'Market Cap': grouped_data}

# Generate the request using the security variable and dictionary
request =  bql.Request(univ, grouped_data_dict)

# Execute the request
response = bq.execute(request)

# Display the response in a DataFrame
response[0].df()
