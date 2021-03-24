from flask import Blueprint

client = Blueprint('client',__name__, static_folder='assets')

from . import views
from . import json
