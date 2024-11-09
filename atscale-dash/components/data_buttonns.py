from dash import Dash, html, dcc, Input, Output, callback, State, dash_table, no_update, ctx, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import base64
import io
import json

data_buttons = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Button(
                    [
                        html.I(className="fa-solid fa-server"),
                        ' Server'
                    ], 
                    id='local_data',
                    className="me-1",
                    color='primary',
                    n_clicks=0
                ),
                dbc.Button(
                    [
                        html.I(className="fa-solid fa-upload"),
                        ' Upload'
                    ],
                    id="collapse-button",
                    className="me-1",
                    color="info",
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
                dbc.Collapse(
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
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
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    
    return is_open

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

def parse_contents(contents):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    return decoded

def load_df(filename, decoded):
    try:
        if 'csv' in filename:
            # Assume a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            # Assume a text file formatted by the DED printer
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=[1], skipfooter=38, engine='python') 
    except Exception as e:
        print(e)
        return no_update

    return df

@callback(
        Output('store', 'data'),
        Input('local_data', 'n_clicks'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
)
def update_store(local_click, contents, filename):
    triggered_id = ctx.triggered_id

    if triggered_id == 'local_data':
        return local_store(local_click)
    elif triggered_id == 'upload-data':
        return upload_store(contents, filename)

def upload_store(contents, filename):
    if contents is None:
        return None    
    else:
        decoded = parse_contents(contents)
        dff = load_df(filename, decoded)
        dff.columns = dff.columns.str.strip()
        dff = dff.sort_index(axis=1)
        d = dff.to_dict('records')
        datastore = {
            "df": d,
            "uploaded_data": True
        }
        return datastore
    
def local_store(n_clicks):
    if n_clicks:
        d = {'uploaded_data': False}
        return d
    else:
        return None
    
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

    if data['uploaded_data']:
        dff = pd.DataFrame(data['df'])
    else:
        dff = df.copy()

    list_items = [generate_filter_list_item(dff[col_name]) for col_name in dff.columns.values]
    return list_items

def apply_filter(df, slider_values, slider_ids):
    for value, id in zip(slider_values, slider_ids):
        if value:
            low, high = value
            col_name = id['index']
            mask = (df[col_name] >= low) & (df[col_name] <= high)
            df = df[mask]
    
    return df

@callback(
    [
        Output('scatter_color_name', 'options'),
        Output('xaxis_column_name', 'options'),
        Output('yaxis_column_name', 'options'),
    ],
    Input('store', 'data'),
)
def update_dropdowns(data):
    if data is None:
        return no_update
    
    if data['uploaded_data']:
        dff = pd.DataFrame(data['df'])
    else:
        dff = df.copy()

    return dff.columns.values, dff.columns.values, dff.columns.values
