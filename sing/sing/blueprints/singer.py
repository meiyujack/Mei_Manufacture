from flask import request,render_template,jsonify,Blueprint
from flask_login import login_required
from sqlalchemy import select

from sing.forms import SingerForm
from sing.models import db,Singer
from sing.utils import turn_rows_into_dict

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

@singer_bp.get("/all")
def singer_all():
    singer_all=db.session.execute(select(Singer)).all()
    return render_template("singer_all.html",singers=turn_rows_into_dict(singer_all))

@singer_bp.get("/<singer_id>")
def singer_one(singer_id):
    return render_template("singer_all.html",singers=[db.session.execute(select(Singer).where(Singer.id==singer_id)).one_or_none()[0].to_json()])