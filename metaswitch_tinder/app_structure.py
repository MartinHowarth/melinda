"""Module that defines how app pages link to other app pages."""
import sys

from flask import session

from metaswitch_tinder import app_globals


def if_logged_in_else(logged_in_target, other_target) -> callable:
    def decide_later() -> str:
        if 'username' in session:
            # Already logged in, skip the signin page
            return logged_in_target
        return other_target
    return decide_later


def module_href(module: object) -> str:
    if 'home' in module.__name__:
        return '/'
    return '/' + module.__name__.split('.')[-1].replace('_', '-')


def href(module_name: str, ref: str=None) -> str:
    _module_href = module_href(sys.modules[module_name])
    if ref is None:
        return _module_href

    href_or_func = app_globals.structure[_module_href]['links'][ref]

    if callable(href_or_func):
        return href_or_func()
    return href_or_func


def generate_structure():
    """
    Generate the definition of the app structure.

    This function defines how pages link to each other.

    All `href`s should be define here in the `links` section for that page.
    """
    # This function must be called before the app is started up.

    # These imports happen here to avoid an infinite loop.
    from metaswitch_tinder.pages import (
        easter,
        page_1,
        page_2,
        user_menu,
        signin,
        signup,
        mentee_landing_page,
        signin_or_signup,
        report,
        home,
    )
    from metaswitch_tinder.tabs import (
        matches,
        messages,
        settings,
    )

    app_globals.structure = {
        module_href(home): {
            'module': home,
            'links': {
                home.im_a_mentee: module_href(mentee_landing_page),
                home.im_a_mentor: if_logged_in_else(module_href(user_menu),
                                                    module_href(signin_or_signup)),
            }
        },
        module_href(mentee_landing_page): {
            'module': mentee_landing_page,
            'links': {
                mentee_landing_page.sign_in: module_href(signin),
                mentee_landing_page.submit_request: module_href(user_menu),
            }
        },
        module_href(signin_or_signup): {
            'module': signin_or_signup,
            'links': {
                signin_or_signup.signin: module_href(signin),
                signin_or_signup.signup: module_href(signup),
            }
        },
        module_href(signin): {
            'module': signin,
            'links': {
                signin.submit: module_href(user_menu),
            }
        },
        module_href(signup): {
            'module': signup,
            'links': {
                signup.submit: module_href(user_menu),
            }
        },
        module_href(report): {
            'module': report,
            'links': {
                report.submit: module_href(home),
            }
        },
        module_href(user_menu): {
            'module': user_menu,
            'links': {
            }
        },
        module_href(matches): {
            'module': matches,
            'links': {
                matches.make_a_request: module_href(mentee_landing_page),
            }
        },
    }