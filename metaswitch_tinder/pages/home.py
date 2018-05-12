import dash_core_components as dcc
import dash_html_components as html
import logging

from flask import session

from metaswitch_tinder.components.grid import create_equal_row

log = logging.getLogger(__name__)


def layout():
    if 'username' in session:
        # Already logged in, skip the signin page
        mentor_href = '/mentor-menu'
    else:
        mentor_href = '/mentor-landing-page'

    return html.Div([
        html.H1("Metaswitch Tinder", className="cover-heading"),
        html.P("Metaswitch Tinder is a match-making service for informal mentoring and unofficial pastoral support "
               "at Metaswitch.",
               className="lead"),
        create_equal_row([
            dcc.Link("I'm a mentor!", href=mentor_href, className="btn btn-lg btn-secondary"),
            dcc.Link("I'm a mentee!", href='/mentee-landing-page', className="btn btn-lg btn-primary"),
        ]),
    ],
        className="container text-center",
    )
