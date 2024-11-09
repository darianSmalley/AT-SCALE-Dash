from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

MAG_GLASS_ICON = 'https://media.istockphoto.com/id/1249867007/vector/analytics-analysis-statistics-searching-gray-icon.jpg?s=612x612&w=0&k=20&c=Yt4RBnpog9OU1uPu9LVONX69bxsdS_HjeHNP6CnFRYs='

tutorial = dbc.Row(
    dbc.Col(
        [
            html.H1('Load data to start!', className='display-3 text-muted'),
            html.Img(src=MAG_GLASS_ICON, 
                        style={'width': '13.33%', 'animation-name': 'fadeInUp'},
                        className="animate__animated animate__fadeInUp animate__slower"),
        ]
    ),
    id='tutorial',
    class_name='text-center',
    align='center',
    justify="center",
)

@callback(    
    Output("tutorial", "style"),
    Input('store', 'data')
)
def toggle_tutorial(data):
    if data:
        return {'display': 'none'}
    
    return {}