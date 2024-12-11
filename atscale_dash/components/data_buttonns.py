from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import base64
import io
import json
import pandas as pd

from .data_store import update_store, local_data

data_buttons = dbc.Row(
    [
        dbc.Col(
            [
                # dbc.Button(
                #     [
                #         html.I(className="fa-solid fa-server"),
                #         ' Local'
                #     ], 
                #     id='local_data',
                #     className="me-1",
                #     color='primary',
                #     n_clicks=0
                # ),
                dbc.Button(
                    [
                        dcc.Loading(
                            [   
                                html.I(className="fa-solid fa-upload"),
                                ' Load'
                            ],
                            id='load-loader',
                            overlay_style={"visibility":"visible", "filter": "blur(2px)"},
                            type='default'
                        )
                    ],
                    id="collapse-button",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Button(
                    [
                        html.I(className="fa-solid fa-filter"),
                        ' Filter'
                    ], 
                    id='open-offcanvas',
                    color='secondary',
                    outline=True,
                    n_clicks=0,
                    class_name="me-1",
                    disabled=True
                ),
                dbc.Button(
                    [   
                        dcc.Loading(
                            [   
                                html.I(className="fa-solid fa-file-export"),
                                ' Export'
                            ],
                            id='export-loader',
                            overlay_style={"visibility":"visible", "filter": "blur(2px)"},
                            type='default'
                        )
                    ], 
                    id='export-button',
                    className="me-1",
                    color='info',
                    n_clicks=0,
                    disabled=True
                ),
                dbc.Collapse(
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            # 'width': '100%',
                            # 'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False

                    ),
                    id="collapse",
                    is_open=False,
                ),
                dbc.Offcanvas(
                    html.Div([
                        html.P('Drag the sliders to select specific ranges for plotting. Static values are shown as badges.'),
                        dbc.ListGroup(id='filter_list', flush=False),
                    ]),
                    id='offcanvas',
                    title='Filter Data Values',
                    is_open=False,
                    backdrop=True
                ),
            ],  
            width="auto"
        ),
    ],
    class_name='text-center',
    align='center',
    justify="center",
)

@callback(    
    Output("open-offcanvas", "disabled"),
    Input('store', 'data')
)
def toggle_filter_button_disabled(data):
    if data:
        return False
    
    return True

@callback(
    Output('export-loader', 'children'),
    # Output('progress-spinner', 'children'),
    Input("export-button", "n_clicks"),
    Input({'type': 'property_range_slider', 'index': ALL}, 'value'),
    State({'type': 'property_range_slider', 'index': ALL}, 'id'),
)
def export_button_callback(n, slider_values, slider_ids):
    if n is None:
        return no_update
    else:    
        if n:
            print('export filtered datafarme')
            local_data.export_data(slider_values, slider_ids)
            return [html.I(className="fa-solid fa-file-export"),
                                    ' Export']

@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    
    return is_open

@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks"), Input('upload-data', 'contents'),],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, load_contents, is_open):
    if n:
        return not is_open
    
    return is_open

# @callback(
#     Output('loading-upload', 'display'),
#     Input('upload-data', 'contents'),
#     Input('store', 'data'),
#     # prevent_initial_call=True
# )
# def show_upload_loading(upload_contents, store_data):
#     triggered_id = ctx.triggered_id

#     if triggered_id == 'upload-data':
#         print('show loader')
#         return 'show'
#     elif triggered_id == 'store':
#         print('hide loader')
#         return 'hide'
#     else:
#         print('no update')
#         return no_update

@callback(
        Output('store', 'data'),
        Output('load-loader', 'children'),
        Output('export-button', 'disabled'),
        # Input('local_data', 'n_clicks'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
)
def update_store_callback(contents, filename):
    if contents is None:
        return no_update
    else:
        triggered_id = ctx.triggered_id

        # if triggered_id == 'local_data':
        #     upload = False
        # elif triggered_id == 'upload-data':
        #     upload = True

        upload = False

        out = update_store(contents, filename, upload)
        children = [html.I(className="fa-solid fa-upload"),
                                    ' Load']

        return out, children, False
    
def generate_filter_list_item(series):
    col_name = series.name
    min_val = series.min()
    max_val = series.max()
    val_range = max_val - min_val
    n_ticks = 20
    step_val = val_range/n_ticks

    if val_range == 0:
        item = dbc.Badge(min_val, className="ms-1")
    else:
        item = dcc.RangeSlider(
                    id={'type': 'property_range_slider', 'index': f'{col_name}'},
                    min=min_val, 
                    max=max_val,
                    step=step_val, 
                    marks=None,
                    persistence=False,
                    persistence_type='local',
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                        "style": {"color": "LightSteelBlue", "fontSize": "11px"},
                        "template": "{value}"
                    },
                )
                        
    out = dcc.Loading(
        dbc.ListGroupItem(
            [
                col_name,
                item
            ]
        ),
        overlay_style={"visibility":"visible", "filter": "blur(2px)"},
        type='default'
    )

    return out

@callback(
        Output('filter_list', 'children'), 
        Input('store', 'data'),
)
def generate_filter_list(data):
    if data is None:
        return no_update
    else:
        if data['uploaded_data']:
            dff = pd.DataFrame(data['df'])
        else:
            dff = local_data.df.copy()

        list_items = [generate_filter_list_item(dff[col_name]) for col_name in dff.columns.values]
        return list_items
    

@callback(
    [
        Output('scatter_color_name', 'options'),
        Output('xaxis_column_name', 'options'),
        Output('yaxis_column_name', 'options'),
        Output('2Dscatter_color_name', 'options'),
        Output('scatter_size_name', 'options')
    ],
    Input('store', 'data'),
)
def update_dropdowns(data):
    if data is None:
        return no_update
    else:
        if data['uploaded_data']:
            dff = pd.DataFrame(data['df'])
        else:
            dff = local_data.df.copy()

        return dff.columns.values, dff.columns.values, dff.columns.values, dff.columns.values, dff.columns.values

