import uuid
import os
import stat
import datetime

from app.home import home
from app import db
from flask import url_for, render_template, redirect, session, request, flash, current_app,make_response
from app.home.forms import LoginForm,RegistForm,UserBaseForm,PwdForm,ReleaseForm
from app.models import User,UserLog,Resource,followers,Tag
from app.home.extra_func import user_login_req,change_filename
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

@home.route('/')
@home.route('/<int:page>',methods=["GET","POST"])
@user_login_req
def index(page=None):
    form = ReleaseForm()
    category = request.values.get("category", "")
    if page is None:
        page = 1
    if category:
        page_data = Resource.query.filter_by(tag_id=int(category)).order_by(-Resource.addtime).paginate(page=page,per_page=10)
    else:
        page_data = Resource.query.order_by(-Resource.addtime).paginate(page=page,per_page=10)
    follower = {}
    user_id = session.get("user_id",0)
    for resource in page_data.items:
        #关注者
        user = User.query.get(user_id)
        #被关注者
        be_user = User.query.get(int(resource.user_id))
        if not user.is_following(be_user):
            follower[resource.user_id] = True
        else:
            follower[resource.user_id] = False
    if form.validate_on_submit():
        data = form.data
        content = data["content"]
        rs_type = data["rs_type"]
        url_type = data["url_type"]
        url = data["download_url"]
        # 如果目录不存在，则创建并给与全部权限
        time_file = datetime.datetime.now().strftime("%Y-%m") + "/"
        rs_file = current_app.config.get("UP_DIR") + "resources/" + time_file
        if not os.path.exists(rs_file):
            os.mkdir(rs_file)
            os.chmod(rs_file, stat.S_IRWXU)
        img_url_all = ""    #组装图片链接地址
        if form.data["img_url_1"]:
            img_1 = form.img_url_1.data.filename
            if img_1 != "":
                #更改上传文件名
                img_1 = change_filename(secure_filename(img_1))
                img_url_all = img_url_all + time_file + img_1
                # 保存图片
                form.img_url_1.data.save(rs_file + img_1)
        if form.data["img_url_2"]:
            img_2 = form.img_url_2.data.filename
            if img_2 != "":
                # 更改上传文件名
                img_2 = change_filename(secure_filename(img_2))
                img_url_all = img_url_all + "," + time_file+ img_2
                # 保存图片
                form.img_url_2.data.save(rs_file + img_2)
        if form.data["img_url_3"]:
            img_3 = form.img_url_3.data.filename
            if img_3 != "":
                # 更改上传文件名
                img_3 = change_filename(secure_filename(img_3))
                img_url_all = img_url_all + "," + time_file + img_3
                # 保存图片
                form.img_url_3.data.save(rs_file + img_3)
        if form.data["img_url_4"]:
            img_4 = form.img_url_4.data.filename
            if img_4 != "":
                # 更改上传文件名
                img_4 = change_filename(secure_filename(img_4))
                img_url_all = img_url_all + "," + time_file + img_4
                # 保存图片
                form.img_url_4.data.save(rs_file + img_4)
        resource = Resource(title=content,url=url,tag_id=rs_type,user_id=session['user_id'],link_id=url_type,img_url=img_url_all)
        db.session.add(resource)
        db.session.commit()
        flash("发布成功!","ok")
        return redirect(url_for('home.index'))
    print(form.errors)
    return render_template('home/index.html', form=form,page_data=page_data,follower=follower,category=category)

@home.route('/login/',methods=["GET","POST"])
def login():
    """会员登陆"""
    form = LoginForm(name=session.get("user", None))
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误!", "err")
            return redirect(url_for('home.login'))
        session["user"] = data["name"]
        session["user_id"] = user.id
        # 会员员登录日志
        userlog = UserLog(
            user_id=session["user_id"],
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.index',page=1))
    return render_template("home/login.html",form=form)

@home.route('/logout/')
@user_login_req
def logout():
    """会员注销"""
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for('home.login'))

@home.route('/register/',methods=["GET","POST"])
def register():
    """会员注册"""
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data["name"],
            email = data["email"],
            phone = data["phone"],
            pwd = generate_password_hash(data["pwd"]),
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！","ok")
        return redirect(url_for("home.login"))
    return render_template('home/register.html',form=form)

