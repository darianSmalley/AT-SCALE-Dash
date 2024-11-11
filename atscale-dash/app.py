
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
import dash_bootstrap_components as dbc

from components import header, data_buttons, tutorial, XYZ_scatter, XY_scatter, file_info

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        header,
        html.Hr(),
        data_buttons,
        tutorial,
        file_info,
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(XYZ_scatter, type='graph'),
                        md=6
                    ),
                    dbc.Col(
                        dcc.Loading(XY_scatter, type='graph'),
                        md=6
                    )
                ], 
            ),
        ], 
        id='graph-container', 
        style={
            'display': 'none'
            })
    ],
    fluid=True,
)

@callback(
        Output('graph-container', 'style'),
        Input('store', 'data')
)
def update_graph_contaienr(data):
    if data is None:
        return no_update

    return {}

app.run_server(jupyter_mode="tab", debug=True, use_reloader=True)