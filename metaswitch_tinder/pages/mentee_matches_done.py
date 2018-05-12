import dash_core_components as dcc
import dash_html_components as html


def layout():
    return [
        html.Br(),
        html.H4("Thanks, your request has been submitted",
                className="text-center"),
        html.Br(),
        dcc.Link(html.Button("Make another request?", className="btn btn-primary btn-lg btn-block"),
                 href='/mentee-landing-page'),
        html.Br(),
    ]
