
from dash import Dash
import dash_bootstrap_components as dbc

from .components import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.layout = layout

if __name__ == "__main__":
    app.run_server(jupyter_mode="tab", debug=True, use_reloader=True)