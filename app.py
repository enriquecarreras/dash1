import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc



data = pd.read_csv('data/dashapp.csv')

all_options = {}
for t in ['Observed','OLS','FB']:
    data = data[data['Kind']==t]
    all_options[t] = data.columns.tolist()

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# Define the app
app.layout = html.Div(children=[
                        html.Div(className='row',  # Define the row element
                                children=[
                                    html.Div(className='four columns div-user-controls',   # Define the left element
                                    children = [
											    html.H2('Dashboard - Macroeconomic data'),

											    html.Div(
											    	[
											    	html.Div(className='div-for-dropdown',
											    		children=[html.P("Kind"),
									                	dcc.Dropdown(
													        id='Kind', clearable=True,
													        value= 'Observed', options= [
													            {'label': c, 'value': c}
													            for c in ['Observed','OLS','FB']]),

									                	html.H2(),
											            
											            html.P("Variable"),
									                dcc.Dropdown(
													        id='variable', clearable=False,
													        value= data.columns.tolist()[0], options= [
													            {'label': c, 'value': c}
													            for c in data.columns.tolist()]),
									                
									                ])])
											]),
                                    html.Div(className='eight columns div-for-charts bg-grey',   # Define the right element
                                    children = [
                                    html.Div([
                                                                                                            dcc.Graph(id='graph')]),
                                    style={'backgroundColor': '#31302F'})],
                                    )  
                                    ])
                                ])
# Define callback to update graph
@app.callback(
	Output('variable','options'),
	Input('tiempo','Number'))

def set_variable_options(Kind):
    return [{'label': i, 'value': i} for i in all_options[Kind]]

@app.callback(
    Output('variable', 'Number'),
    Input('variable', 'options'))

def set_variable_value(available_options):
    return available_options[0]['Number']

@app.callback(
    Output('graph', 'figure'),
    [Input("Kind", "Number"),
    Input("variable", "Number")]
)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
