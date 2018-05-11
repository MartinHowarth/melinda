import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event

import metaswitch_tinder.database.matches
from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags
from metaswitch_tinder import database, global_config


NAME = __name__.replace('.', '')


def mentee_landing_page(config: MetaswitchTinder):
    global_config.Global.IS_MENTEE = True
    if global_config.Global.USERNAME:
        is_signed_in_fields = [
            html.H4("Welcome {}!".format(global_config.Global.USERNAME),
                    className="text-center"),
            # Must include something with the id `email-NAME`, but hidden in this case
            dcc.Input(value='', type='text', id='email-{}'.format(NAME), style={'display': 'none'})
        ]
    else:
        is_signed_in_fields = [
            html.A(html.Button("I have an account!",
                               id='sign-in-{}'.format(NAME),
                               className="btn btn-lg btn-primary btn-block"),
                   href='/mentee-signin'),
            html.Br(),
            create_equal_row([
                html.Label('Email:', className="text-center"),
                dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
            ]),
        ]

    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        *is_signed_in_fields,
        html.Br(),
        html.H4('What do you want to learn about?', className="text-center"),
        html.Br(),
        multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
        html.Br(),
        html.H4('What specifically about that?', className="text-center"),
        html.Br(),
        create_equal_row([dcc.Input(value='', type='text', id='details-{}'.format(NAME))]),
        html.Br(),
        html.A(html.Button("Submit!",
                           id='submit-{}'.format(NAME),
                           className="btn btn-lg btn-primary btn-block"),
               href='/mentee-menu')
    ],
        className="container", id='my-div')


def add_callbacks(app):
    @app.callback(
        Output('my-div'.format(NAME), 'children'),
        [],
        [
            State('email-{}'.format(NAME), 'value'),
            State('categories-{}'.format(NAME), 'value'),
            State('details-{}'.format(NAME), 'value'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def submit_mentee_information(email, categories, details):
        metaswitch_tinder.database.matches.handle_mentee_added_request(email, categories, details)
        return
