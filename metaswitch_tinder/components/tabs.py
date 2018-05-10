import dash_core_components as dcc
import dash_html_components as html

from typing import Dict


def generate_tabs(tabs: Dict[str, html.Div], default_tab_value: html.Div) -> html.Div:
    """
    :param tabs: Dict of {"tab_name": html.Div(tab contents)}
    :param default_tab_value: The default value to display
    :return: html.Div for the tabs.
    """
    formatted_dict = [
        {'label': key, 'value': value} for key, value in tabs.items()
    ]

    return html.Div([
        dcc.Tabs(
            tabs=formatted_dict,
            value=default_tab_value,
            id='tabs'
        ),
        html.Div(id='tab-content')
    ], style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    })
