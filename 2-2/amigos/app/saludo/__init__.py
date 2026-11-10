from flask import Blueprint

saludo = Blueprint("saludo", __name__)

from . import views