import itertools
import logging
import string
import time

from random import randint
from typing import List, Optional, Union

from sqlalchemy_utils import ScalarListType

from metaswitch_tinder.app import db

log = logging.getLogger(__name__)


class Tag(db.Model):
    """A tag that users can associate with requests and claim as skills."""

    _name = db.Column(db.String, primary_key=True)

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        value = self.normalise_tag(value)
        self._name = value

    def add(self):
        db.session.add(self)
        log.info(f"Added new tag to database: {self.name}")
        self.commit()

    def commit(self):
        db.session.commit()

    @staticmethod
    def normalise_tag(name: str) -> str:
        """
        Take a string and normalise it so that it matches a standard.

        That is:
            - Capital first letter of each word
            - No commas (the tags are separated by commas in the database)
        """
        normalised_name = name.replace(",", " ")
        normalised_name = string.capwords(normalised_name)
        log.debug("Normalised tag %s to: %s", name, normalised_name)
        return normalised_name


class Request(db.Model):
    """
    id - Randomly generated "unique" ID of request
    maker - Name of user who made the request (str)
    tags - Comma separated list of tags
    comment - Comment about request (str)
    """

    id = db.Column(db.String, primary_key=True)
    _maker = db.Column(db.String(80))  # Also the mentee, by definition.
    mentor = db.Column(
        db.String(80)
    )  # This is the (singular) mentor who has been matched with.
    comment = db.Column(db.String(2000))
    tags = db.Column(ScalarListType())  # type: List[str]
    _possible_mentors = db.Column(ScalarListType())  # type: List[str]
    _rejected_mentors = db.Column(ScalarListType())  # type: List[str]
    _accepted_mentors = db.Column(ScalarListType())  # type: List[str]

    def __init__(
        self,
        maker_email_or_user: Union[str, "User"],
        tags: Union[str, List[str]],
        comment: str = None,
    ) -> None:
        if not isinstance(tags, list) and tags is not None:
            tags = [tags]
        if isinstance(maker_email_or_user, User):
            maker_email_or_user = maker_email_or_user.email

        self.id = str(time.time()) + str(randint(1, 100))
        self._maker = maker_email_or_user
        self.tags = tags or []
        self.comment = comment or ""
        self._accepted_mentors = []
        self._possible_mentors = []
        self._rejected_mentors = []
        self.mentor = ""

    def __repr__(self):
        return (
            "Request<{self.id}>"
            "(maker={self.maker}, tags={self.tags}, comment={self.comment})".format(
                self=self
            )
        )

    def add(self):
        db.session.add(self)

        # Register this request with the user.
        user = self.get_maker()
        user.requests += [self]

        # Now go and work out which mentors are possible matches
        self.populate_initial_possible_mentors()

        self.commit()

    def commit(self):
        db.session.commit()

    def delete(self):
        for user in self.get_all_involved_users():
            user.handle_request_deletion(self)

        db.session.delete(self)
        self.commit()

    def handle_user_deletion(self, user: "User"):
        log.debug("%s: Handling user deletion: %s", self, user)
        for involved_user in self.get_all_involved_users():
            involved_user.handle_request_deletion(self)

        if user.email in self.accepted_mentors:
            users = self.accepted_mentors
            users.remove(user.email)
            self.accepted_mentors = users

        if user.email in self.possible_mentors:
            users = self.possible_mentors
            users.remove(user.email)
            self.possible_mentors = users

        if user.email in self.rejected_mentors:
            users = self.rejected_mentors
            users.remove(user.email)
            self.rejected_mentors = users

        if user.email == self.maker:
            log.info("Deleting request: %s", self)
            db.session.delete(self)
            self.commit()

    @property
    def maker(self) -> str:
        return self._maker

    @maker.setter
    def maker(self, value: Union[str, "User"]):
        if isinstance(value, User):
            self.maker = value.email
        else:
            self.maker = value

    def get_maker(self) -> "User":
        maker = get_user(self.maker)
        if maker is None:
            raise AssertionError(
                "Could not get maker from database with email: %s" % self.maker
            )
        return maker

    @property
    def accepted_mentors(self) -> List[str]:
        return self._accepted_mentors.copy()

    @accepted_mentors.setter
    def accepted_mentors(self, value: Union[List["User"], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.email)
            else:
                mentors.append(mentor)

        self._accepted_mentors = list(set(mentors))
        self.commit()

    def get_accepted_mentors(self) -> List["User"]:
        return get_users(self.accepted_mentors)

    @property
    def possible_mentors(self) -> List[str]:
        return self._possible_mentors.copy()

    @possible_mentors.setter
    def possible_mentors(self, value: Union[List["User"], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.email)
            else:
                mentors.append(mentor)

        self._possible_mentors = list(set(mentors))
        self.commit()

    def get_possible_mentors(self) -> List["User"]:
        return get_users(self.possible_mentors)

    def remove_possible_mentor(self, mentor: Union["User", str]):
        if isinstance(mentor, User):
            email = mentor.email
        else:
            email = mentor

        if email in self.possible_mentors:
            mentors = self.possible_mentors
            mentors.remove(email)
            self.possible_mentors = mentors
        self.commit()

    @property
    def rejected_mentors(self) -> List[str]:
        return self._rejected_mentors.copy()

    @rejected_mentors.setter
    def rejected_mentors(self, value: Union[List["User"], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.email)
            else:
                mentors.append(mentor)

        self._rejected_mentors = list(set(mentors))
        self.commit()

    def get_rejected_mentors(self) -> List["User"]:
        return get_users(self.rejected_mentors)

    @property
    def all_involved_users(self):
        return itertools.chain(
            [self.maker],
            [self.mentor],
            self.possible_mentors,
            self.rejected_mentors,
            self.accepted_mentors,
        )

    def get_all_involved_users(self) -> List["User"]:
        return get_users(list(self.all_involved_users))

    def populate_initial_possible_mentors(self):
        all_users = list_all_users()

        possible_mentors = []  # type: List['User']
        for user in all_users:
            if user.could_mentor_for_request(self):
                # Record this user as a possible mentor for this request
                possible_mentors.append(user)

                # And mark that mentor as involved in this request
                user.requests += [self]

        self.possible_mentors = possible_mentors
        self.commit()

    def handle_mentee_accept_mentor(self, mentor: "User"):
        """
        Called when a mentee accepts a mentor.

        A mentee can accept multiple mentors.
        """
        self.accepted_mentors += [mentor]

    def handle_mentee_reject_mentor(self, mentor: "User"):
        """
        Called when a mentee rejects a mentor.

        A mentee can reject multiple mentors.
        """
        self.rejected_mentors += [mentor]
        mentor.remove_request(self)

    def handle_mentor_accept_mentee(self, mentor: "User"):
        """Called when a mentor accepts a mentee. This can only be called once."""
        print("mentor %s accepted request: %s", mentor, self)
        self.mentor = mentor.email
        self.possible_mentors = []
        self.accepted_mentors = []
        self.rejected_mentors = []

        # Change this request to be a match for both mentor and mentee
        mentor.matches += [self]
        mentor.remove_request(self)

        mentee = self.get_maker()
        mentee.matches += [self]
        mentee.remove_request(self)

        self.commit()

    def handle_mentor_reject_mentee(self, mentor: "User"):
        """Called when a mentor rejects a mentee."""
        # Record rejected mentees the same as if the mentor had been rejected.
        self.rejected_mentors += [mentor]
        mentor.remove_request(self)


class User(db.Model):
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, primary_key=True)
    bio = db.Column(db.String(2000))
    mentoring_details = db.Column(db.String(2000))

    # Requests that this user is involved with. Both as a mentor and as a mentee.
    _requests = db.Column(ScalarListType())  # type: List[str]
    _tags = db.Column(ScalarListType())  # type: List[str]

    # The list of requests (for both mentors and mentees) that have been completed.
    _matches = db.Column(ScalarListType())  # type: List[str]

    def __init__(
        self,
        name: str,
        email: str,
        bio: str = None,
        tags: List[str] = None,
        mentoring_details: str = None,
    ) -> None:
        if not isinstance(tags, list) and tags is not None:
            tags = [tags]

        self.name = name
        self.email = email
        self.bio = bio or ""
        self.mentoring_details = mentoring_details or ""
        self._tags = tags or []

        self._requests = []
        self._matches = []

    def __repr__(self):
        return (
            "User(name={self.name}, email={self.email}, "
            "bio={self.bio}, tags={self.tags})".format(self=self)
        )

    def add(self):
        db.session.add(self)

        self.populate_all_possible_requests_to_mentor()

        self.commit()

    def commit(self):
        db.session.commit()

    def delete(self):
        for request in self.get_requests():
            request.handle_user_deletion(self)

        for request in self.get_matches():
            request.handle_user_deletion(self)

        db.session.delete(self)
        self.commit()

    def handle_request_deletion(self, request: Request):
        log.debug("%s: Handling request deletion: %s", self, request)
        self.remove_request(request)
        self.remove_match(request)

    @property
    def tags(self) -> List[str]:
        return self._tags.copy()

    def set_tags(self, tags: List[str]):
        self._tags = list(set(tags))
        self.commit()

        # Mentoring skills have changed, update possible requests to mentor.
        self.populate_all_possible_requests_to_mentor()

    @property
    def requests(self) -> List[str]:
        return self._requests.copy()

    @requests.setter
    def requests(self, value: Union[List["Request"], List[str]]):
        reqs = []
        for request in value:
            if isinstance(request, Request):
                reqs.append(request.id)
            else:
                reqs.append(request)

        self._requests = list(set(reqs))
        self.commit()

    def get_requests(self) -> List["Request"]:
        return get_requests_by_ids(self.requests)

    def remove_request(self, request: Request):
        request_ids = self.requests
        if request.id in request_ids:
            request_ids.remove(request.id)
            self.requests = request_ids

    def remove_match(self, match: Request):
        match_ids = self.matches
        if match.id in match_ids:
            match_ids.remove(match.id)
            self.matches = match_ids

    def get_requests_as_mentee(self):
        # Filter to only the requests made by this user.
        return [req for req in self.get_requests() if req.maker == self.email]

    def get_requests_as_mentor(self):
        # Filter to only the requests that this user didn't make.
        requests = [req for req in self.get_requests() if req.maker != self.email]

        # Filter out all the requests this mentor has rejected already
        requests = [req for req in requests if self.email not in req.rejected_mentors]
        return requests

    @property
    def matches(self) -> List[str]:
        return self._matches.copy()

    @matches.setter
    def matches(self, value: Union[List["Request"], List[str]]):
        mats = []
        for match in value:
            if isinstance(match, Request):
                mats.append(match.id)
            else:
                mats.append(match)

        self._matches = list(set(mats))
        self.commit()

    def get_matches(self) -> List["Request"]:
        return get_requests_by_ids(self.matches)

    def populate_all_possible_requests_to_mentor(self):
        log.info(
            "%s: populate_all_possible_requests_to_mentor initial requests: %s",
            self.email,
            self.requests,
        )
        requests = list_all_requests()

        matching_requests = []
        for request in requests:
            if self.could_mentor_for_request(request):
                # Mark this user as a possible match for the request
                request.possible_mentors += [self]

                # Mark this user as involved as well.
                matching_requests.append(request)
            else:
                request.remove_possible_mentor(self)

        matching_requests.extend(self.get_requests_as_mentee())

        self.requests = list(set(matching_requests))
        log.info(
            "%s: populate_all_possible_requests_to_mentor final requests: %s",
            self.email,
            self.requests,
        )
        self.commit()

    def could_mentor_for_request(self, request: Request) -> bool:
        """Returns True if this user could be the mentor for a request."""
        return (
            any((tag in self.tags for tag in request.tags))
            and request.maker != self.email
        )


def list_all_requests() -> List[Request]:
    return Request.query.all()


def get_request_by_id(request_id: str) -> Optional[Request]:
    return Request.query.filter_by(id=request_id).first()


def get_requests_by_ids(request_ids: List[str]) -> List[Request]:
    if not request_ids:
        return []
    return Request.query.filter(Request.id.in_(request_ids)).all()


def list_all_users() -> List[User]:
    return User.query.all()


def get_user(user_email: str) -> Optional[User]:
    return User.query.filter_by(email=user_email).first()


def get_users(emails: List[str]) -> List[User]:
    if not emails:
        return []
    return User.query.filter(User.email.in_(emails)).all()


def list_all_tags() -> List[Tag]:
    return Tag.query.all()


def handle_signup_submit(
    username: str,
    email: str,
    biography: str = None,
    categories: List[str] = None,
    details: str = None,
):
    print("Signup submitted:", username, email, biography)
    new_user = User(username, email, biography, categories, details)
    new_user.add()


def user_already_exists(user_email: str) -> bool:
    print("signin submitted:", user_email)
    all_users = list_all_users()
    all_user_emails = [user.email for user in all_users]
    print("all users:", all_user_emails)
    if user_email not in all_user_emails:
        return False
    return True


def create_request(user_email: str, categories: List[str], details: str):
    log.info("Creating request for %s: %s, %s", user_email, categories, details)
    request = Request(user_email, categories, details)
    request.add()
