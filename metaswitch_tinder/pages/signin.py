import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session

from metaswitch_tinder import database
from metaswitch_tinder.app import app
from metaswitch_tinder.components.grid import create_equal_row


NAME = __name__.replace('.', '')


def signin_redirected(next_page):
    def layout():
        return html.Div([
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Username:', className="text-center"),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
            html.Br(),
            dcc.Link(html.Button("Submit!", id='submit-{}'.format(NAME),
                                 n_clicks=0, className="btn btn-lg btn-primary btn-block"),
                     href=next_page),
        ],
            className="container", id='signin')
    return layout


@app.callback(
    Output('signin', 'children'),
    [],
    [
        State('username-{}'.format(NAME), 'value'),
    ],
    [Event('submit-{}'.format(NAME), 'click')]
)
def submit_signup_information(username):
    print('signin', session)
    database.identity.handle_signin_submit(username)
    print('signin', session)
    session['username'] = username
    print('signin', session)
