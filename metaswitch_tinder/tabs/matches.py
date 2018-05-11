import dash_core_components as dcc
import dash_html_components as html
import random

from dash.dependencies import Input, Output, State, Event

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import global_config, matches, database
from metaswitch_tinder.components.grid import create_equal_row


def children_no_matches():
    return [
            html.Br(),
            html.Img(src=random.choice(global_config.Global.CONFIG.sad_ducks),
                     className="rounded-circle", width=200, height=200),
            html.Br(),
            html.Br(),
            html.P("Aw shucks! You're out of matches!", className="lead"),
            html.Br(),
            html.Button("Return to start", className="btn btn-primary btn-lg btn-block"),
        ]


def children_for_match(match: matches.Match):
    return [
            html.Br(),
            create_equal_row([
                html.Button("✘", id='reject-match', className="btn btn-lg btn-secondary"),
                html.Img(src=global_config.Global.CONFIG.default_user_image,
                         className="rounded-circle", width=200, height=200),
                html.Button("✔", id='accept-match', className="btn btn-lg btn-primary"),
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Table([
                html.Tr([
                    html.Td("Name"),
                    html.Td(match.other_user)
                ], className="table-success"),
                html.Tr([
                    html.Td("Tags"),
                    html.Td(', '.join(match.tags))
                ], className="table-success"),
                html.Tr([
                    html.Td("Bio"),
                    html.Td(match.bio)
                ], className="table-success"),
               ], className="table table-condensed"),
            html.Div(match.other_user, id='current-other-user', style={'display': 'none'})
        ]


def get_matches_children():
    current_matches = matches.generate_matches()
    if not current_matches:
        children = children_no_matches()
    else:
        children = children_for_match(random.choice(current_matches))
    return children


def matches_tab(config: MetaswitchTinder=None):
    return html.Div(
        children=get_matches_children(),
        className="container text-center",
        id="match-div"
    )


def add_callbacks(app):
    @app.callback(
        Output('match-div', 'children'),
        [],
        [
            State('current-other-user', 'children'),
            State('accept-match', 'n_clicks'),
            State('reject-match', 'n_clicks'),
        ],
        [
            Event('accept-match', 'click'),
            Event('reject-match', 'click'),
        ]
    )
    def submit_mentee_information(other_user, n_accept_clicked, n_reject_clicked):
        if n_accept_clicked:
            if global_config.Global.IS_MENTEE:
                database.matches.handle_mentee_accept_match(other_user)
            else:
                database.matches.handle_mentor_accept_match(other_user)
        else:
            if global_config.Global.IS_MENTEE:
                database.matches.handle_mentee_reject_match(other_user)
            else:
                database.matches.handle_mentor_reject_match(other_user)
        return get_matches_children()
