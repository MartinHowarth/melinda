import dash_core_components as dcc
import dash_html_components as html

from .config_model import MetaswitchTinder


def create_app_layout(_config: MetaswitchTinder):
    def regenerate_layout():
        return html.Div(
            children=[
                html.H1("Hello from Metaswitch Tinder!")
            ],
            className="container",
            id="main",  # Must match the ID in the "startLoops" javascript function.
        )
    return regenerate_layout
