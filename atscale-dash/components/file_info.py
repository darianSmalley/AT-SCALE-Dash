import datetime
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from .data_store import local_data

file_info = dbc.Row(dbc.Col(html.Div(id='output-data-upload', style={'padding-top': '10px', 'padding-bottom': '10px'})))

@callback(
        Output('output-data-upload', 'children'),
        Input('store', 'data'),
        # Input('local_data', 'n_clicks'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified'),
)
def update_data_upload(stored_data, contents, filename, date):
    if stored_data is None:
        return no_update

    if stored_data['uploaded_data'] is False:
            return html.Div(
                    dbc.Container(
                        [
                            html.H3(f'File: {local_data.filename}', className='display-7', style={'textAlign':'left'}),
                            html.P(f'Shape: {local_data.df.shape}', className="lead")
                        ], 
                        className="py-3"
                    ),
                className='p-3 bg-body-secondary rounded-3'
            )
                
    
    elif contents is None:
        return None
    else:
        # dff = pd.DataFrame(stored_data['df'])
        return html.Div(
            dbc.Container([
                    html.H3(f'File: {local_data.filename}', className='display-7', style={'textAlign':'left'}),
                    html.H5(f'Date Created: {datetime.datetime.fromtimestamp(date)}', style={'textAlign':'left'}),
                    html.P(f'Shape: {local_data.df.shape}', className="lead")
                ], 
                className="py-3"),
            className='p-3 bg-body-secondary rounded-3'
        )