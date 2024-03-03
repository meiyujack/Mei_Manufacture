from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired


def generate_css(type,*new_css_value:list):
    form_base_text=["rounded-md","mt-1","bg-gray-100","border-transparent","focus:border-gray-500","focus:bg-white","focus:ring-0"]
    base={"text":form_base_text,"submit":form_submit_css}
    result=""
    if new_css_value:
        base[type].extend(new_css_value)
        result=" ".join(base[type])
    else:
        result=" ".join(base[type])

    return {"class":result}

form_select_css = {
    "class":
    "block w-22 mt-1 rounded-md bg-gray-100 border-transparent focus:border-none focus:ring-transparent"
}
form_date_css = {
    "class":
    "mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
}
form_submit_css={
    "class":"border border-black p-1 rounded-md hover:bg-blue-900 rounded-md hover:text-white transition duration-300"
}
form_checkbox_css={
    "class":"rounded bg-gray-200 border-transparent focus:border-transparent focus:bg-gray-200 text-gray-500 focus:ring-0 focus:ring-offset-0"
}

class LoginForm(FlaskForm):
    nickname = StringField("昵称", validators=[DataRequired()],render_kw=generate_css("text","block","w-full"))
    password = PasswordField("密码", validators=[DataRequired()],render_kw=generate_css("text","block","w-full"))
    remember = BooleanField("记住我",render_kw=form_checkbox_css)
    submit = SubmitField('登陆',render_kw=form_submit_css)


class SingerForm(FlaskForm):
    name = StringField("歌手名称", validators=[DataRequired()])
    birth = DateField("出生日期",
                      validators=[DataRequired()],
                      render_kw=form_date_css)
    submit = SubmitField('提交')


class TrackForm(FlaskForm):
    name = StringField("歌曲名称", validators=[DataRequired()],render_kw=generate_css("text",""))
    duration = StringField("时长", validators=[DataRequired()],render_kw=generate_css("text","w-12"))
    singer_id = SelectField("歌手名称", render_kw=form_select_css)
    album_id = SelectField("专辑名称", render_kw=form_select_css)
    submit = SubmitField('提交',render_kw=form_submit_css)
