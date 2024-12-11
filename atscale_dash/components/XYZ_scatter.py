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
                dbc.Row([
                    dbc.Col(
                        [
                            html.H6("Marker Color", className="card-subtitle"),
                            dcc.Dropdown(id='scatter_color_name', value='Melt Pool Temperature (C)'),
                        ]
                    ),
                    dbc.Col( 
                        [
                            html.H6("Marker Size", className="card-subtitle"),
                            dcc.Dropdown(id='scatter_size_name', value='Melt Pool Size (mm)'),
                        ]
                    )
                ]),
                dcc.Loading([
                    dcc.Graph(id='3d-scatter', style={'display': 'none'})
                ], type='graph'),
            ]
        ),
    ],
    class_name="shadow-sm p-3 mb-5 bg-white rounded animate__animated animate__fadeInUp animate__slow"
)

@callback(
    Output('3d-scatter', 'figure'),
    Output('3d-scatter', 'style'),
    Input('store', 'data'),
    Input('scatter_color_name', 'value'),
    Input('scatter_size_name', 'value'),
    Input({'type': 'property_range_slider', 'index': ALL}, 'value'),
    State({'type': 'property_range_slider', 'index': ALL}, 'id'),
)
def update_scatter3d(data, marker_color, marker_size, slider_values, slider_ids,):
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
                        color=marker_color,
                        size=marker_size,
                        # size_max=12
                        )
    
    # fig.update_traces(marker=dict(size=2))
    fig.update_traces(
        marker_line_width=0
    )
    fig.update_layout(
        coloraxis_colorbar_title_side="right",
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        height=500, 
        hovermode='closest')

    return fig, {}