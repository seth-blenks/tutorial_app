from flask import Blueprint

admin = Blueprint('admin', __name__, static_folder='assets', url_prefix='/admin/')

from . import views
from . import json