'''
COUNT(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
MIN(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
MAX(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
AVG(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
MEDIAN(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
STD(px_last(dates=RANGE(2014-01-01, 2014-12-31)))
RSQUARE(px_last(dates=RANGE(2014-01-01, 2014-12-31)), px_last(dates=RANGE(2014-01-01, 2014-12-31)))
STDERR(px_last(dates=RANGE(2014-01-01, 2014-12-31)), px_last(dates=RANGE(2014-01-01, 2014-12-31)))
CORREL(px_last(dates=RANGE(2014-01-01, 2014-12-31)), px_last(dates=RANGE(2014-01-01, 2014-12-31)))
PCT_CHANGE(px_last(dates=RANGE(2014-01-01, 2014-12-31), fill=prev, frq=d))
'''


#String Interface Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the request string to return the lowest value of px_last 
# for the specified date range for the members of the INDU Index
request = "get(MIN(px_last(dates=RANGE(2016-01-01, 2017-12-31)))) for (MEMBERS('INDU Index'))"

# Execute the request
response = bq.execute(request)

# Display the response in a data frame
response[0].df()



#Object Model Example

# Import the BQL library
import bql

# Instantiate an object to interface with the BQL service
bq = bql.Service()

# Define the field: PX_LAST the start and end dates 
date_range = bq.func.range('2016-01-01', '2017-12-31')
px_last = bq.data.px_last(dates=date_range)

# Define the universe 
univ = bq.univ.members('INDU Index')

# Define the request object to return the lowest value of px_last 
# for the specified date range for the members of the INDU Index
func_max = bq.func.min(px_last) 

# Execute the request 
request = bql.Request(univ, func_max)
response = bq.execute(request)

# Display the response in a data frame
response[0].df()
