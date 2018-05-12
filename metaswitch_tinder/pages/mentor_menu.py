from metaswitch_tinder.components.tabs import generate_tabs
from metaswitch_tinder.database.manage import User, list_all_users, get_user


def layout():
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches', 'Settings': 'settings'}, 'matches')
