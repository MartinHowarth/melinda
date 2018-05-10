from schematics.models import Model
from schematics.types import ModelType, URLType


class MetaswitchTinder(Model):
    css_cdn = URLType(default='https://maxcdn.bootstrapcdn.com/bootswatch/4.0.0/minty/bootstrap.min.css')
    duck = URLType(required=True)
