import dash_core_components as dcc
import dash_html_components as html

from flask import session

from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import database, pages
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags

NAME = __name__.replace('.', '')

def settings_tab():
    print('settings', session)
    username = session.get('username', 'Not logged in!')
    if username is 'Not logged in!':
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=[
            html.H1("{}, Update your details".format(username),),
            html.Br(),
            create_equal_row([
                html.Label('Email:'),
                dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([
                html.Label('Location:', ),
                dcc.Input(value='', placeholder='Which office are you in?', type='text', id='location-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([html.Label('Biography:')]),
            dcc.Textarea(placeholder='Enter a biography', value='', id='biography-{}'.format(NAME),
                         style={'width': '100%'}),
            html.Br(),
            create_equal_row([html.Label('Mentoring topics:')]),
            multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
            html.Br(),
            create_equal_row([html.Label('Additional topic tags:')]),
            create_equal_row(
                [dcc.Input(placeholder='e.g. \"python\", \"object-oriented design\", \"session-based testing\"',
                           value='', type='text', id='details-{}'.format(NAME))]),
            html.Br(),
            html.Button("Save", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-primary btn-block"),
            html.Button("Delete Account", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-warning btn-block"),
        ],
        className="container",
    )