from flask import request,render_template,jsonify,Blueprint
from sqlalchemy import select

from sing.forms import TrackForm
from sing.utils import turn_row_into_tuple
from flask_login import login_required,current_user
from sing.models import db,Singer,Album,User,Track

track_bp=Blueprint("track",__name__)


@login_required
@track_bp.route("/insert", methods=["GET", "POST"])
def track_insert():
    if request.method == "GET":
        track_form = TrackForm()
        track_form.singer_id.choices = turn_row_into_tuple(
            db.session.execute(select(Singer.id, Singer.name)).all())
        track_form.album_id.choices = turn_row_into_tuple(
            db.session.execute(select(Album.id, Album.name)).all())
        return render_template('insert_track.html', form=track_form)
    if request.method == "POST":
        user = db.session.get(User, current_user.id)
        track = Track(name=request.form['name'],
                      duration=request.form['duration'],
                      singer_id=request.form['singer_id'],
                      album_id=request.form['album_id'])
        result = track.insert(user)
        if not isinstance(result, OSError):
            return request.form['name'] + result
        else:
            raise result("权限不足")
        
@login_required
@track_bp.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        track_form = TrackForm()
        track_form.singer_id.choices = turn_row_into_tuple(
            db.session.execute(select(Singer.id, Singer.name)).all())
        track_form.album_id.choices = turn_row_into_tuple(
            db.session.execute(select(Album.id, Album.name)).all())
        return render_template('update_track.html', form=track_form,tracks=db.session.execute(select(Track.name,Track.duration)).all())
    if request.method == "POST":
        user = db.session.get(User, current_user.id)
        track = Track(name=request.form['name'],
                      duration=request.form['duration'],
                      singer_id=request.form['singer_id'],
                      album_id=request.form['album_id'])
        result = track.insert(user)
        if not isinstance(result, OSError):
            return request.form['name'] + result
        else:
            raise result("权限不足")


@track_bp.get("/all")
def track_all():
    track_all = db.session.execute(select(Track)).all()
    result=[]
    for track in track_all:
        raw=track[0].to_json()
        raw["singer_id"]=track[0].singer.name
        raw["album_id"]=track[0].album.name
        result.append(raw)
    return jsonify({"all_tracks":result})