from .manage import User, Request, get_request_by_id, get_user, list_whole_table


def handle_mentee_added_request(username, email, categories, details):
    print("Mentee submitted:", username, email, categories, details)
    mentee = User(username, email, '', '', '')
    mentee.add()
    request = Request(username, categories, details)
    request.add()
    print(list_whole_table(Request))
    print(list_whole_table(User))


def handle_mentee_reject_match(request_id):
    print("mentee rejected match:", request_id)
    request = get_request_by_id(request_id)
    request.state = request.State.REJECTED
    request.commit()


def handle_mentee_accept_match(request_id, current_user, matched_user):
    print("mentee accepted match:", request_id)
    request = get_request_by_id(request_id)
    request.state = request.State.MATCHED
    request.commit()
    matched_user.add_mentor_match(current_user.username)


def handle_mentor_reject_match(request_id):
    print("mentor rejected match:", request_id)
    request = get_request_by_id(request_id)
    request.state = request.State.REJECTED
    request.commit()


def handle_mentor_accept_match(request_id):
    print("mentor accepted match:", request_id)
    request = get_request_by_id(request_id)
    request.state = request.State.MATCHED
    request.commit()
