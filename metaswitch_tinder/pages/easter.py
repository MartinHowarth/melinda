import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder


def easter(_config: MetaswitchTinder):
    return html.Div(
        children=[
            html.H1("Easter egg goes here!")
        ],
        className="container",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
