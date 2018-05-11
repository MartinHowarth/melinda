import itertools

from collections import defaultdict
from flask import session
from typing import List

from metaswitch_tinder import global_config
from metaswitch_tinder import database, tinder_email


class Match:
    def __init__(self, other_user, their_tags, bio, your_tags):
        self.other_user = other_user
        self.their_tags = their_tags
        self.bio = bio
        self.your_tags = your_tags


def tag_to_mentor_mapping(mentors: List[database.users.Mentor]):
    tag_map = defaultdict(list)
    for mentor in mentors:
        for tag in mentor.tags:
            tag_map[tag].append(mentor)
    return tag_map


def tag_to_request_mapping(mentees: List[database.users.Mentee]):
    tag_map = defaultdict(list)
    for mentee in mentees:
        for request in mentee.requests:
            for tag in request.tags:
                tag_map[tag].append(request)
    return tag_map


def matches_for_mentee(mentor_tag_map, mentee: database.users.Mentee):
    matches = []
    for request in mentee.requests:
        possible_mentors = list(itertools.chain(*[mentor_tag_map[tag] for tag in request.tags]))
        if possible_mentors:
            matches.extend([Match(mentor.username, mentor.tags, mentor.bio, request.tags) for mentor in possible_mentors])
    return matches


def matches_for_mentor(request_tag_map, mentor: database.users.Mentor):
    matches = []
    possible_requests = list(itertools.chain(*[request_tag_map[tag] for tag in mentor.tags]))
    if possible_requests:
        matches.extend([Match('hidden', request.tags, request.details, mentor.tags) for request in possible_requests])
    return matches


def generate_matches():
    mentees = database.users.get_mentees()
    mentors = database.users.get_mentors()
    request_tag_map = tag_to_request_mapping(mentees)
    mentor_tag_map = tag_to_mentor_mapping(mentors)

    if session['is_mentee']:
        return matches_for_mentee(mentor_tag_map, database.users.get_mentee(session['username']))
    return matches_for_mentor(request_tag_map, database.users.get_mentor(session['username']))


def handle_mentee_reject_match(matched_user):
    print("mentee rejected match:", matched_user)
    database.matches.handle_mentee_reject_match(matched_user)


def handle_mentee_accept_match(matched_user):
    print("mentee accepted match:", matched_user)
    database.matches.handle_mentee_accept_match(matched_user)
    # TODO - Add the mentee to the list of matches for the mentor

def handle_mentor_reject_match(matched_user):
    print("mentor rejected match:", matched_user)
    database.matches.handle_mentor_reject_match(matched_user)


def handle_mentor_accept_match(matched_user, matched_tags):
    print("mentor accepted match:", matched_user)
    database.matches.handle_mentor_accept_match(matched_user)
    current_user = database.users.get_mentor(session['username'])
    other_user = database.users.get_mentee(matched_user)
    tinder_email.send_email([current_user.email, other_user.email], "You've matched on " + (','.join(matched_tags)))
    # TODO - make the email text better
