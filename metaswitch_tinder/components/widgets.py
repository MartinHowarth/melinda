import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session


def logout_button():
    return html.A(html.Button("Logout!", id='logout',
                              className="btn btn-lg btn-primary btn-block"),
                  href='/', id='dummy')


def add_callbacks(app):
    @app.callback(
        Output('dummy', 'children'),
        [],
        [],
        [Event('logout', 'click')]
    )
    def handle_logout():
        del session['username']
        del session['is_mentee']
        return
