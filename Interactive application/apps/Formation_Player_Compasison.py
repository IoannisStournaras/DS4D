import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64
import pandas as pd
import pitch_plotly as pitch

from app import app

path = 'C:\\Users\\iq10189\\Desktop\\University_of_Edinburgh\\Data Science for Design\\FIFA\\DS4D\\data\\dataset.csv'
original_data = pd.read_csv(path, sep=';' , decimal=',')
teams = original_data.sort_values('team')['team'].unique()
mydata = original_data.groupby(['team','cluster']).mean()
clusterized = original_data.groupby(['cluster']).mean()

layout = html.Div([
	html.H3(
		children="Formation and Player Comparison",
		style={
			'textAlign':'center',
			'color':'#111111'
		}
	),
	html.Div([
		html.Div([	
			dcc.Link(html.Button('Go to Main Page'), href='/index')],
			style={'width': '100%', 'textAlign':'center','display': 'inline-block'}),			
	]),
	html.Div([
		html.Div([
			html.Label("Pick First Team"),
			dcc.Dropdown(
				id='Team_1',
				options=[{'label':i,'value':i} for i in teams],
				value = 'Spain')
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("First Team Available Clusters "),
			dcc.Dropdown(id="Cluster_1",
			value=5)
			],
		style={'width': '48%', 'display': 'inline-block'}),
		]),
	html.Div([
		html.Div([
			html.Label("Pick Second Team"),
			dcc.Dropdown(
				id='Team_2',
				options=[{'label':i,'value':i} for i in teams],
				value = 'Belgium')
			],
			style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.Label("Second Team Available Clusters"),
			dcc.Dropdown(id="Cluster_2",
			value=2)
			],
		style={'width': '48%', 'display': 'inline-block'}),
		]),
	html.Div([
		html.Div([
			dcc.Graph(id='Football Pitch',config={'displayModeBar': False})],
		style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			dcc.Graph(id='Football Pitch2',config={'displayModeBar': False})],
		style={'width': '48%', 'display': 'inline-block'}),
	]),	
	
	html.Div([	
		html.Div([
			dcc.Graph(id='Radar2',config={'displayModeBar': False})],
			style={'width': '33%', "text-align":'center','display': 'inline-block'}),
		html.Div([
			dcc.Graph(id='Radar3',config={'displayModeBar': False})],
			style={'width': '33%', "text-align":'center','display': 'inline-block'}),
		html.Div([
			dcc.Graph(id='Radar1',config={'displayModeBar': False})],
			style={'width': '33%', "text-align":'center','display': 'inline-block'}),		
	])		
])

@app.callback(
	dash.dependencies.Output('Cluster_1','options'),
	[dash.dependencies.Input('Team_1', 'value')])
def set_clusterA_options(selected_team):
	avail_clus=mydata.loc[selected_team].index
	return [{'label': i, 'value': i} for i in avail_clus]
	
@app.callback(
	dash.dependencies.Output('Cluster_2','options'),
	[dash.dependencies.Input('Team_2', 'value')])
def set_clusterB_options(selected_team):
	avail_clus=mydata.loc[selected_team].index
	return [{'label': i, 'value': i} for i in avail_clus]
	
@app.callback(
	dash.dependencies.Output('Football Pitch', 'figure'),
	[dash.dependencies.Input('Team_1', 'value'),
	dash.dependencies.Input('Cluster_1', 'value')])
def update_graph_Field(team,cluster):
	title = '%s Formation'%team
	plotter = pitch.Plotter(title)
	demo_arr=[]
	temp_frame = mydata.loc[team,cluster]
	for i in range(1,12):
		player=[temp_frame['X%s' %i],temp_frame['Y%s' %i],\
		'Player %s' %i,15]
		demo_arr.append(player)
	plotter.add_events(demo_arr)
	data, layout = plotter.plot()
	return {'data': data, 'layout': layout}

@app.callback(
dash.dependencies.Output('Radar1', 'figure'),
	[dash.dependencies.Input('Football Pitch', 'hoverData'),
	dash.dependencies.Input('Football Pitch2', 'hoverData'),
	dash.dependencies.Input('Team_1', 'value'),
	dash.dependencies.Input('Cluster_1', 'value'),
	dash.dependencies.Input('Team_2', 'value'),
	dash.dependencies.Input('Cluster_2', 'value')])
