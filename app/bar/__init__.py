from flask import Blueprint

bp = Blueprint('bar', __name__)

from app.bar import routes
