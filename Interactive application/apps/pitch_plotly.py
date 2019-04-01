import plotly as py
from plotly.graph_objs import *

class Plotter:
    def add_events(self, arr):
        xvals, yvals, names, size = zip(*arr)

        trace = Scatter(
            x=xvals,
            y=yvals,
			showlegend=False,
            text=names,
			hoverinfo = 'text',
            mode='markers',
            marker=Marker(
                color=u"Black",
                size=size,
                line=Line(width=2, color='white')
            )
        )

        self.traces.append(trace)

    def add_events_dict(self, mydict):
        arr=[]
        for key in mydict:
            arr.append(mydict[key])
        xvals, yvals, names, size = zip(*arr)

        trace = Scatter(
            x=xvals,
            y=yvals,
			showlegend=False,
            text=names,
			hoverinfo = 'text',
            mode='markers',
            marker=Marker(
                color=u"Black",
                size=size,
                line=Line(width=2, color='white')
            )
        )

        self.traces.append(trace)	
    def add_contours(self, X, Y):

        trace_1 = Histogram2dContour(
            x=X,
            y=Y,
			ncontours=3,
			showscale=False,
			opacity=1,
			colorscale="Greys",
			reversescale=True,
			hoverinfo = 'none',
			contours = {
				'showlines':True,
				#'start':1,
				#'end':10,
				'coloring':'lines'
        }
        )

        self.traces.append(trace_1)
		
    def __init__(self, plot_title):
        self.traces = []

        trace1 = Scatter(
            showlegend=False,
            x=[50, 50],
            y=[100, 0],
            mode='lines',
            line=Line(width=2, color='white')
        )
        self.traces.append(trace1)
        trace2 = Scatter(
            showlegend=False,
            x=[0, 16, 16, 0],
            y=[80, 80, 20, 20],
            mode='lines',
            line=Line(width=2, color='white'),

        )
        self.traces.append(trace2)

        trace3 = Scatter(
            showlegend=False,
            x=[100, 84, 84, 100],
            y=[80, 80, 20, 20],
            mode='lines',
            line=Line(width=2, color='white')
        )
        self.traces.append(trace3)

        self.layout = Layout(
            title=plot_title,
            hovermode='closest',
            autosize=True,
            width=600,
            height=350,
			#margin=dict(l=50,r=50,t=50,b=0),
            plot_bgcolor='rgba(50, 200, 96, 1)',
            xaxis=XAxis(
                range=[0, 100],
                showgrid=False,
                showticklabels=False
            ),
            yaxis=YAxis(
                range=[0, 100],
                showgrid=False,
                showticklabels=False
            ),
            annotations=Annotations([
                Annotation(
                    x=0,
                    y=0,
                    xref='x',
                    yref='y',
                    xanchor='left',
                    yanchor='top',
                    showarrow=False
                )
            ])
)
        
    def plot(self):
        return self.traces, self.layout
