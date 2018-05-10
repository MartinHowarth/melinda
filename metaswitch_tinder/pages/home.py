import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder


def home(_config: MetaswitchTinder):
    return html.Div([
        dcc.Link('Go to Page 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go to Page 2', href='/page-2'),
    ])
