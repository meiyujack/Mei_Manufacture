from flask_login import login_required,current_user
from flask import redirect,url_for,Blueprint,flash

from sing.models import User,db

admin_bp=Blueprint("admin",__name__)

@login_required
@admin_bp.get("/authorize")
def authenticate():
    if current_user.is_authenticated:
        user = db.session.get(User, current_user.id)
        return user.role.name
    else:
        flash("未授权，请登陆",category="warning")
        return redirect(url_for("user.login"))