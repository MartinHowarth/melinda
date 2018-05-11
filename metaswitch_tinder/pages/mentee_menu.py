from metaswitch_tinder.components.tabs import generate_tabs


def mentee_menu():
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches', 'Settings': 'settings'}, 'matches')
