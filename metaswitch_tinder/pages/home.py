import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.grid import create_equal_row


def home(config: MetaswitchTinder):
    return html.Div([
        html.H1("Metaswitch Tinder", className="cover-heading"),
        html.P("Metaswitch Tinder is a match-making service for informal mentoring and unofficial pastoral support "
               "at Metaswitch.",
               className="lead"),
        create_equal_row([
            html.A("I'm a mentor!", href='/mentor-menu', className="btn btn-lg btn-secondary"),
            html.A("I'm a mentee!", href='/page-2', className="btn btn-lg btn-primary"),
        ])
    ],
        className="container text-center",)
