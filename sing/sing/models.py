from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, Table, Column
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
from typing import Generic, TypeVar, Annotated



T = TypeVar("T")
idpk = Annotated[int, mapped_column(primary_key=True)]
create_time = Annotated[datetime.datetime,
                        mapped_column(server_default=func.current_timestamp())]


class Base(DeclarativeBase, Generic[T]):

    def to_json(self):
        answer = self.__dict__.copy()
        del answer["_sa_instance_state"]
        for k, v in answer.items():
            if isinstance(v, datetime.date):
                answer[k] = str(v)
        return answer

    def insert(self, curr_user):
        if curr_user.role.permissions[0].id & 4 == 4:
            db.session.add(self)
            db.session.commit()
            return '添加成功'
        else:
            return PermissionError

    @staticmethod
    def update(curr_user):
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
        
db = SQLAlchemy(model_class=Base)


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


role_permission = Table("role_permission", Base.metadata,
                        Column("role_id", ForeignKey("role.id")),
                        Column("permission_id", ForeignKey("permission.id")))


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
