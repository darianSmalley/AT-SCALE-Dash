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
                            'X-Axis',
                            dcc.Dropdown(id='xaxis_column_name', value='Program Time (s)'),
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
                            'Y-Axis',
                            dcc.Dropdown(id='yaxis_column_name', value='SLED (J/mm^2)'),
                            dcc.RadioItems(
                                ['Linear', 'Log'],
                                'Linear',
                                id='crossfilter-yaxis-type',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px', 'marginRight': '5px'}
                            )
                        ],
                        align="end"
                    ),
                ]),
                dcc.Loading(
                    dcc.Graph(id='graph-content', style={'display': 'none'}), type='graph'
                )
            ]
        )
    ],
    class_name="shadow-sm p-3 mb-5 bg-white rounded"
)

@callback(
    Output('graph-content', 'figure'),
    Output('graph-content', 'style'),
    Input('store', 'data'),
    Input('xaxis_column_name', 'value'),
    Input('yaxis_column_name', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input({'type': 'property_range_slider', 'index': ALL}, 'value'),
    State({'type': 'property_range_slider', 'index': ALL}, 'id'),
)
def update_graph(data, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, slider_values, slider_ids):
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
    )

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig, {}