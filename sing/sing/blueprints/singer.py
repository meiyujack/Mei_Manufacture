from flask import request,render_template,jsonify,Blueprint
from flask_login import login_required
from sqlalchemy import select

from sing.forms import SingerForm
from sing.models import db,Singer

singer_bp=Blueprint('singer',__name__)

@login_required
@singer_bp.route("/insert", methods=["GET", "POST"])
def singer_insert():
    if request.method == "GET":
        singer_form = SingerForm()
        return render_template('insert_singer.html', form=singer_form)
    # if request.method == "POST":
    #     user = db.session.get(User, current_user.id)
    #     track = Track(name=request.form['name'],
    #                   duration=request.form['duration'],
    #                   singer_id=request.form['singer_id'],
    #                   album_id=request.form['album_id'])
    #     result = track.insert(user)
    #     if not isinstance(result, OSError):
    #         return request.form['name'] + result
    #     else:
    #         raise result("权限不足")

@singer_bp.get("/singer/all")
def singer_all():
    singer_all=db.session.execute(select(Singer)).all()
    result=[]
    for singer in singer_all:
        raw=singer[0].to_json()
        result.append(raw)

    return jsonify({"all_singers":result})