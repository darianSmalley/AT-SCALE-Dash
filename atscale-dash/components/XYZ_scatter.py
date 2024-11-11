from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from .util import apply_filter
from .data_store import local_data

XYZ_scatter = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("XYZ Scatter Plot", className="card-title"),
                html.H6("Marker Color", className="card-subtitle"),
                dcc.Dropdown(id='scatter_color_name', value='Program Time (s)', style={'width':'22rem'}),
                dcc.Loading([
                    dcc.Graph(id='3d-scatter', style={'display': 'none'})
                ], type='graph'),
            ]
        ),
    ],
    class_name="shadow-sm p-3 mb-5 bg-white rounded"
)

@callback(
    Output('3d-scatter', 'figure'),
    Output('3d-scatter', 'style'),
    Input('store', 'data'),
    Input('scatter_color_name', 'value'),
    Input({'type': 'property_range_slider', 'index': ALL}, 'value'),
    State({'type': 'property_range_slider', 'index': ALL}, 'id'),
)
def update_scatter3d(data, scatter_color_name, slider_values, slider_ids,):
    if data is None:
        return no_update
    
    if data['uploaded_data']:
        dff = pd.DataFrame(data['df'])
    else:
        dff = local_data.df.copy()

    dff = apply_filter(dff, slider_values, slider_ids)

    fig = px.scatter_3d(dff, 
                        x="X Position (mm)", 
                        y="Y Position (mm)", 
                        z='Z Position (mm)', 
                        color=scatter_color_name,
                        )
    
    fig.update_traces(marker=dict(size=2))
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, height=500, hovermode='closest')

    return fig, {}