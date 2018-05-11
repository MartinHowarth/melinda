import dash_core_components as dcc
import dash_html_components as html

from flask import session


def messages():
    print('messages', session)
    username = session.get('username', 'Not logged in!')
    if username is 'Not logged in!':
        print('not logged in', session)
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=[
            html.H1("{}, here are your messages".format(username))
        ],
        className="container",
    )
