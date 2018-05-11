from typing import List


class Mentee:
    # This is definitely not set in stone - just needed something to work against
    def __init__(self, username, requests, email=""):
        self.username = username
        self.requests = requests
        self.email = email


class Mentor:
    # This is definitely not set in stone - just needed something to work against
    def __init__(self, username, tags: List[str], bio, email=""):
        self.username = username
        self.tags = tags
        self.bio = bio
        self.email = email


class Request:
    # This is definitely not set in stone - just needed something to work against
    def __init__(self, tags, details):
        self.tags = tags
        self.details = details


def get_mentee(username):
    # TODO
    print("getting mentee:", username)
    return Mentee('Abe', [
            Request(['SIP', 'ducks'], 'Talking ducks. Obviously')
        ])


def get_mentor(username):
    # TODO
    print("getting mentor:", username)
    return Mentor('Felicity', ['SIP'], 'CFS CFS')


def get_mentees():
    # TODO actually get all mentees from database
    return [
        Mentee('Abe', [
            Request(['SIP', 'ducks'], 'Talking ducks. Obviously')
        ]),
        Mentee('Lincoln', [
            Request(['SIP'], 'love phone calls')
        ]),
    ]


def get_mentors():
    # TODO actually get all mentors from database
    return [
        Mentor('Felicity', ['SIP'], 'CFS CFS'),
        Mentor('Ambrosia', ['SIP'], 'Quack'),
    ]
