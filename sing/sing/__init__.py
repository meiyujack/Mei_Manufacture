import os
import datetime

from flask import Flask
from flask_login import current_user

from sing.blueprints.user import user_bp
from sing.blueprints.singer import singer_bp
from sing.blueprints.album import album_bp
from sing.blueprints.track import track_bp
from sing.blueprints.admin import admin_bp  
from sing.extensions import login_manager,csrf
from sing.models import db,User,Role,Permission,Singer,Album,Track
from sing.settings import config

def create_app(config_name=None):
    if config_name is None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app=Flask('sing')
    app.config.from_object(config[config_name])
    app.json.ensure_ascii = False

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(singer_bp,url_prefix="/singer")
    app.register_blueprint(album_bp,url_prefix="/album")
    app.register_blueprint(track_bp,url_prefix="/track")
    app.register_blueprint(admin_bp,url_prefix="/admin")



def register_commands(app):
    @app.cli.command()
    def create_db():
        db.drop_all()
        db.create_all()
        print("Recreated database.")

    @app.cli.command()
    def init_db():
        jay_chou = Singer(name="周杰伦", birth=datetime.date(1979, 1, 18))
        jay = Album(name="Jay",
                    publish_time=datetime.date(2000, 11, 7),
                    singer_id=1)
        adorable_lady = Track(name="可爱女人",
                              duration="3:59",
                              singer_id=1,
                              album_id=1)
        perfectionism = Track(name="完美主义",
                              duration="4:04",
                              singer_id=1,
                              album_id=1)
        visitor = Role(name="游客")
        fan = Role(name="粉丝")
        admin = Role(name="管理员")

        no_permission = Permission(id=0, insert=0, delete=0, update=0)
        only_update = Permission(id=1, insert=0, delete=0, update=1)
        only_delete = Permission(id=2, insert=0, delete=1, update=0)
        update_delete = Permission(id=3, insert=0, delete=1, update=1)
        only_insert = Permission(id=4, insert=1, delete=0, update=0)
        insert_update = Permission(id=5, insert=1, delete=0, update=1)
        insert_delete = Permission(id=6, insert=1, delete=1, update=0)
        all_permissions = Permission(id=7, insert=1, delete=1, update=1)

        visitor.permissions.append(no_permission)
        fan.permissions.append(only_insert)
        admin.permissions.append(all_permissions)

        jay.tracks.append(adorable_lady)
        jay.tracks.append(perfectionism)

        nickname = input("请输入管理员昵称：")
        password = input("请输入管理员密码：")
        administrator = User(nickname=nickname, rid=3)
        administrator.set_password(password)

        db.session.add_all([
            jay_chou, jay, visitor, fan, admin, no_permission, only_update,
            only_delete, update_delete, only_insert, insert_update,
            insert_delete, all_permissions, administrator
        ])
        db.session.commit()
        print("Initialized database.")