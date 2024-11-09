from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

DCG_LOGO = 'https://engineering.jhu.edu/dcg/wp-content/uploads/2021/02/JH-WSE-DCG_Logo.png'
PNNL_LOGO = 'https://www.pnnl.gov/sites/default/files/styles/hero_1600x1200/public/media/image/AT%20SCALE%20Hero%20Image.png?h=08b866d1&itok=4Q-utOef'

header = dbc.Row(
    [
        dbc.Col(
            html.Img(src=DCG_LOGO, style={'width': '100%'}), 
            width={'size': 3}
        ),
        dbc.Col(
            html.H1('AT-SCALE Digital Twin Dashboard', style={'textAlign':'center', 'font-weight': 'bold'}), 
            key='test', 
            id='animated-text', 
            className="animate__animated animate__fadeInUp animate__faster",
        ),
        dbc.Col(
            html.Img(src=PNNL_LOGO, style={'width': '350px', 'height': '150px', 'object-fit': 'cover'}), 
            width={'size': 3}
        )
    ], 
    justify="center", 
    align='center'
)