@home.route('/user/',methods=['POST','GET'])
@user_login_req
def user():
    """用户基本信息"""
    form = UserBaseForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        face_url = secure_filename(form.face.data.filename)
        # 如果目录不存在，则创建并给与全部权限
        if not os.path.exists(current_app.config.get("UP_DIR")):
            os.mkdir(current_app.config.get("UP_DIR"))
            os.chmod(current_app.config.get("UP_DIR"), stat.S_IRWXU)
        face = change_filename(face_url)
        form.face.data.save(current_app.config.get("UP_DIR") + str("users/") + face)
        name_count = User.query.filter_by(name=data["name"])
        if name_count == 1:
            flash("昵称已经存在！", "err")
            return redirect(url_for('home.user'))
        user.name = data["name"]
        email_count = User.query.filter_by(email=data["email"])
        if email_count == 1:
            flash("邮箱已经存在！", "err")
            return redirect(url_for('home.user'))
        user.email = data["email"]
        phone_count = User.query.filter_by(phone=data["phone"])
        if phone_count == 1:
            flash("手机号码已经存在！", "err")
            return redirect(url_for('home.user'))
        user.phone = data["phone"]
        user.face = face,
        user.info = data["info"],
        db.session.add(user)
        db.session.commit()
        flash("修改成功！", "ok")
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)
    return render_template('home/user.html')

@home.route('/pwd/',methods=["GET","POST"])
@user_login_req
def pwd():
    """修改密码"""
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.get(int(session["user_id"]))
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误！","err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["pwd"])
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功！","ok")
        return redirect(url_for('home.login'))
    return render_template('home/pwd.html',form=form)

@home.route('/focus_user/',methods=['POST','GET'])
@user_login_req
def focus_user():
    """个人中心关注会员"""
    users = User.query.join(
        followers, (followers.c.followed_id == User.id)
    ).filter(
        followers.c.follower_id == session["user_id"]
    ).all()
    return render_template('home/focus_user.html',users=users)

@home.route('/my_resources/<int:page>/',methods=['POST','GET'])
@user_login_req
def my_resources(page=None):
    """我的资源"""
    category = request.values.get("category", "")
    if page is None:
        page = 1
    if category:
        page_data = Resource.query.filter_by(tag_id=int(category)).filter(
            Resource.user_id == session['user_id']
        ).order_by(-Resource.addtime).paginate(page=page,per_page=10)
    else:
        page_data = Resource.query.filter(Resource.user_id==session['user_id']).order_by(-Resource.addtime).paginate(page=page,per_page=10)
    return render_template('home/my_resources.html',page_data=page_data,category=category)

