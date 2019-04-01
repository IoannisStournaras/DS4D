import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

path = '~/Desktop//DS4D//dataset.csv'

original_data = pd.read_csv(path, sep=';' , decimal=',')

teamData = original_data.set_index('team', inplace=False)
cteams = teamData.groupby('team').mean()
mydata = cteams.drop(columns = 'cluster')
#mydata = original_data.groupby(['team','cluster']).mean()
clust = teamData.groupby('cluster').mean()
teams = original_data.sort_values('team')['team'].unique()
#mydata = original_data.groupby(['team','cluster']).mean()
position = np.arange(1,12)
choices = ['X-axes Comparison','Y-axes Comparison','Betweenness','Closeness']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.H1(
		children="Compare same players in different clusters",
		style={
			'textAlign':'center',
			'color':'#111111'
		}
	),

	html.Div([
		html.Div([
			html.Label("Pick 1st player number"),
			dcc.Dropdown(
				id='Number1',
				options=[{'label':i,'value':i} for i in position],
				value = 6)
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("Pick 2nd player number"),
			dcc.Dropdown(
				id='Number2',
				options=[{'label':i,'value':i} for i in position],
				value = 2)
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("Select statistical category"),
			dcc.Dropdown(
				id="Choices",
				options=[{'label':i,'value':i} for i in choices],
				value='Closeness')
			],
		style={'width': '48%', 'display': 'inline-block'}),
		]),
	dcc.Graph(id='Stats', config={'displayModeBar': False})
])

@app.callback(
	dash.dependencies.Output('Stats', 'figure'),
	[dash.dependencies.Input('Number1', 'value'),
	 dash.dependencies.Input('Number2', 'value'),
     	 dash.dependencies.Input('Choices', 'value')])
	 #dash.dependencies.Input('ClusterA', 'value'),
	 #dash.dependencies.Input('ClusterB', 'value')])
def update_graph_Close(N1,N2,C):
	data = [
		go.Bar(
			x=np.arange(1,7),
			y=clust[C[0]+str(N1)],
			name=C+' '+str(N1)),
		go.Bar(
			x=np.arange(1,7),
			y=clust[C[0]+str(N2)],
			name=C+' '+str(N2))
	]
	layout = go.Layout(
	#title = 'Statistics'
		barmode='group'
		)	
	return {'data': data, 'layout': layout}
	#return {'data': data}

if __name__ == '__main__':
    app.run_server(debug=True)