def update_graph_Radar(hoverData1,hoverData2,team1,cluster1,team2,cluster2):
	keimeno = hoverData1['points'][0]['text']
	n1 = keimeno.split(" ")[1]
	keimeno = hoverData2['points'][0]['text']
	n2 = keimeno.split(" ")[1]
	temp_frame = mydata.loc[team1,cluster1]
	C, B, X, Y = "C"+n1, "B"+n1, "X"+n1, "Y"+n1
	C_,B_, X_, Y_ = temp_frame[[C,B,X,Y]]
	temp_frame = mydata.loc[team2,cluster2]
	C, B, X, Y = "C"+n2, "B"+n2, "X"+n2, "Y"+n2
	C, B, X, Y = temp_frame[[C,B,X,Y]]
	data =[
		go.Scatterpolar(
			r = [C*10, X, B*100+5, Y],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Team A Player Performance'
		),
		go.Scatterpolar(
			r = [C_*10, X_, B_*100+5, Y_],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Team B Player Performance'
		)
	]
	layout = go.Layout(
		title="Comparing Player "+n1+ " to " +n2,
		polar = dict(
			radialaxis = dict(
		visible = True,
		range = [0, 100]
		)
	),
	showlegend = False
	)
	return {'data': data, 'layout': layout}
	
@app.callback(
dash.dependencies.Output('Radar2', 'figure'),
	[dash.dependencies.Input('Football Pitch', 'hoverData'),
	dash.dependencies.Input('Team_1', 'value'),
	dash.dependencies.Input('Cluster_1', 'value')])
def update_graph_Radar2(hoverData1,team1,cluster1):
	keimeno = hoverData1['points'][0]['text']
	n = keimeno.split(" ")[1]
	temp_frame = mydata.loc[team1,cluster1]
	C, B, X, Y = "C"+n, "B"+n, "X"+n, "Y"+n
	C_,B_, X_, Y_ = temp_frame[[C,B,X,Y]]
	C, B, X, Y=clusterized.loc[cluster1][[C,B,X,Y]]
	data =[
		go.Scatterpolar(
			r = [C*10, X, B*100+5, Y],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Mean performance'
		),
		go.Scatterpolar(
			r = [C_*10, X_, B_*100+5, Y_],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Player Performance',
		)
	]
	layout = go.Layout(
		title="Comparing "+team1+" Player" +n+ " to average performance of cluster "+ str(cluster1),
		polar = dict(
		radialaxis = dict(
		visible = True,
		range = [0, 100]
		)
	),
	showlegend = False
	)
	return {'data': data, 'layout': layout}
	
@app.callback(
dash.dependencies.Output('Radar3', 'figure'),
	[dash.dependencies.Input('Football Pitch2', 'hoverData'),
	dash.dependencies.Input('Team_2', 'value'),
	dash.dependencies.Input('Cluster_2', 'value')])
def update_graph_Radar2(hoverData2,team2,cluster2):
	keimeno = hoverData2['points'][0]['text']
	n = keimeno.split(" ")[1]
	temp_frame = mydata.loc[team2,cluster2]
	C, B, X, Y = "C"+n, "B"+n, "X"+n, "Y"+n
	C_,B_, X_, Y_ = temp_frame[[C,B,X,Y]]
	C, B, X, Y=clusterized.loc[cluster2][[C,B,X,Y]]
	data =[
		go.Scatterpolar(
			r = [C*10, X, B*100+5, Y],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Mean performance'
		),
		go.Scatterpolar(
			r = [C_*10, X_, B_*100+5, Y_],
			theta = ['Close','X', 'Between', 'Y'],
			fill = 'toself',
			name = 'Player Performance',
		)
	]
	layout = go.Layout(
		title="Comparing "+team2+ " Player" +n+ " to average performance of cluster "+ str(cluster2),
		polar = dict(
		radialaxis = dict(
		visible = True,
		range = [0, 100]
		)
	),
	showlegend = False
	)
	return {'data': data, 'layout': layout}
	
@app.callback(
	dash.dependencies.Output('Football Pitch2', 'figure'),
	[dash.dependencies.Input('Team_2', 'value'),
	dash.dependencies.Input('Cluster_2', 'value')])
def update_graph_Field(team,cluster):
	title = '%s Formation' %team
	plotter = pitch.Plotter(title)
	demo_arr=[]
	temp_frame = mydata.loc[team,cluster]
	for i in range(1,12):
		player=[temp_frame['X%s' %i],temp_frame['Y%s' %i],\
		'Player %s' %i,15]
		demo_arr.append(player)
	plotter.add_events(demo_arr)
	data, layout = plotter.plot()
	return {'data': data, 'layout': layout}

	