@home.route('/my_resources/edit/',methods=['POST','GET'])
@user_login_req
def my_resources_edit():
    """我的资源修改"""
    if request.method == "POST":
        id = request.values.get("rs-id",0)
        title = request.values.get("title","")
        rs_type = request.values.get("rs-type", 0)
        url_type = request.values.get("url-type", 0)
        download_url = request.values.get("download-url",0)
        img_url_1 = request.files['img_url_1']
        img_url_2 = request.files['img_url_2']
        img_url_3 = request.files['img_url_3']
        img_url_4 = request.files['img_url_4']
        resource = Resource.query.get(int(id))
        resource.title = title
        resource.tag_id = rs_type
        resource.link_id = url_type
        resource.url = download_url
        img_url_all = resource.img_url
        #全为空则不对图片操作
        if not (img_url_1 or img_url_2 or img_url_3 or img_url_4):
            print("all kong")
        else:
            # 如果目录不存在，则创建并给与全部权限
            time_file = datetime.datetime.now().strftime("%Y-%m") + "/"
            rs_file = current_app.config.get("UP_DIR") + "resources/" + time_file
            print(rs_file)
            if not os.path.exists(rs_file):
                os.mkdir(rs_file)
                os.chmod(rs_file, stat.S_IRWXU)
            img_url = resource.img_url.split(",")
            if img_url[0] is not "":
                url_count = len(img_url)
            else:
                url_count = 0
            #如果图片已有
            if url_count:
                if url_count == 1:
                    if img_url_1:
                        # 更改上传文件名
                        img_1 = change_filename(secure_filename(img_url_1.filename))
                        img_url[0] = time_file + img_1
                        img_url_1.save(rs_file+img_1)
                    else:
                        if img_url_2 and url_count != 2:
                            #图片追加
                            img_2 = change_filename(secure_filename(img_url_2.filename))
                            img_url.append(time_file + img_2)
                            img_url_2.save(rs_file + img_2)
                if url_count == 2:
                    if img_url_2:
                        img_2 = change_filename(secure_filename(img_url_2.filename))
                        img_url[1] = time_file + img_2
                        img_url_2.save(rs_file+img_2)
                    else:
                        if img_url_3 and url_count != 3:
                            #图片追加
                            img_3 = change_filename(secure_filename(img_url_3.filename))
                            img_url.append(time_file + img_3)
                            img_url_3.save(rs_file + img_3)
                if url_count == 3:
                    if img_url_3:
                        img_3 = change_filename(secure_filename(img_url_3.filename))
                        img_url[2] = time_file + img_3
                        img_url_3.save(rs_file+img_3)
                    else:
                        if img_url_4 and url_count != 4:
                            # 图片追加
                            img_4 = change_filename(secure_filename(img_url_4.filename))
                            img_url.append(time_file + img_3)
                            img_url_4.save(rs_file + img_4)
                if url_count == 4:
                    if img_url_4:
                        img_4 = change_filename(secure_filename(img_url_4.filename))
                        img_url[3] = time_file + img_4
                        img_url_4.save(rs_file+img_4)
                img_url_all_new = ""
                i = 0
                for img in img_url:
                    if i == 0:
                        img_url_all_new = img
                    else:
                        img_url_all_new += "," + img
                    i += 1
                resource.img_url = img_url_all_new
            else:
                if img_url_1:
                    img_1 = change_filename(secure_filename(img_url_1.filename))
                    img_url_all += (time_file + img_1)
                    img_url_1.save(rs_file + img_1)
                if img_url_2:
                    img_2 = change_filename(secure_filename(img_url_2.filename))
                    img_url_all += "," + (time_file + img_2)
                    img_url_2.save(rs_file + img_2)
                if img_url_4:
                    img_3 = change_filename(secure_filename(img_url_3.filename))
                    img_url_all += "," + (time_file + img_3)
                    img_url_3.save(rs_file + img_3)
                if img_url_4:
                    img_4 = change_filename(secure_filename(img_url_4.filename))
                    img_url_all += "," + (time_file + img_4)
                    img_url_4.save(rs_file + img_4)
                resource.img_url = img_url_all
        db.session.add(resource)
        db.session.commit()
        flash("修改成功","ok")
        resource = Resource.query.get(int(id))
        img_url = resource.img_url.split(",")
        if img_url[0] is not "":
            url_count = len(img_url)
        else:
            url_count = 0
        return render_template("home/my_resources_edit.html", resource=resource, img_url=img_url, url_count=url_count)
    id = request.values.get("id", 0)
    resource = Resource.query.get(int(id))
    img_url = resource.img_url.split(",")
    if img_url[0] is not "":
        url_count = len(img_url)
    else:
        url_count = 0
    return render_template("home/my_resources_edit.html",resource=resource,img_url=img_url,url_count=url_count)

@home.route('/to_attention/',methods=["POST"])
@user_login_req
def to_attention():
    """关注"""
    be_user_id = request.values.get("be_user_id","")
    be_user = User.query.get(int(be_user_id))
    user = User.query.get(int(session["user_id"]))
    user.follow(be_user)
    return make_response("关注成功")

@home.route('/my_focus/',methods=["GET","POST"])
@user_login_req
def my_focus():
    """我的关注"""
    category = request.values.get("category","")
    if category:
        resources = Resource.query.filter_by(tag_id=int(category)).join(
            followers,(followers.c.followed_id == Resource.user_id)
        ).filter(
            followers.c.follower_id == session["user_id"]
        ).order_by(-Resource.addtime)
    else:
        resources = Resource.query.join(
            followers,(followers.c.followed_id == Resource.user_id)
        ).filter(
            followers.c.follower_id == session["user_id"]
        ).order_by(-Resource.addtime)
    return render_template('home/my_focus.html',resources=resources,category=category)

@home.route('/un_attention/',methods=["POST"])
@user_login_req
def un_attention():
    """取消关注"""
    be_user_id = request.values.get("be_user_id", "")
    be_user = User.query.get(int(be_user_id))
    user = User.query.get(int(session["user_id"]))
    user.unfollow(be_user)
    return make_response("取消关注成功")

@home.route('/post_error/',methods=["POST"])
@user_login_req
def post_error():
    """链接报错信息"""
    url_info = request.values.get("url_info", "")
    if not url_info:
        return make_response("提交失败！请选择合适的报错信息")
    rs_id = request.values.get("rs_id", "")
    resource = Resource.query.get(int(rs_id))
    resource.url_info = url_info
    db.session.add(resource)
    db.session.commit()
    return make_response("提交成功")