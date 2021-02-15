import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import statsmodels.api as sm



all_options = {}
for t in ['mensual','trimestral','anual']:
    data = pd.read_excel('data/sample_data.xlsx', sheet_name = t).T
    data.columns = data.loc['Indicador'].values
    data.drop('Indicador', inplace = True)
    #data = data.reset_index().rename(columns = {'index':'Date'})

    data.index = data.index.rename('Date')
    all_options[t] = data.columns.tolist()

data = pd.read_excel('data/sample_data.xlsx', sheet_name = 'mensual').T
data.columns = data.loc['Indicador'].values
data.drop('Indicador', inplace = True)
#data = data.reset_index().rename(columns = {'index':'Date'})

data.index = pd.to_datetime(data.index).rename('Fecha')
data = data.convert_dtypes()
# Initialise the app
app = dash.Dash(__name__)
server = app.server

# Define the app
app.layout = html.Div(children=[
                        html.Div(className='row',  # Define the row element
                                children=[
                                    html.Div(className='four columns div-user-controls',   # Define the left element
                                    children = [
											    html.H2('Dashboard - Bolivia'),
											    html.P('''Visualizamos los datos que me paso el banqui'''),
											    #html.P('''Bolivia (aimara: Wuliwya; guaraní: Mborívia; quechua: Buliwya), oficialmente Estado Plurinacional de Bolivia,12​13​ es un país soberano situado en la región centro-occidental de América del Sur, políticamente se constituye como un estado plurinacional, descentralizado con autonomías. Está organizado en nueve departamentos. Su capital constitucional es Sucre,14​ sede del órgano judicial; la ciudad de La Paz es la sede de los órganos ejecutivo, legislativo y electoral.'''),

											    html.Div(
											    	[
											    	html.Div(className='div-for-dropdown',
											    		children=[html.P("Rango temporal"),
									                	dcc.Dropdown(
													        id='tiempo', clearable=False,
													        value= 'mensual', options= [
													            {'label': c, 'value': c}
													            for c in ['mensual','trimestral','anual']]),

									                	html.H2(),
											            
											            html.P("Variable"),
									                dcc.Dropdown(
													        id='variable', clearable=False,
													        value= data.columns.tolist()[0], options= [
													            {'label': c, 'value': c}
													            for c in data.columns.tolist()]),
									                html.H2(),
									                html.H2(),
									                html.P('Seasonal decomposition'),
									                html.Div(
									                	[dcc.Checklist(
									                		id = 'radiotrend',
															options=[
															    {'label': 'Trend', 'value': 'trend'}
															    ],
															)]),
									                html.H2(),
									                html.H2(),
									                html.Div(
									                	[dcc.Checklist(
									                		id = 'searesid',
															options=[
															    {'label': 'Seasonal', 'value': 'seasonal'},
															    {'label': 'Residuals', 'value': 'resid'}
															    ], value = ['seasonal', 'resid']
															)])
									                ])])
											]),
                                    html.Div(className='eight columns div-for-charts bg-grey',   # Define the right element
                                    children = [
                                    html.Div([
                                                                                                            dcc.Graph(id='graph')]),
                                    html.Div([dcc.Graph(id='seasonal-resid-plot')],style={'backgroundColor': '#31302F'})],
                                    )  
                                    ])
                                ])
# Define callback to update graph
@app.callback(
	Output('variable','options'),
	Input('tiempo','value'))

def set_variable_options(tiempo):
    return [{'label': i, 'value': i} for i in all_options[tiempo]]

@app.callback(
    Output('variable', 'value'),
    Input('variable', 'options'))

def set_variable_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('graph', 'figure'),
    [Input("tiempo", "value"),
    Input("variable", "value"),
    Input("radiotrend", "value")]
)

def update_figure(tiempo, variable, radiotrend):
	data = pd.read_excel('data/sample_data.xlsx', sheet_name = tiempo).T
	data.columns = data.loc['Indicador'].values
	data.drop('Indicador', inplace = True)
	#data = data.reset_index().rename(columns = {'index':'Date'})
	data.index = pd.to_datetime(data.index).rename('Fecha')
	data = data.convert_dtypes()
	if radiotrend == ['trend']:

		decomposed = sm.tsa.seasonal_decompose(data[variable].astype('float32'))

		fig = go.Figure()

		fig.add_trace(go.Scatter(
		    x=data.index,
		    y=data[variable],
		    name= str(variable)
		))

		fig.add_trace(go.Scatter(
		    x= data.index,
		    y=decomposed.trend,
		    name="Trend"
		))

		fig.layout.template = 'plotly_dark'

		return fig.update_layout(
			{'plot_bgcolor': 'rgba(0, 0, 0, 0)',
	        'paper_bgcolor': 'rgba(0, 0, 0, 0)', "height": 400, 'title':'Variable principal con tendencia'})
	else:
		return px.line(data, x= data.index, y=variable, render_mode="webgl", template='plotly_dark').update_layout(
			{'plot_bgcolor': 'rgba(0, 0, 0, 0)',
	        'paper_bgcolor': 'rgba(0, 0, 0, 0)', "height": 400, 'title':'Variable principal'})

@app.callback(
    Output('seasonal-resid-plot', 'figure'),
    [Input("tiempo", "value"),
    Input("variable", "value"),
    Input("searesid", "value")])

def update_figure2(tiempo, variable, searesid):
	data = pd.read_excel('data/sample_data.xlsx', sheet_name = tiempo).T
	data.columns = data.loc['Indicador'].values
	data.drop('Indicador', inplace = True)
	#data = data.reset_index().rename(columns = {'index':'Date'})
	data.index = pd.to_datetime(data.index).rename('Fecha')
	data = data.convert_dtypes()
	decomposed = sm.tsa.seasonal_decompose(data[variable].astype('float32'))

	fig = go.Figure()
	
	for col in searesid:
		if col == 'seasonal':
	    	
			fig.add_trace(go.Scatter(
		    x=data.index,
		    y=decomposed.seasonal,
		    name= 'Seasonal'))

		if col == 'resid':
	    	
			fig.add_trace(go.Scatter(
		    x=data.index,
		    y=decomposed.resid,
		    name= 'Residuals'))

		fig.layout.template = 'plotly_dark'
	
	return fig.update_layout(
		{'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)', "height": 250, 'title':'Componentes estacionales'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)