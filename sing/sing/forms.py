from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

form_select_css = {
    "class":
    "block w-22 mt-1 rounded-md bg-gray-100 border-transparent focus:border-none focus:ring-transparent"
}
form_date_css = {
    "class":
    "mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
}


class LoginForm(FlaskForm):
    nickname = StringField("昵称", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField('登陆')


class SingerForm(FlaskForm):
    name = StringField("歌手名称", validators=[DataRequired()])
    birth = DateField("出生日期",
                      validators=[DataRequired()],
                      render_kw=form_date_css)
    submit = SubmitField('提交')


class TrackForm(FlaskForm):
    name = StringField("歌曲名称", validators=[DataRequired()])
    duration = StringField("时长", validators=[DataRequired()])
    singer_id = SelectField("歌手名称", render_kw=form_select_css)
    album_id = SelectField("专辑名称", render_kw=form_select_css)
    submit = SubmitField('提交')
