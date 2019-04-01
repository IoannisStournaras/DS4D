import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64

from app import app
path_img = 'C:\\Users\\iq10189\\Desktop\\University_of_Edinburgh\\Data Science for Design\\FIFA\\DS4D\\Interactive application\\fifa1.JPG'
with open(path_img, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
encoded_image = "data:image/png;base64," + encoded_string

layout = html.Div([
    html.H2(
		children='Welcome to FIFA Presentation',
		style={
			'textAlign':'center',
			'color':'#111111'
		}
	),
	html.Div([
		dcc.Link(html.Button('Go to App 1'), href='/app1')],
		style={'width': '15.5%', 'display': 'inline-block'}),
	html.Div([
		dcc.Link(html.Button('Go to Team Statistics'), href='/app2')],
		style={'width': '25%', 'display': 'inline-block'}),
	html.Div([
		dcc.Link(html.Button('Go to App2'), href='/app2')],
		style={'width': '20%', 'display': 'inline-block'}),
	html.Div([
		dcc.Link(html.Button('Average Statistics'), href='/app3')],
		style={'width': '20%', 'display': 'inline-block'}),
	html.Img(src=encoded_image, 
		style={
			'width':"80%",
			'height':"70%"})
])