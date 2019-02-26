'''
Factor Scoring Model
Factor scoring in BQuant allows you to create flexible, dynamic factors using 
the Bloomberg Query Language (BQL) service to access Bloomberg data, so that you 
can easily automate scoring models to increase coverage and focus on interesting companies.
'''


'''
Part 1. Creating the Model
1.1 Importing Required Libraries
First, we will import the modules needed to create the scoring model.
'''

# Import the Bloomberg Query Language (BQL) library, which allows you 
# to access fundamentals and universe data
import bql

# Import the pandas and numpy libraries as well as the partial class, which are used to 
# create and manipulate data structures, as well as to perform mathematical operations
import pandas as pd
import numpy as np
from functools import partial
from collections import OrderedDict

# Import bqplot, bwidgets, and ipywidgets, which are used for visualizing results
from bqplot import Axis, LinearScale, OrdinalScale, Scatter, Figure, Tooltip
from bqwidgets import DataGrid
from ipywidgets import VBox, HBox, Dropdown, Button, Layout
from IPython.display import display

# Instantiate an object to interface with the BQL service
bq = bql.Service()


'''
1.2 Defining Factors
Now that we've imported our libraries, we will define and analyze the factors that will be used in the scoring model. 
The factors are defined in dictionaries in the cell below, and each factor has 2 parts:

Expression: The BQL data item or custom expression for the factor
Weight: The weight of the factor in the composite score
In addition, we will define analytical functions to control outliers or transform data into a standardized analytic, like a zscore.
'''

# Define analytical functions to control the BQL data that is downloaded

# analytics: zscore
def zscore(factor):
    grouped_factor = bq.func.group(factor)
    avg = bq.func.ungroup(bq.func.avg(bq.func.dropna(grouped_factor)),ungroupOrder='current')
    std = bq.func.ungroup(bq.func.std(bq.func.dropna(grouped_factor)),ungroupOrder='current')
    return (factor - avg) / std

# analytics: winsorize
def winsorize(factor, limit):
    lower_bound = -1 * limit
    upper_bound = limit
    return bq.func.if_(factor >= upper_bound, upper_bound, 
                bq.func.if_(factor <= lower_bound, lower_bound, factor))

# Define parameters for the factors
params ={'dates':'-1Y','fill':'PREV','Currency':'USD'}

# Define the factors to be used in the model
factor_model = {
    "Value Model": {
        "FCF Yield": {
                "expression":winsorize(zscore(bq.data.cf_free_cash_flow()/bq.data.px_last()),3), 
                "weights": 0.2
            },
         "Earnings Yield": {
                "expression":winsorize(zscore(bq.data.is_eps()/bq.data.px_last()),3), 
                "weights": 0.3
            },
         "Leverage": {
                "expression":winsorize(zscore(1/bq.data.tot_debt_to_ebitda()),3), 
                "weights": 0.3
            },
         "Profitability": {
                "expression":winsorize(zscore(bq.data.net_income()/bq.data.sales_rev_turn()),3),  
                "weights": 0.2
            }
    },
    "Growth Model": {
        "EBITDA Growth": {
                "expression":winsorize(zscore(bq.data.ebitda_growth()),3), 
                "weights": 0.2
            },
         "Sales Growth": {
                "expression":winsorize(zscore(bq.data.sales_growth()),3), 
                "weights": 0.3
            },
         "Leverage": {
                "expression":winsorize(zscore(1/bq.data.tot_debt_to_ebitda()),3), 
                "weights": 0.3
            },
         "Profitability": {
                "expression":winsorize(zscore(bq.data.net_income()/bq.data.sales_rev_turn()),3), 
                "weights": 0.2
            }
    }
}

# Define factor mappings to be used in dropdown menus
model_list = list(factor_model.keys())


'''
1.3 Defining a Universe
Next, we'll define the different universes for which we want to score. 
For this example, we'll use a retail peer group and the Dow Jones Index.
'''

# Define universe mappings to be used in dropdown menus
universe = {
    "Universe 1": list(['MRW LN Equity','MGNT RM Equity','SBRY LN Equity',
                        'ICA SS Equity','FIVE LI Equity','JMT PL Equity']),
    "Universe 2": bq.univ.members('INDU Index') ,         
}

univ_list = list(universe.keys())



'''
Part 2. Creating the Model Outputs
Now that we have defined our factors and security universe, we can put them together 
to see how the companies performed on our scoring model. We will use Bloomberg's 
visualization library bqplot to create a chart, and Bloomberg's bqwidget package to 
create a create an interactive table of the companies.

2.1 Creating the Final Score
'''

# Define a function to extract data for the scoring model using the Factors create above
# This function contains the business logic to calculate an aggregate score for the factors
def get_data(analysis_universe, factors, parameters):
    factor_dict = OrderedDict()
    weights_df = pd.DataFrame()
    for x,y in factor_model[factors].items():
        factor_dict[x] = y['expression']
        weights_df = weights_df.append(pd.DataFrame({'name':[x],'weights':[y['weights']]}))
     # Create the request
    weights_df = weights_df.set_index('name')
    request = bql.Request(universe.get(analysis_universe), factor_dict, with_params=parameters)
    # Execute the request object.
    response = bq.execute(request)
    # Return a combined DataFrame.
    response_df_concat = pd.concat([item.df() for item in response],axis=1)
    # Calculate aggregate score and then create a percent rank
    output_df = response_df_concat[list(factor_dict)].fillna(value=0)
    output_df['Factor Score'] = output_df.dot(weights_df)
    output_df['% Rank'] = output_df['Factor Score'].rank(pct=True).fillna(value=0)

    return output_df
    
    
