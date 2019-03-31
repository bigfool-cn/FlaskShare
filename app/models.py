#coding:utf8
from werkzeug.security import check_password_hash
from app import db
import datetime


# 关注
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


#会员模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True) #编号
    name = db.Column(db.String(100),unique=True)    #昵称
    pwd = db.Column(db.String(100)) #密码
    email = db.Column(db.String(100),unique=True)   #邮箱
    phone = db.Column(db.String(11),unique=True)    #手机号
    status = db.Column(db.Boolean,default=True) #账号状态,true为正常，false为冻结
    info = db.Column(db.Text)   #简介
    face = db.Column(db.String(255),unique=True)    #头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #注册时间
    uuid = db.Column(db.String(255),unique=True)    #唯一标识符
    userlogs = db.relationship('UserLog',backref='user') #会员日志外键关系关联
    comments = db.relationship('Comment',backref='user')    #评论外键关系关联
    resources = db.relationship('Resource', backref='user')  # 资源外键关系关联
    resourcecols = db.relationship('ResourceCol',backref='user')    #资源收藏外键关系关联
    followed = db.relationship('User',
       secondary=followers,
       primaryjoin=(followers.c.follower_id == id),
       secondaryjoin=(followers.c.followed_id == id),
       backref=db.backref('followers', lazy='dynamic'),
       lazy='dynamic')

    def __repr__(self):
        return "<User %s>"%self.name

    #验证密码
    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)
    #关注
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    #取消关注
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    #是否关注
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


#会员登陆日记模型
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer,primary_key=True) #编号
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))    #所属会员
    ip = db.Column(db.String(100)) #登陆ip
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #登陆时间

    def __repr__(self):
        return "<UserLog %s>"%self.id

# 会员操作日志
class UserOpLog(db.Model):
    __tablename__ = "useroplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登陆ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登陆时间

    def __repr__(self):
        return "<UserOpLog %s>" % self.id

#标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer,primary_key=True) #编号
    name = db.Column(db.String(100))    #标标签名
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间
    resources = db.relationship('Resource',backref='tag') #资源外键关联
    def __repr__(self):
        return "<Tag %s>"%self.name

# 链接类型
class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100))  # 类型名
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    resources = db.relationship('Resource', backref='link')  # 资源外键关联

    def __repr__(self):
        return "<Link %s>" % self.name

#评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)    #内容
    resource_id = db.Column(db.Integer,db.ForeignKey('resource.id'))  #所属电影
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))    #所属用户
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间

    def __repr__(self):
        return "<Comment %s>"%self.id

# 资源
class Resource(db.Model):
    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(500), unique=True)  # 下载链接
    img_url = db.Column(db.String(512)) #图片地址
    url_info = db.Column(db.String(15),default="")  #下载链接报错信息
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))  # 所属链接类型
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='resource')  # 评论外键关系关联
    resourcecols = db.relationship('ResourceCol', backref='resource')  # 资源收藏外键关系关联

    def __repr__(self):
        return "<Resource %s>" % self.title

#资源收藏
class ResourceCol(db.Model):
    __tablename__ = "resourcecol"
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))  # 所属资源
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  #添加时间

    def __repr__(self):
        return "<ResourceCol %s>" % self.id


#权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255)) #地址
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)#添加时间

    def __repr__(self):
        return "<Auth %s>" % self.name

# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限列表
    admins = db.relationship('Admin',backref='role')   #管理员关系关联
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Role %s>" % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)   #是否是超级管理员 0为是
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))    #所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    adminlogs = db.relationship('AdminLog',backref='admin') #管理员登陆日志关系关联
    adminoplogs = db.relationship('AdminOpLog',backref='admin')   #管理员操作日志关系关联

    def __repr__(self):
        return "<Admin %s>" % self.name

    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)


#管理员登陆日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登陆时间

    def __repr__(self):
        return "<AdminLog %s>" % self.id

#操作日志
class AdminOpLog(db.Model):
    __tablename__ = "adminoplog"
    id = db.Column(db.Integer,primary_key=True) #编号
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))    #所属管理员
    ip = db.Column(db.String(100)) #登陆ip
    reason = db.Column(db.String(600))  #操作原因
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #登陆时间

    def __repr__(self):
        return "<AdminOpLog %s>"%self.id