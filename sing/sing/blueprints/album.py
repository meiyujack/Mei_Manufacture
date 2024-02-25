from flask import jsonify,Blueprint

from sing.models import db,Album
from sqlalchemy import select

album_bp=Blueprint("album",__name__)

@album_bp.get("/all")
def album_all():
    album_all=db.session.execute(select(Album)).all()
    result=[]
    for album in album_all:
        raw=album[0].to_json()
        print(album[0].tracks)
        raw["tracks"]=[track.to_json for track in album[0].tracks]
        result.append(raw)
    return jsonify({"all_albums":result})