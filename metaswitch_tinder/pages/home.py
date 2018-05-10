import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder


def home(config: MetaswitchTinder):
    return html.Div([
        html.A(html.Button('Page 1', id='button1'), href='/page-1'),
        html.Br(),
        dcc.Link('Go to Page 2', href='/page-2'),
    ])
