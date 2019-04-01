#No comments yet
#Still work to be done
#Just a first attempt
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from app import app
path = 'C:\\Users\\iq10189\\Desktop\\University_of_Edinburgh\\Data Science for Design\\FIFA\\DS4D\\data\\dataset.csv'

original_data = pd.read_csv(path, sep=';' , decimal=',')
teams = original_data.sort_values('team')['team'].unique()
mydata = original_data.groupby(['team','cluster']).mean()

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


layout = html.Div([
	html.H1(
		children="Compare Team Statistics",
		style={
			'textAlign':'center',
			'color':'#111111'
		}
	),
	
	html.Div([
		html.Div([
			html.Label("Pick First Team"),
			dcc.Dropdown(
				id='TeamA',
				options=[{'label':i,'value':i} for i in teams],
				value = 'Spain')
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("Available Clusters"),
			dcc.Dropdown(id="ClusterA",
			value=1)
			],
		style={'width': '48%', 'display': 'inline-block'}),
		]),
		
	html.Div([
		html.Div([
			html.Label("Pick Second Team"),	
			dcc.Dropdown(
			id='TeamB',
			options=[{'label': i, 'value': i} for i in teams],
			value='Belgium')
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("Available Clusters"),
			dcc.Dropdown(id="ClusterB",
			value=1)
			],
		style={'width': '48%', 'display': 'inline-block'}),
		]),
	dcc.Graph(id='Closeness', config={'displayModeBar': False}),
	dcc.Graph(id='Betweenness', config={'displayModeBar': False})
])

@app.callback(
	dash.dependencies.Output('ClusterA','options'),
	[dash.dependencies.Input('TeamA', 'value')])
def set_clusterA_options(selected_team):
	avail_clus=mydata.loc[selected_team].index
	return [{'label': i, 'value': i} for i in avail_clus]
	
@app.callback(
	dash.dependencies.Output('ClusterB','options'),
	[dash.dependencies.Input('TeamB', 'value')])
def set_clusterB_options(selected_team):
	avail_clus=mydata.loc[selected_team].index
	return [{'label': i, 'value': i} for i in avail_clus]

@app.callback(
	dash.dependencies.Output('Closeness', 'figure'),
	[dash.dependencies.Input('TeamA', 'value'),
     dash.dependencies.Input('TeamB', 'value'),
	 dash.dependencies.Input('ClusterA', 'value'),
	 dash.dependencies.Input('ClusterB', 'value')])
def update_graph_Close(A,B,C1,C2):
	data = [
		go.Bar(
			x=mydata.columns[0:11],
			y=mydata.loc[A,C1]["C1":"C11"],
			name=A),
		
        go.Bar(
			x=mydata.columns[0:11],
			y=mydata.loc[B,C2]["C1":"C11"],
			name=B
		)
	]
	layout = go.Layout(
	title = 'Closeness',
		barmode='group'
		)	
	return {'data': data, 'layout': layout}

@app.callback(
	dash.dependencies.Output('Betweenness', 'figure'),
	[dash.dependencies.Input('TeamA', 'value'),
     dash.dependencies.Input('TeamB', 'value'),
	 dash.dependencies.Input('ClusterA', 'value'),
	 dash.dependencies.Input('ClusterB', 'value')])
def update_graph_Between(A,B,C1,C2):
	data = [
		go.Bar(
			x=mydata.columns[11:22],
			y=mydata.loc[A,C1]["B1":"B11"],
			name=A),
		
        go.Bar(
			x=mydata.columns[11:22],
			y=mydata.loc[B,C2]["B1":"B11"],
			name=B
		)
	]
	layout = go.Layout(
		title = 'Betweenness',
		barmode='group'
		)	
	return {'data': data, 'layout': layout}
	

#if __name__ == '__main__':
#	app.run_server(debug=True)