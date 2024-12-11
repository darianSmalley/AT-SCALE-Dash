from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from .util import apply_filter
from .data_store import local_data

XY_scatter = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("2D Scatter Plot", className="card-title"),
                dbc.Row([
                    dbc.Col(
                        [
                            html.H6('X-Axis', className="card-subtitle"),
                            dcc.Dropdown(id='xaxis_column_name', value='Melt Pool Temperature (C)'),
                            dcc.RadioItems(
                                ['Linear', 'Log'],
                                'Linear',
                                id='crossfilter-xaxis-type',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px', 'marginRight': '5px'}
                            )
                        ],
                        align="end"
                    ),
                    dbc.Col(
                        [
                            html.H6("Y-Axis", className="card-subtitle"),
                            dcc.Dropdown(id='yaxis_column_name', value='Melt Pool Size (mm)'),
                            dcc.RadioItems(
                                ['Linear', 'Log'],
                                'Linear',
                                id='crossfilter-yaxis-type',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px', 'marginRight': '5px'}
                            )
                        ],
                        align="end"
                    ),
                    dbc.Col(
                        [
                            html.H6("Marker Color", className="card-subtitle"),
                            dcc.Dropdown(id='2Dscatter_color_name', value='Laser Power On Time (s)'),
                        ]
                    )
                ]),
                dcc.Loading(
                    dcc.Graph(id='graph-content', style={'display': 'none'}), type='graph'
                )
            ]
        )
    ],
    class_name="shadow-sm p-3 mb-5 bg-white rounded animate__animated animate__fadeInUp animate__slow"
)

@callback(
    Output('graph-content', 'figure'),
    Output('graph-content', 'style'),
    Input('store', 'data'),
    Input('xaxis_column_name', 'value'),
    Input('yaxis_column_name', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('2Dscatter_color_name', 'value'),
    Input({'type': 'property_range_slider', 'index': ALL}, 'value'),
    State({'type': 'property_range_slider', 'index': ALL}, 'id'),
)
def update_graph(data, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, scatter_color_name, slider_values, slider_ids):
    if data is None:
        return no_update
    
    if data['uploaded_data']:
        dff = pd.DataFrame(data['df'])
    else:
        dff = local_data.df.copy()

    dff = apply_filter(dff, slider_values, slider_ids)

    fig = px.scatter(dff,
        x=xaxis_column_name,
        y=yaxis_column_name,
        color=scatter_color_name
    )

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(
        coloraxis_colorbar_title_side="right",
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        hovermode='closest')

    return fig, {}