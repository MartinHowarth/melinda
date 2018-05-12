import dash_core_components as dcc
import dash_html_components as html

from flask import session

from metaswitch_tinder.components.grid import create_equal_row


def layout():
    session['is_mentee'] = False
    return html.Div([
        html.H1("Metaswitch Tinder", className="cover-heading"),
        create_equal_row([
            dcc.Link("Sign in!", href='/mentor-signin', className="btn btn-lg btn-secondary"),
            dcc.Link("Sign up!", href='/mentor-signup', className="btn btn-lg btn-primary"),
        ])
    ],
        className="container text-center",)
