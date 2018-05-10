import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder


def matches(config: MetaswitchTinder):
    return html.Div(
        children=[
            html.H1("Here are your matches")
        ],
        className="container",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
