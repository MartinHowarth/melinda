from metaswitch_tinder import global_config


class Match:
    def __init__(self, other_user, tags, bio):
        self.other_user = other_user
        self.tags = tags
        self.bio = bio


def generate_matches():
    # TODO - Somehow mark that a match has been rejected/accepted and don't show it
    print("generating matches for:", global_config.Global.USERNAME)
    return [Match('fred', ['ducks'], '*loves ducks*'), Match('Georgia', ['bread', 'butter'], 'is bread')]
