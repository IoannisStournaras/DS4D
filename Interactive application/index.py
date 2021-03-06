import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import Formation_Player_Compasison, Team_Statistics,main_page,errorbars,Toy_Example


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/formation':
         return Formation_Player_Compasison.layout
    elif pathname == '/statistics/clusters':
         return Team_Statistics.layout
    elif pathname == '/statistics':
         return errorbars.layout
    elif pathname == '/index':
        return main_page.layout
    elif pathname == '/example':
        return Toy_Example.layout
    else: 
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)