
import datetime
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from components import header, data_buttons, tutorial, XYZ_scatter, XY_scatter

DCG_LOGO = 'https://engineering.jhu.edu/dcg/wp-content/uploads/2021/02/JH-WSE-DCG_Logo.png'
MAG_GLASS_ICON = 'https://media.istockphoto.com/id/1249867007/vector/analytics-analysis-statistics-searching-gray-icon.jpg?s=612x612&w=0&k=20&c=Yt4RBnpog9OU1uPu9LVONX69bxsdS_HjeHNP6CnFRYs='
PNNL_LOGO = 'https://www.pnnl.gov/sites/default/files/styles/hero_1600x1200/public/media/image/AT%20SCALE%20Hero%20Image.png?h=08b866d1&itok=4Q-utOef'

dir = 'data/Wall_4mm_400mm_LH0.225mm_MFR4.2_delay_1018-24-9-26-14-32-16'
local_filename = 'Transducer_4mm_400mm_LH0.225mm_move_over_for_delay_1018-24-9-26-14-32-16.txt'
df = pd.read_csv(f'{dir}/{local_filename}', skiprows=[1], skipfooter=38, engine='python')  
df.columns = df.columns.str.strip()
df = df.sort_index(axis=1)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        header,
        html.Hr(),
        data_buttons,
        tutorial,
        dbc.Row(dbc.Col(dcc.Loading(html.Div(id='output-data-upload', style={'padding-top': '10px', 'padding-bottom': '10px'})))),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        XYZ_scatter,
                        md=6
                    ),
                    dbc.Col(
                        XY_scatter,
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
        Output('output-data-upload', 'children'),
        Input('store', 'data'),
        Input('local_data', 'n_clicks'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified'),
)
def update_data_upload(stored_data, local_click, contents, filename, date):
    if stored_data is None:
        return no_update

    if stored_data['uploaded_data'] is False:
            return html.Div(
                    dbc.Container(
                        [
                            html.H3(f'File: {local_filename}', className='display-7', style={'textAlign':'left'}),
                            html.P(f'Shape: {df.shape}', className="lead")
                        ], 
                        className="py-3"
                    ),
                className='p-3 bg-body-secondary rounded-3'
            )
                
    
    elif contents is None:
        return None
    else:
        dff = pd.DataFrame(stored_data['df'])
        return html.Div(
            dbc.Container([
                    html.H3(f'File: {filename}', className='display-7', style={'textAlign':'left'}),
                    html.H5(f'Date Created: {datetime.datetime.fromtimestamp(date)}', style={'textAlign':'left'}),
                    html.P(f'Shape: {dff.shape}', className="lead")
                ], 
                className="py-3"),
            className='p-3 bg-body-secondary rounded-3'
        )






@callback(
        Output('graph-container', 'style'),
        Input('store', 'data'),
)
def update_graph_contaienr(data):
    if data is None:
        return no_update
    
    return {}





app.run_server(jupyter_mode="tab", debug=True, use_reloader=False)