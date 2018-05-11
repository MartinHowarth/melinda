import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import global_config


def mentor_landing_page(config: MetaswitchTinder):
    global_config.Global.IS_MENTEE = False
    return html.Div([
        html.H1("Metaswitch Tinder", className="cover-heading"),
        create_equal_row([
            html.A("Sign in!", href='/mentor-signin', className="btn btn-lg btn-secondary"),
            html.A("Sign up!", href='/mentor-signup', className="btn btn-lg btn-primary"),
        ])
    ],
        className="container text-center",)
