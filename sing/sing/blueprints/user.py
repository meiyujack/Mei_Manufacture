from flask import url_for
from flask_login import login_user
from sing.forms import LoginForm
from sing.models import db,User

from flask import request,render_template,redirect,Blueprint
from sqlalchemy import select

import datetime

user_bp=Blueprint("user",__name__)


@user_bp.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        print(request.headers)
        login_form = LoginForm()
        return render_template('login.html', form=login_form)
    if request.method == "POST":
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        curr_user = db.session.execute(
            select(User).where(User.nickname == nickname)).first()[0]
        if curr_user:
            if curr_user.check_password(password):
                login_user(curr_user,
                           remember=request.form.get("remember"),
                           duration=datetime.timedelta(days=3))
                return redirect(url_for("authenticate"))