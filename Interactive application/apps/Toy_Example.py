import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64
import pandas as pd
import pitch_plotly as pitch
import numpy as np
import ds4d as machine
from app import app
from sklearn.linear_model import LogisticRegression

path = 'C:\\Users\\iq10189\\Desktop\\University_of_Edinburgh\\Data Science for Design\\FIFA\\DS4D\\data\\dataset.csv'
original_data = pd.read_csv(path, sep=';' , decimal=',')
teams = original_data.sort_values('team')['team'].unique()
######Fitting Classification algorithm
y = original_data.loc[:,'cluster']  
x = original_data.loc[:,'C1':'Y11']
split  = np.rint(0.8*x.shape[0])
X_clean_train = x[:int(split)].values
X_clean_val = x[int(split):].values
y_train = y[:int(split)]
y_val = y[int(split):]
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(X_clean_train, y_train)
#####
demo_dict={}
old_form={}
ML=[]
for i in range(0,11):
	ML.append([])
	
layout = html.Div([
	html.Div([
		html.Div([
			html.Div([
				html.Label("Choose your Team"),
				dcc.Dropdown(
					id='Team_for_Formation',
					options=[{'label':i,'value':i} for i in teams],
					value = 'Spain')
				],
				style={'width': '32%', 'display': 'inline-block'}),
			html.Div([
				html.Label("Pick a Cluster"),
				dcc.Dropdown(id="Cluster_for_Formation",
				value=1)
				],
			style={'width': '32%', 'display': 'inline-block'}),
			html.Div([
				html.Label("Pick a Game"),
				dcc.Dropdown(id="Game_for_Formation",
				value=588)
				],
			style={'width': '32%', 'display': 'inline-block'}),
			]),
		html.Div([
			dcc.Graph(id='Football_Pitch_Mul',config={'displayModeBar': False})],
		style={'width': '48%','display': 'inline-block'}),	
	html.Div([	
		html.Label("Select a Player"),
		dcc.Dropdown(
			id = 'Player',
			options =[{'label':"Player %s"%i, 'value':i} for i in range(1,12)],
			value=1),
		html.Label("Modify X Position"),
		dcc.Slider(
			id='X_slider',
			min=0,
			max=100,
			step=0.1),
		html.Label("Modify Y position"),
		dcc.Slider(
			id='Y_slider',
			min=0,
			max=100,
			#marks={i*10:str(i*10) for i in range(1,11)},
			step=0.1),
		html.Label("Modify Betweenness"),
		dcc.Slider(
			id='Bet_slider',
			min=0,
			max=1,
			#marks={i/10:str(i/10) for i in range(1,11)},
			step=0.001),
		html.Label("Modify Closeness"),
		dcc.Slider(
			id='Clo_slider',
			min=0,
			max=10,
			#marks={i:str(i) for i in range(1,11)},
			step=0.01),
			html.Button(id ='submit',n_clicks=0, children="Submit Player")],
		style={'width': '50%','display': 'inline-block'}),
	]),
	html.Div([
		html.Div([
			dcc.Graph(id="Football_Pitch"),
			html.Button(id="submit_team",n_clicks=0, children="Submit New Formation")],
		style={'width': '50%','display': 'inline-block'}),
		html.Div(id='print',
		style={'width': '50%','display': 'inline-block'}),
	])
	
])

#Dropdowns
@app.callback(
	dash.dependencies.Output('Cluster_for_Formation','options'),
	[dash.dependencies.Input('Team_for_Formation', 'value')])
def set_cluster_options(selected_team):
	avail_clus=original_data.loc[original_data['team']==selected_team]['cluster'].unique()
	return [{'label': i, 'value': i} for i in avail_clus]
@app.callback(
	dash.dependencies.Output('Game_for_Formation','options'),
	[dash.dependencies.Input('Team_for_Formation', 'value'),
	dash.dependencies.Input('Cluster_for_Formation', 'value')])
def set_game_options(selected_team,selected_cluster):
	avail_games=original_data.loc[(original_data['team']==selected_team) &(original_data['cluster']==selected_cluster)]
	return [{'label': i+1, 'value': j} for i,j in enumerate(avail_games.index)]
	
#Figure 2
@app.callback(
	dash.dependencies.Output('Football_Pitch_Mul', 'figure'),
	[dash.dependencies.Input('Game_for_Formation', 'value')])
def update_graph_Field(game):
	global demo_dict,ML
	demo_dict={}
	title = 'Initial Formation'
	plotter = pitch.Plotter(title)
	demo_arr=[]
	temp_frame = original_data.iloc[game]
	for i in range(1,12):
		player=[temp_frame['X%s' %i],temp_frame['Y%s' %i],\
		'Player %s' %i,15]
		ML[i-1]=[temp_frame['C%s' %i],temp_frame['B%s' %i],temp_frame['X%s' %i],temp_frame['Y%s' %i]]
		demo_arr.append(player)
	plotter.add_events(demo_arr)
	data, layout = plotter.plot()
	return {'data': data, 'layout': layout}	

