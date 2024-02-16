from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, func

from typing import List
from typing_extensions import Annotated
import datetime


class Base(DeclarativeBase):

    def to_json(self):
        answer = self.__dict__.copy()
        del answer["_sa_instance_state"]
        return answer


idpk = Annotated[int, mapped_column(primary_key=True)]
create_time = Annotated[datetime.datetime,
                        mapped_column(server_default=func.current_timestamp() +
                                      datetime.timedelta(hours=8))]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app, model_class=Base)
#migrate = Migrate(app, db)
with app.app_context():
    db.engine.echo = True

# class User(db.Model):
#     id:Mapped[idpk]
#     username:Mapped[str]=mapped_column(unique=True)
#     create_time:Mapped[create_time]
#     email:Mapped[str]


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
        jay = Album(name="Jay", publish_time=datetime.date(2000, 11, 7),singer_id=1)
        adorable_lady = Track(name="可爱女人",
                              duration="03:59",
                              singer_id=1,
                              album_id=1)
        perfectionism = Track(name="完美主义",
                              duration="04:04",
                              singer_id=1,
                              album_id=1)
        jay.tracks.append(adorable_lady)
        jay.tracks.append(perfectionism)
        db.session.add_all([jay_chou, jay])
        db.session.commit()
        print("Initialized database.")


@app.get("/")
def main():
    return "hello"


if __name__ == "__main__":
    app.run()
