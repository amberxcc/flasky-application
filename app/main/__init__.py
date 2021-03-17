from flask import Blueprint

main = Blueprint('main', __name__)

# 避免循环导入依赖，因为在 app/main/views.py 和 app/main/errors.py 中还要导入 main 蓝本
from . import views, errors
from ..models import Permission


# 在模板中也能访问权限Permission类
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