###X function
@app.callback(
	dash.dependencies.Output('X_slider','value'),
	[dash.dependencies.Input('Player', 'value'),
	dash.dependencies.Input('Game_for_Formation', 'value')])
def set_X_initial(player,game):
	temp_frame = original_data.iloc[game]
	mean = temp_frame['X%s'%player]
	return mean

@app.callback(
	dash.dependencies.Output('X_slider','min'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	min=original_data['X%s'%player].min()
	return min
	
@app.callback(
	dash.dependencies.Output('X_slider','max'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	max=original_data['X%s'%player].max()
	return max
	
###Y functions
@app.callback(
	dash.dependencies.Output('Y_slider','value'),
	[dash.dependencies.Input('Player', 'value'),
	dash.dependencies.Input('Game_for_Formation', 'value')])
def set_clusterA_options(player,game):
	temp_frame=original_data.iloc[game]
	mean = temp_frame['Y%s'%player]
	return mean

@app.callback(
	dash.dependencies.Output('Y_slider','min'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	min=original_data['Y%s'%player].min()
	return min
	
@app.callback(
	dash.dependencies.Output('Y_slider','max'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	max=original_data['Y%s'%player].max()
	return max
###Between
@app.callback(
	dash.dependencies.Output('Bet_slider','value'),
	[dash.dependencies.Input('Player', 'value'),
	dash.dependencies.Input('Game_for_Formation', 'value')])
def set_clusterA_options(player,game):
	temp_frame = original_data.iloc[game]
	mean = temp_frame['B%s'%player]
	return mean

@app.callback(
	dash.dependencies.Output('Bet_slider','min'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	min=original_data['B%s'%player].min()
	return min
	
@app.callback(
	dash.dependencies.Output('Bet_slider','max'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	max=original_data['B%s'%player].max()
	return max

###Close	
@app.callback(
	dash.dependencies.Output('Clo_slider','value'),
	[dash.dependencies.Input('Player', 'value'),
	dash.dependencies.Input('Game_for_Formation', 'value')])
def set_clusterA_options(player,game):
	temp_frame = original_data.iloc[game]
	mean = temp_frame['C%s'%player]
	return mean

@app.callback(
	dash.dependencies.Output('Clo_slider','min'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	min=original_data['C%s'%player].min()
	return min
	
@app.callback(
	dash.dependencies.Output('Clo_slider','max'),
	[dash.dependencies.Input('Player', 'value')])
def set_clusterA_options(player):
	max=original_data['C%s'%player].max()
	return max
	
	
@app.callback(
	dash.dependencies.Output('Football_Pitch', 'figure'),
	[dash.dependencies.Input('submit', 'n_clicks')],
	[dash.dependencies.State('Game_for_Formation', 'value'),
	dash.dependencies.State('Player', 'value'),
	dash.dependencies.State('X_slider', 'value'),
	dash.dependencies.State('Y_slider', 'value'),
	dash.dependencies.State('Clo_slider', 'value'),
	dash.dependencies.State('Bet_slider', 'value')])
def update_graph_Field(click,game,player1,X,Y,C,B):
	title = 'New Formation'
	global ML
	plotter = pitch.Plotter(title)
	temp_frame = original_data.iloc[game]
	for i in range(1,12):
		player=[temp_frame['X%s' %i],temp_frame['Y%s' %i],\
		'Player %s' %i,15]
		ML[i-1]=[temp_frame['C%s' %i],temp_frame['B%s' %i],temp_frame['X%s' %i],temp_frame['Y%s' %i]]
		old_form[i]=player
	if click==0:
		plotter.add_events_dict(old_form,u'Black')
		data, layout = plotter.plot()
		return {'data': data, 'layout': layout}

	if click>0:
		name='Player %s' %player1
		player = [X,Y,name,15]
		ML[player1-1] = [C,B,X,Y]
		demo_dict[player1]=player
		[old_form.pop(key) for key in list(demo_dict.keys())] 
		plotter.add_events_dict(demo_dict,u'Red')
	plotter.add_events_dict(old_form,u'Black')
	data, layout = plotter.plot()
	return {'data': data, 'layout': layout}

@app.callback(
	dash.dependencies.Output('print', 'children'),
	[dash.dependencies.Input("submit_team", 'n_clicks')])
def update_output(clicks):
	if any(len(elem) is 0 for elem in ML) & clicks>0:
		return 'Please submit 11 players first'
	Close, Between, X, Y = zip(*ML)
	Close=np.asarray(Close)
	Between=np.asarray(Between)
	X=np.asarray(X)
	Y=np.asarray(Y)
	data = np.concatenate((Close,Between,X,Y),axis=None).T
	a=logreg.predict([data])[0]
	return str(a)	

