import base64
import io
from dash import no_update
from dash.exceptions import PreventUpdate
import pandas as pd

from .util import apply_filter

def load_df(filename, decoded=None):
    try:
        if 'csv' in filename:
            # Assume a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            # Assume a text file formatted by the DED printer
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=[1], skipfooter=38, engine='python') 
    except Exception as e:
        print(e)
        return no_update

    df.columns = df.columns.str.strip()
    df = df.sort_index(axis=1)
    return df

def parse_contents(contents):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    return decoded

def update_store(contents, filename, upload=False):
    if contents is None:
        return None    
    else:
        decoded = parse_contents(contents)
        df = load_df(filename, decoded)
        
        if upload:
            d = df.to_dict('records')
            datastore = {
                "df": d,
                "uploaded_data": True,
            }
        else:
            local_data.set_df(df)
            local_data.set_filename(filename)
            datastore = {
                "uploaded_data": False,
                "update_local_data": True
            }
        
        return datastore

def server_store(n_clicks):
    if n_clicks:
        d = {'uploaded_data': False}
        return d
    else:
        return None
    
class _local_data:
    def __init__(self):
        # self.root_dir = 'data'
        # self.dir = 'Wall_4mm_400mm_LH0.225mm_MFR4.2_delay_1018-24-9-26-14-32-16'
        # self.filename = 'Transducer_4mm_400mm_LH0.225mm_move_over_for_delay_1018-24-9-26-14-32-16.txt'
        # df = pd.read_csv(f'{self.root_dir}/{self.dir}/{self.filename}', skiprows=[1], skipfooter=38, engine='python')
        # df.columns = df.columns.str.strip()
        # self.df = df.sort_index(axis=1)
        self.root_dir = None
        self.dir = None
        self.filename = None
        self.df = None

    def set_df(self, df):
        self.df = df

    def set_filename(self, filename):
        self.filename = filename
    
    def export_data(self, slider_values, slider_ids):
        print('in export data')
        dff = self.df.copy()
        dff = apply_filter(dff, slider_values, slider_ids)
        out_filepath = f'{self.root_dir}/{self.dir}/{self.filename}_filtered.csv'
        dff.to_csv(out_filepath, index=False)

local_data = _local_data()