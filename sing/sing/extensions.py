from flask import request,current_app
from flask_login import LoginManager,current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db=SQLAlchemy()
csrf=CSRFProtect()


login_manager=LoginManager()
login_manager.login_view='user.login'
login_manager.login_message="请登陆访问该页面。"


from sing.models import User
@login_manager.user_loader
def load_user(id) -> User:
    return User(id=id)

