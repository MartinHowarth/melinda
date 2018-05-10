from .easter import easter
from .page_1 import page_1
from .page_2 import page_2
from .home import home
from .mentor_menu import mentor_menu
from . import mentee_landing_page


pages = {
    '/page-1': page_1,
    '/page-2': page_2,
    '/easter': easter,
    '/mentor-menu': mentor_menu,
    '/mentee-landing-page': mentee_landing_page.mentee_landing_page,
}
