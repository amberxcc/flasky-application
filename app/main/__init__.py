from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


# 在模板中也能访问权限
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
