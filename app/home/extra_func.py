from functools import wraps
import uuid
import datetime
import os

from flask import  redirect, url_for,session,request
from app.home import home

"""上下应用文处理器"""
@home.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data

"""登录验证装饰器"""
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get("user",False):
            return redirect(url_for('home.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_function

"""更改上传文件名"""
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]#取出后缀
    return filename