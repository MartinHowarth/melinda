import itertools

from collections import defaultdict
from typing import List

from metaswitch_tinder import global_config
from metaswitch_tinder import database


class Match:
    def __init__(self, other_user, tags, bio):
        self.other_user = other_user
        self.tags = tags
        self.bio = bio


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
            matches.extend([Match(mentor.username, mentor.tags, mentor.bio) for mentor in possible_mentors])
    return matches


def matches_for_mentor(request_tag_map, mentor: database.users.Mentor):
    matches = []
    possible_requests = list(itertools.chain(*[request_tag_map[tag] for tag in mentor.tags]))
    if possible_requests:
        matches.extend([Match('hidden', request.tags, request.details) for request in possible_requests])
    return matches


def generate_matches():
    mentees = database.users.get_mentees()
    mentors = database.users.get_mentors()
    request_tag_map = tag_to_request_mapping(mentees)
    mentor_tag_map = tag_to_mentor_mapping(mentors)

    if global_config.Global.IS_MENTEE:
        return matches_for_mentee(mentor_tag_map, database.users.get_mentee(global_config.Global.USERNAME))
    return matches_for_mentor(request_tag_map, database.users.get_mentor(global_config.Global.USERNAME))