#2.2 Visualization Class    

# Define a class to control the visualization and user interface
class FactorVisualization:
    def __init__(self):
        # Initialize the chart with a default ticker
        self.data_chart = pd.DataFrame()
        self.chart_dropdown_x = Dropdown(description='X-Axis',layout=Layout(width='380px'))
        self.chart_dropdown_y = Dropdown(description='Y-Axis',layout=Layout(width='380px'))
        
        self.x_sc = LinearScale()
        self.y_sc = LinearScale()  
        self.tt = Tooltip(fields=['name','x', 'y'], formats=['', '.2f','.2f']) 
        self.scatter = Scatter(scales= {'x': self.x_sc, 'y': self.y_sc}, colors=['dodgerblue'],
                        tooltip=self.tt, unhovered_style={'opacity': 0.5})

        self.ax_x = Axis(scale=self.x_sc)
        self.ax_y = Axis(scale=self.y_sc, orientation='vertical', tick_format='0.2f')        
        self.fig = Figure(marks=[], axes=[self.ax_x, self.ax_y],
                          animation_duration=1000,
                          padding_x=0,layout = {'width':"100%",'height':"500px"})
        
        self.data_grid = DataGrid(layout = {'width':"720px",'height':"200px"})
        
        self.box = VBox([HBox([self.fig]),
                         HBox([self.chart_dropdown_x,self.chart_dropdown_y])
                        ])
        
        display(self.box)
    
    # Define a method to update scatter chart
    def plot_scatter(self, x_data, y_data, label_data,x_name,y_name):
        distance_x = max(x_data) - min (x_data)
        distance_y = max(y_data) - min (y_data)
        self.x_sc.min = min (x_data) - (distance_x)/10
        self.x_sc.max = max(x_data) + (distance_x)/10
        self.y_sc.min = min (y_data) - (distance_y)/10
        self.y_sc.max = max(y_data) + (distance_y)/10
        self.x_data = x_data
        self.y_data = y_data
        self.label_data = label_data
        self.tt.labels=['Company',x_name,y_name]
        self.scatter.x = x_data
        self.scatter.y = y_data
        self.scatter.names = label_data
        self.fig.title = "Scatter Chart: " + x_name + "  v " + y_name
        self.ax_x.label = x_name
        self.ax_y.label = y_name
        self.fig.marks = [self.scatter]
    
    # Define a method to control default chart state
    def populate_default_chart(self,df):
        self.data_chart = df
        options_list = list(df.columns)
        options_list.append(' ')
        self.chart_dropdown_x.options = options_list
        self.chart_dropdown_y.options = options_list
        self.chart_dropdown_x.value =  options_list[0] 
        self.chart_dropdown_y.value =  options_list[1]
        x_data = df[df.columns[0]].values
        y_data = df[df.columns[1]].values
        label_data = df[df.columns[0]].index
        self.plot_scatter(x_data,y_data,label_data,list(df.columns)[0],list(df.columns)[1])
        self.chart_dropdown_x.observe(self.on_change)
        self.chart_dropdown_y.observe(self.on_change)
    
    # Define a handler for axis changes on chart
    def on_change(self,change):
        if change['type'] == 'change' and change['name'] == 'value':
            if self.chart_dropdown_x.value == ' ' or self.chart_dropdown_y.value == ' ':
                pass
            else:
                x_data = self.data_chart[self.chart_dropdown_x.value].values
                y_data = self.data_chart[self.chart_dropdown_y.value].values
                label_data = self.data_chart[self.data_chart.columns[0]].index
                self.plot_scatter(x_data,y_data,label_data,self.chart_dropdown_x.value,self.chart_dropdown_y.value)

# Define a handler for when the 'Generate Scores' button is clicked
def handle_click(sender,vs): 
    vs.chart_dropdown_x.value =  ' '
    vs.chart_dropdown_y.value =  ' '
    factor_score = get_data(dropdown_universe.value,dropdown_model.value,params)
    vs.populate_default_chart(factor_score)
    vs.data_grid.close()
    factor_score_for_grid = factor_score.reset_index()
    factor_score_for_grid.columns = [x.replace('.','_') for x in list(factor_score_for_grid.columns.values)]
    vs.data_grid = DataGrid(data=factor_score_for_grid.round(2))
    vs.data_grid.layout = Layout(width = '700px', height = '200px', margin = '25px 0px 0px 50px')
    display(vs.data_grid)
    


#2.3 Controls
# Define and display the input widgets
dropdown_universe = Dropdown(options=univ_list,description='Analysis Universe',style={'description_width':'initial'},value=univ_list[1])
dropdown_model = Dropdown(options=model_list,description='Factor Model',value=model_list[0])
button_update = Button(description="Generate Scores", button_style='success')
interface = VBox([HBox([dropdown_universe,dropdown_model, button_update])]) 
display(interface)

# Initialize visualization class and populate the chart
vs =  FactorVisualization()
factor_score = get_data(dropdown_universe.value, dropdown_model.value, params)
vs.populate_default_chart(factor_score)
vs.data_grid.close()

# Set up and populate the datagrid layout
factor_score_for_grid = factor_score.reset_index()
factor_score_for_grid.columns = [x.replace('.','_') for x in list(factor_score_for_grid.columns.values)]
vs.data_grid = DataGrid(data=factor_score_for_grid.round(2))
vs.data_grid.layout = Layout(width = '705px', height = '200px', margin = '25px 0px 0px 50px')
display(vs.data_grid)

button_update.on_click(partial(handle_click,vs=vs))
    
