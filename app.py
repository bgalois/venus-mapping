import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Venus Surface Mapping"),
    dcc.Textarea(
        id='grid-input',
        value='2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2\n2,2,2,2,2,2,2,2',
        style={'width': '100%', 'height': '150px'}
    ),
    html.Button('Generate Chart', id='submit-button', n_clicks=0),
    dcc.Graph(id='surface-plot')
])

@app.callback(
    Output('surface-plot', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('grid-input', 'value')
)
def update_graph(n_clicks, input_text):
    try:
        # Parse and flip rows so row 1 is at the front
        data = [list(map(int, row.split(','))) for row in input_text.strip().split('\n')]
        z = np.array(data[::-1])  # Flip rows so row 1 is at the front
        z_norm = (z - 1) / 2

        colorscale = [
            [0.0, 'red'], [0.33, 'red'],
            [0.34, 'green'], [0.66, 'green'],
            [0.67, 'purple'], [1.0, 'purple']
        ]

        fig = go.Figure(data=[go.Surface(
            z=z,
            surfacecolor=z_norm,
            colorscale=colorscale,
            cmin=0,
            cmax=1,
            showscale=False
        )])

        fig.update_layout(
            scene=dict(
                xaxis_title='Column',
                yaxis_title='Row',
                zaxis_title='Value',
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(8)),
                    ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                ),
                yaxis=dict(
                    tickmode='array',
                    tickvals=list(range(8)),
                    ticktext=['8', '7', '6', '5', '4', '3', '2', '1']  # Reversed so front is row 1
                ),
                zaxis=dict(
                    range=[0, 3.9],
                    tickmode='array',
                    tickvals=[1, 2, 3],
                    ticktext=['1', '2', '3']
                )
            ),
            height=600,   # Taller window (most important for bottom clipping)
            margin=dict(l=0, r=0, b=0, t=10)
        )

        return fig
    except Exception as e:
        print("Error:", e)
        return go.Figure()

if __name__ == '__main__':

    app.run(debug=True)


