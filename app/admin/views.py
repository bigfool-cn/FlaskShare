import datetime
import os

from app.admin import admin
from app import db
from flask import render_template,url_for,session,flash,redirect,request
from werkzeug.security import generate_password_hash
from app.admin.forms import LoginForm,PwdForm,AdminForm,RoleForm,AuthForm,TagForm,LinkForm
from app.models import User,UserLog,UserOpLog,Resource,ResourceCol,Role,Comment,Tag,Link,Auth,Admin,AdminOpLog,AdminLog
from app.admin.extra_func import admin_login_req,change_filename
from flask import current_app


@admin.route("/",methods=["GET"])
@admin_login_req
def index():
    """首页"""
    return render_template("admin/index.html")

@admin.route('/login/',methods=['GET','POST'])
def login():
    """登陆"""
    form = LoginForm(account=session.get("admin",None))
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!","err")
            return  redirect(url_for('admin.login'))
        session["admin"] = data["account"]
        session["role"] = Admin.query.join(Role).filter(admin.role_id==Role.id).first().role.name
        session["admin_id"] = admin.id
        #管理员登录日志
        adminlog = AdminLog(
            admin_id =  session["admin_id"],
            ip = request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('admin.index'))
    return render_template('admin/login.html',form=form)

@admin.route('/logout/')
@admin_login_req
def logout():
    """退出"""
    session.pop("admin",None)
    session.pop("admin_id",None)
    return redirect(url_for('admin.login'))

