import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags
from metaswitch_tinder import database


NAME = __name__.replace('.', '')


def mentee_landing_page(config: MetaswitchTinder):
    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        html.Button("I have an account!", id='sign-in-{}'.format(NAME), className="btn btn-lg btn-primary btn-block"),
        html.Br(),
        create_equal_row([
            html.Label('Email:', className="text-center"),
            dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
        ]),
        html.Br(),
        html.H4('I want to learn about...', className="text-center"),
        html.Br(),
        multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
        html.Br(),
        html.H4('Specifically regarding...', className="text-center"),
        html.Br(),
        create_equal_row([dcc.Input(value='', type='text', id='details-{}'.format(NAME))]),
        html.Br(),
        html.Button("Submit!", id='submit-{}'.format(NAME), n_clicks=0, className="btn btn-lg btn-primary btn-block"),
    ],
        className="container", id='my-div')


def add_submit_callback(app):
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
        database.input.handle_mentee_submit(email, categories,details)
        # TODO link to next page
        return html.Div("Submitted! %s, %s %s" % (email, categories, details))
