import dash_core_components as dcc
import dash_html_components as html
import random

from metaswitch_tinder.config_model import MetaswitchTinder


def easter(config: MetaswitchTinder):
    return html.Div(
        children=[
            html.Img(
                src=random.choice(config.ducks),
                style={'display': 'block',
                       'width': '100%',
                       'vertical-align': 'middle'}
            ),
        ],
    )
