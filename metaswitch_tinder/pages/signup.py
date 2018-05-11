import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session

from metaswitch_tinder import global_config
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import database, pages
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags

NAME = __name__.replace('.', '')


def signup_redirected(next_page):
    def signup():
        session['is_mentee'] = False
        return html.Div([
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Username:', ),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
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
            dcc.Textarea(placeholder='Enter a biography', value='Loves ducks', id='biography-{}'.format(NAME), style={'width':'100%'}),
            html.Br(),
            create_equal_row([html.Label('Mentoring topics:')]),
            multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
            html.Br(),
            create_equal_row([html.Label('Additional topic tags:')]),
            create_equal_row([dcc.Input(placeholder='e.g. \"python\", \"object-oriented design\", \"session-based testing\"',
                                        value='', type='text', id='details-{}'.format(NAME))]),
            html.Br(),
            html.Button("Submit!", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-primary btn-block"),
            html.Div(next_page, id='next-page', style={'display': 'none'})
        ], className="container", id='signup')
    return signup


def add_callbacks(app):
    @app.callback(
        Output('signup', 'children'),
        [],
        [
            State('username-{}'.format(NAME), 'value'),
            State('email-{}'.format(NAME), 'value'),
            State('biography-{}'.format(NAME), 'value'),
            State('categories-{}'.format(NAME), 'value'),
            State('details-{}'.format(NAME), 'value'),
            State('next-page', 'children'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def submit_signup_information(username, email, biography, categories, details, next_page):
        session['username'] = username
        database.identity.handle_signup_submit(username, email, biography, categories, details)
        return pages.pages[next_page]()
