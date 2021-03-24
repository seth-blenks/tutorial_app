from flask import Blueprint

admin = Blueprint('admin', __name__, static_folder='assets', url_prefix='/au/ua/1/ob/ad/')

from . import views
from . import json