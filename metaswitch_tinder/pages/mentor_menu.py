import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.generate_tabs import generate_tabs


def mentor_menu(config: MetaswitchTinder):
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches'}, 'matches')