@admin.route('/tag/add/',methods=["GET","POST"])
@admin_login_req
def tag_add():
    """添加标签"""
    form= TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1:
            flash("标签名称已存在","err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data["name"])
        db.session.add(tag)
        db.session.commit()
        flash("标签添加成功","ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个标签：%s" %data["name"]
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html',form=form)

@admin.route('/tag/list/<int:page>/',methods=["GET"])
@admin_login_req
def tag_list(page=None):
    """标签列表"""
    if page is None:
        page = 1
    page_data = Tag.query.paginate(page=page,per_page=10)
    return render_template('admin/tag_list.html',page_data=page_data)

@admin.route('/tag/edit/<int:id>/',methods=["GET","POST"])
@admin_login_req
def tag_edit(id=None):
    """标签列修改"""
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1 and tag.name != data["name"]:
            flash("标签名称已存在", "err")
            return redirect(url_for('admin.tag_edit',id=id))
        tag.name=data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改标签了：%s→%s" %(tag.name,data["name"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for('admin.tag_edit',id=id))
    return render_template('admin/tag_edit.html', form=form,tag=tag)

@admin.route('/tag/del/<int:id>/',methods=["GET"])
@admin_login_req
def tag_del(id=None):
    """标签删除"""
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("标签删除成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个标签：%s" %tag.name
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.tag_list",page=1))

@admin.route('/link/add/',methods=["GET","POST"])
@admin_login_req
def link_add():
    """添加链接类型"""
    form= LinkForm()
    if form.validate_on_submit():
        data = form.data
        link_count = Link.query.filter_by(name=data["name"]).count()
        if link_count == 1:
            flash("链接类型名称已存在","err")
            return redirect(url_for('admin.link_add'))
        link = Link(name=data["name"])
        db.session.add(link)
        db.session.commit()
        flash("链接类型添加成功","ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个链接类型：%s" %data["name"]
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for('admin.link_add'))
    return render_template('admin/link_add.html',form=form)

@admin.route('/link/list/<int:page>/',methods=["GET"])
@admin_login_req
def link_list(page=None):
    """链接类型列表"""
    if page is None:
        page = 1
    page_data = Link.query.paginate(page=page,per_page=10)
    return render_template('admin/link_list.html',page_data=page_data)

@admin.route('/link/edit/<int:id>/',methods=["GET","POST"])
@admin_login_req
def link_edit(id=None):
    """链接类型列修改"""
    form = LinkForm()
    link = Link.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        link_count = Link.query.filter_by(name=data["name"]).count()
        if link_count == 1 and link.name != data["name"]:
            flash("链接类型已存在", "err")
            return redirect(url_for('admin.link_edit',id=id))
        link.name=data["name"]
        db.session.add(link)
        db.session.commit()
        flash("修改链接类型成功", "ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改链接类型了：%s→%s" %(link.name,data["name"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for('admin.link_edit',id=id))
    return render_template('admin/link_edit.html', form=form,link=link)

@admin.route('/link/del/<int:id>/',methods=["GET"])
@admin_login_req
def link_del(id=None):
    """链接类型删除"""
    link = Link.query.filter_by(id=id).first_or_404()
    db.session.delete(link)
    db.session.commit()
    flash("链接类型删除成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个链接类型：%s" %link.name
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.link_list",page=1))

@admin.route('/user/list/<int:page>',methods=["GET"])
@admin_login_req
def user_list(page=None):
    """会员列表"""
    if page is None:
        page = 1
    page_data = User.query.order_by(User.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/user_list.html',page_data=page_data)
    return render_template('admin/user_list.html')

@admin.route('/user/view/<int:id>',methods=["GET"])
@admin_login_req
def user_view(id=None):
    """查看会员"""
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html',user=user)

@admin.route('/user/del/<int:id>/',methods=["GET"])
@admin_login_req
def user_del(id=None):
    """删除会员"""
    user = User.query.get_or_404(id)
    # os.remove(current_app.config.get("UP_DIR")+"users/"+str(user.face))
    db.session.delete(user)
    db.session.commit()
    flash("会员删除成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个会员：%s" %user.name
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.user_list",page=1))

@admin.route('/user/freeze/<int:id>/',methods=["GET"])
@admin_login_req
def user_freeze(id=None):
    """冻结会员"""
    user = User.query.get_or_404(id)
    user.status = False
    db.session.add(user)
    db.session.commit()
    flash("会员冻结成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="冻结了一个会员：%s" %user.name
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.user_list",page=1))

@admin.route('/user/unfreeze/<int:id>/',methods=["GET"])
@admin_login_req
def user_unfreeze(id=None):
    """解冻会员"""
    user = User.query.get_or_404(id)
    user.status = True
    db.session.add(user)
    db.session.commit()
    flash("会员解冻成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="解冻了一个会员：%s" %user.name
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.user_list",page=1))

@admin.route('/adminoplog/list/<int:page>',methods=["GET"])
@admin_login_req
def adminoplog_list(page=None):
    """管理员操作日志列表"""
    if page is None:
        page = 1
    page_data = AdminOpLog.query.join(
        Admin
    ).filter(
        Admin.id == AdminOpLog.admin_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminoplog_list.html',page_data=page_data)

@admin.route('/adminloginlog/list/<int:page>',methods=["GET"])
@admin_login_req
def adminloginlog_list(page=None):
    """管理员登陆日志"""
    if page is None:
        page = 1
    page_data = AdminLog.query.join(
        Admin
    ).filter(
        Admin.id == AdminLog.admin_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminloginlog_list.html',page_data=page_data)

@admin.route('/pwd/',methods=["GET","post"])
@admin_login_req
def pwd():
    """修改密码"""
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        name = session["admin"]
        admin = Admin.query.filter_by(name=name).first()
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登陆！","ok")
        #记录操作日志
        adminoplog = AdminOpLog(
            admin_id = session["admin_id"],
            ip = request.remote_addr, #获取登陆ip,
            reason = "修改了密码"
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html',form=form)

@admin.route('/auth/add/',methods=["GET","POST"])
@admin_login_req
def auth_add():
    """添加权限"""
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name = data["name"],
            url = data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功","ok")
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了权限：%s→%s→%s" % (session["admin"],data["name"],data["url"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for("admin.auth_add"))
    return render_template('admin/auth_add.html',form=form)

@admin.route('/auth/list/<int:page>/',methods=["GET","POST"])
@admin_login_req
def auth_list(page=None):
    """权限列表"""
    if page is None:
        page = 1
    page_data = Auth.query.paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html',page_data=page_data)

@admin.route('/auth/edit/<int:id>',methods=["GET","POST"])
@admin_login_req
def auth_edit(id=None):
    """修改权限"""
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data["name"]).count()
        if auth_count == 1 and auth.name != data["name"]:
            flash("权限名称已存在", "err")
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data["name"]
        auth.url = data["url"]
        db.session.add(auth)
        db.session.commit()
        flash("修改权限成功","ok")
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了权限：%s→%s→%s：%s→%s" % (session["admin"],auth.name,auth.url,data["name"],data["url"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for("admin.auth_edit",id=id))
    return render_template('admin/auth_edit.html',form=form,auth=auth)

@admin.route('/auth/del/<int:id>/',methods=["GET"])
@admin_login_req
def auth_del(id=None):
    """权限删除"""
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("权限删除成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个权限：%s→%s" %(session["admin"],auth.name)
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.auth_list",page=1))

@admin.route('/role/add/',methods=["GET","POST"])
@admin_login_req
def role_add():
    """添加角色"""
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name = data["name"],
            auths = ",".join(map(lambda ah:str(ah),data["auths"]))#整形转字符串
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功","ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个角色：%s→%s" % (session["admin"], data["name"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for("admin.role_add"))
    return render_template('admin/role_add.html',form=form)

@admin.route('/role/list/<int:page>',methods=["GET"])
@admin_login_req
def role_list(page=None):
    """角色列表"""
    if page is None:
        page = 1
    page_data = Role.query.paginate(page=page, per_page=10)
    return render_template('admin/role_list.html',page_data=page_data)

@admin.route('/role/edit/<int:id>',methods=["GET","POST"])
@admin_login_req
def role_edit(id=None):
    """修改角色"""
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        form.auths.data = list(map(lambda ah:int(ah),role.auths.split(",")))#字符串转整形转列表
    if form.validate_on_submit():
        data = form.data
        role_count = Role.query.filter_by(name=data["name"]).count()
        if role_count == 1 and role.name != data["name"]:
            flash("角色名称已存在", "err")
            return redirect(url_for('admin.role_edit', id=id))
        role.name = data["name"]
        role.auths = ",".join(map(lambda ah:str(ah),data["auths"]))
        db.session.add(role)
        db.session.commit()
        flash("修改角色成功","ok")
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了角色：%s→%s：%s" % (session["admin"],role.name,data["name"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for("admin.role_edit",id=id))
    return render_template('admin/role_edit.html',form=form,role=role)

@admin.route('/role/del/<int:id>/',methods=["GET"])
@admin_login_req
def role_del(id=None):
    """删除角色"""
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("角色删除成功","ok")
    # 记录操作日志
    adminoplog = AdminOpLog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个角色：%s→%s" %(session["admin"],role.name)
    )
    db.session.add(adminoplog)
    db.session.commit()
    return redirect(url_for("admin.role_list",page=1))

@admin.route('/admin/add/',methods=["GET","POST"])
@admin_login_req
def admin_add():
    """添加管理员"""
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin_count = Admin.query.filter_by(name=data["name"]).count()
        if admin_count == 1:
            flash("管理员名称已存在", "err")
            return redirect(url_for('admin.admin_add'))
        admin = Admin(
            name = data["name"],
            pwd = generate_password_hash(data["pwd"]),
            is_super = 1,
            role_id = data["role_id"]
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功", "ok")
        # 记录操作日志
        adminoplog = AdminOpLog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个管理员：%s→%s" % (session["admin"], data["name"])
        )
        db.session.add(adminoplog)
        db.session.commit()
        return redirect(url_for("admin.admin_add"))
    return render_template('admin/admin_add.html',form=form)

@admin.route('/admin/list/<int:page>/',methods=["GET"])
@admin_login_req
def admin_list(page=None):
    """管理员列表"""
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html',page_data=page_data)

@admin.route('/userloginlog/list/<int:page>',methods=["GET"])
@admin_login_req
def userloginlog_list(page=None):
    """会员登录日志"""
    if page is None:
        page = 1
    page_data = UserLog.query.join(
        User
    ).filter(
        User.id == UserLog.user_id
    ).order_by(-UserLog.addtime).paginate(page=page, per_page=10)

    return render_template('admin/userloginlog_list.html',page_data=page_data)
