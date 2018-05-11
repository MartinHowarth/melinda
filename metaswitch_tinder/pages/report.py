import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from metaswitch_tinder import tinder_email

NAME = __name__.replace('.', '')


def report():
    return html.Div([
        html.H1("Report an issue", className="text-center"),
        html.Br(),
        dcc.Textarea(placeholder='Report an issue or inappropriate content.  '
                                 'Please include as much information as possible',
                     value='', id='report-{}'.format(NAME),
                     style={'width': '100%'}),
        html.A(html.Button("Submit Report", id='submit-{}'.format(NAME),
                    n_clicks=0, className="btn btn-sm btn-danger btn-block"),
               href="/")
    ], className="container text-center", id="report")


def add_callbacks(app):
    @app.callback(
        Output('report', 'children'),
        [],
        [
            State('report-{}'.format(NAME), 'value'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def report_email(report_text):
        print('report')
        tinder_email.send_report_email(report_text)
        return
