import os
import click
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from flask_wtf import FlaskForm
from wtforms import Form,TextAreaField,RadioField,BooleanField,SubmitField
from wtforms.validators import DataRequired

er=Flask(__name__)

@er.route('/')
def hi():
    return 'Hi Guys!'

er.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL','mysql+pymysql://root:12345@localhost:3306/Programmer')
er.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
er.secret_key='show me the money'

db=SQLAlchemy(er)
session=db.session

#Forms
class NewProgrammerForm(FlaskForm):
    name=TextAreaField('name',validators=[DataRequired('请输入名称！')])
    gender=RadioField('gender')
    age=TextAreaField('age')
    csharp=BooleanField('C#')
    java=BooleanField('Java')
    vb = BooleanField('VB')
    python = BooleanField('Python')
    c = BooleanField('c')
    comment=TextAreaField('Comment')
    submit=SubmitField('Save')

#Models
class Programmer(db.Model):
    id=Column(db.Integer,primary_key=True)
    name=Column(db.VARCHAR(20),index=True)
    gender=Column(db.CHAR)
    age=Column(db.Integer)
    csharp=Column(db.CHAR)
    java=Column(db.CHAR)
    vb=Column(db.CHAR)
    python=Column(db.CHAR)
    c=Column(db.CHAR)
    comment=Column(db.VARCHAR(255))

    #optional
    def __repr__(self):
        return '<Programmer %r>'% self.name

@er.route('/new',methods=['GET','POST'])
def new_programmer():
    form=NewProgrammerForm()
    if form.validate_on_submit():
        name=form.name.data
        gender=form.gender.data
        age = form.age.data
        csharp = form.csharp.data
        java = form.java.data
        vb = form.vb.data
        python = form.python.data
        c = form.c.data
        comment = form.comment.data
        programmer=Programmer(name=name,gender=gender,age=age,csharp=csharp,java=java,vb=vb,python=python,c=c,comment=comment)
        db.session.add(programmer)
        db.session.commit()
        flash('该程序员已添加。')

@er.cli.command()
def hello():
    click.echo('Hello,Programmer!')

if __name__=='__main__':
    er.run()



