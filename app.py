from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user
#from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey, func, select
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, widgets
from wtforms.validators import DataRequired

from typing import List, TypeVar, Generic
from typing_extensions import Annotated
import datetime

T = TypeVar("T")


class Base(DeclarativeBase, Generic[T]):

    def to_json(self):
        answer = self.__dict__.copy()
        del answer["_sa_instance_state"]
        return answer

    def insert(self, curr_user):
        if curr_user.role.permissions[0].id & 4 == 4:
            db.session.add(self)
            db.session.commit()
            return '添加成功'
        else:
            return PermissionError

    def update(self, curr_user):
        if curr_user.role.permissions.id & 1 == 1:
            db.session.commit()
            return '修改成功'
        else:
            return PermissionError

    def delete(self, curr_user):
        if curr_user.role.permissions.id & 2 == 2:
            db.session.delete(self)
            db.session.commit()
            return '删除成功'
        else:
            return PermissionError


idpk = Annotated[int, mapped_column(primary_key=True)]
create_time = Annotated[datetime.datetime,
                        mapped_column(server_default=func.current_timestamp())]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = "show me the money"
db = SQLAlchemy(app, model_class=Base)
login_manager = LoginManager(app)
login_manager.login_view = "main"

#migrate = Migrate(app, db)
with app.app_context():
    db.engine.echo = True


class Singer(db.Model):
    id: Mapped[idpk]
    name: Mapped[str] = mapped_column(unique=True)
    birth: Mapped[datetime.date]
    albums = relationship("Album")


class Album(db.Model):
    id: Mapped[idpk]
    name: Mapped[str]
    publish_time: Mapped[datetime.date]
    singer_id: Mapped[int] = mapped_column(ForeignKey("singer.id"))
    tracks = relationship("Track",
                          back_populates="album",
                          cascade="save-update,merge,delete")


class Track(db.Model):
    id: Mapped[idpk]
    name: Mapped[str]
    duration: Mapped[str]
    singer_id: Mapped[int] = mapped_column(ForeignKey("singer.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"))
    album = relationship("Album", back_populates="tracks")
    singer = relationship("Singer")


class TrackForm(FlaskForm):
    name = StringField("歌曲名称", validators=[DataRequired()])
    duration = StringField("时长", validators=[DataRequired()])
    singer_id = SelectField("歌手名称", validate_choice=False)
    album_id = SelectField("专辑名称")
    submit = SubmitField('提交')


role_permission = Table("role_permission", Base.metadata,
                        Column("role_id", ForeignKey("role.id")),
                        Column("permission_id", ForeignKey("permission.id")))


class User(db.Model, UserMixin):
    id: Mapped[idpk]
    nickname: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    create_time: Mapped[create_time]
    rid: Mapped[int] = mapped_column(ForeignKey("role.id"), default=0)
    role = relationship("Role")

    def set_password(self, pwd_txt):
        self.password = generate_password_hash(pwd_txt)

    def check_password(self, curr_pwd):
        return check_password_hash(self.password, curr_pwd)


class LoginForm(FlaskForm):
    nickname = StringField("昵称", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField('登陆')


@login_manager.user_loader
def load_user(id) -> User:
    return User(id=id)


class Role(db.Model):
    id: Mapped[idpk]
    name: Mapped[str]
    permissions = relationship("Permission",
                               secondary=role_permission,
                               back_populates="roles")


class Permission(db.Model):
    id: Mapped[idpk]
    insert: Mapped[int]
    delete: Mapped[int]
    update: Mapped[int]
    roles = relationship("Role",
                         secondary=role_permission,
                         back_populates="permissions")


def insert_delete_update(curr_user: User, obj: Generic[T]):
    k_v = obj.to_json()
    generic = Generic[T]()
    if curr_user.role.permissions.id & 4 == 4:
        for k, v in k_v.items():
            generic.k = v
        db.session.add(generic)
        db.session.commit()
        return "添加成功"
    elif curr_user.role.permissions.id & 2 == 2:
        db.session.delete(generic)
        db.session.commit()
        return "删除成功"
    elif curr_user.role.permissions.id & 1 == 1:
        for k, v in k_v.items():
            generic.k = v
            db.session.commit()
        return "修改成功"
    else:
        return PermissionError


@app.cli.command()
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Recreated database.")


@app.cli.command()
def init_db():
    with app.app_context():
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


@app.route("/", methods=["GET", "POST"])
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


@login_required
@app.get("/authorize")
def authenticate():
    if current_user.is_authenticated:
        user = db.session.get(User, current_user.id)
        return user.role.name
    else:
        return redirect(url_for("main"))


def turn_row_into_tuple(obj: list):
    return [tuple(x) for x in obj]


@login_required
@app.route("/track/insert", methods=["GET", "POST"])
def insert():
    if request.method == "GET":
        track_form = TrackForm()
        track_form.singer_id.choices = turn_row_into_tuple(
            db.session.execute(select(Singer.id, Singer.name)).all())
        track_form.album_id.choices = turn_row_into_tuple(
            db.session.execute(select(Album.id, Album.name)).all())
        return render_template('insert.html', form=track_form)
    if request.method == "POST":
        user = db.session.get(User, current_user.id)
        track = Track(name=request.form['name'],
                      duration=request.form['duration'],
                      singer_id=request.form['singer_id'],
                      album_id=request.form['album_id'])
        result=track.insert(user)
        if not isinstance(result, OSError):
            return request.form['name'] + result
        else:
            return result


if __name__ == "__main__":
    app.run()
