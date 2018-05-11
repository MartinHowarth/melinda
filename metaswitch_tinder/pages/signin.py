import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import global_config
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import database


NAME = __name__.replace('.', '')


def signin_redirected(next_page):
    def signin(config: MetaswitchTinder=None):
        return html.Div([
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Username:', className="text-center"),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
            html.Br(),
            html.A(html.Button("Submit!", id='submit-{}'.format(NAME),
                               n_clicks=0, className="btn btn-lg btn-primary btn-block"),
                   href=next_page)
        ],
            className="container", id='signin')
    return signin


def add_callbacks(app):
    @app.callback(
        Output('signin', 'children'),
        [],
        [
            State('username-{}'.format(NAME), 'value'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def submit_signup_information(username):
        print("here")
        global_config.Global.USERNAME = username
        database.identity.handle_signin_submit(username)
        return
