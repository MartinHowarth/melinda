from .easter import easter
from .page_1 import page_1
from .page_2 import page_2
from .home import home
from .mentor_menu import mentor_menu
from .mentee_menu import mentee_menu
from .signin import signin_redirected
from .signup import signup_redirected
from . import mentee_landing_page, mentor_landing_page, signup, signin


pages = {
    '/page-1': page_1,
    '/page-2': page_2,
    '/easter': easter,
    '/mentor-landing-page': mentor_landing_page.mentor_landing_page,
    '/mentor-signin': signin_redirected('/mentor-menu'),
    '/mentor-signup': signup_redirected('/mentor-menu'),
    '/mentor-menu': mentor_menu,
    '/mentee-signin': signin_redirected('/mentee-landing-page'),
    '/mentee-signup': signup_redirected('/mentee-landing-page'),
    '/mentee-menu': mentee_menu,
    '/mentee-landing-page': mentee_landing_page.mentee_landing_page,
}
