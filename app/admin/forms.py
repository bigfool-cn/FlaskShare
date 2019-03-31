from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo,Regexp
from flask import session
from app import create_app
from app.models import Admin,Role,Auth

app = create_app('default')
app.app_context().push()


class LoginForm(FlaskForm):
    """管理员登陆表单"""
    account = StringField(
        label="账号",
        validators=[DataRequired("请输入账号！")],
        description="账号",
        render_kw={
            "class ": "form-control",
            "placeholder":"请输入账号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入密码！")],
        description="密码",
        render_kw={
            "class ": "form-control",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class ": "btn btn-primary btn-block btn-flat",
        }
    )
    def validate_account(self,field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在")

class PwdForm(FlaskForm):
    """修改密码"""
    old_pwd = PasswordField(
        label="旧密码",
        validators=[DataRequired("请输入旧密码！")],
        description="旧密码",
        render_kw={
            "class ": "form-control",
            "id":"input_oldpwd",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[DataRequired("请输入新密码！"),EqualTo('new_pwd2',message='新密码不一致')],
        description="新密码",
        render_kw={
            "class ": "form-control",
            "id":"input_newpwd",
            "placeholder": "请输入新密码！",
        }
    )
    new_pwd2 = PasswordField(
        label="确认新密码",
        validators=[DataRequired()],
        description="确认新密码",
        render_kw={
            "class ": "form-control",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

    """验证旧密码"""
    def validate_old_pwd(self,filed):
        pwd = filed.data
        name = session["admin"]
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码输入错误")


class TagForm(FlaskForm):
    name = StringField(
        label="标签名称",
        validators = [DataRequired("请输入标签")],
        description = "标签名称",
        render_kw={
            "class":"form-control",
            "id":"input_name",
            "placeholder":"请输入标签名称！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )


class LinkForm(FlaskForm):
    name = StringField(
        label="链接类型",
        validators = [DataRequired("请输入链接类型")],
        description = "链接类型名称",
        render_kw={
            "class":"form-control",
            "id":"input_name",
            "placeholder":"请输入链接类型！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )


class AuthForm(FlaskForm):
    """添加权限"""
    name = StringField(
        label="权限名称",
        validators=[DataRequired("请输入权限名称")],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[DataRequired("请输入权限地址"),Regexp("/[a-z]+/|/[a-z]+/[a-z]+/[a-z]+/.*",message="权限地址格式错误")],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class RoleForm(FlaskForm):
    """添加角色"""
    name = StringField(
        label="角色名称",
        validators=[DataRequired("请输入角色名称")],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！"
        }
    )
    auths_list = Auth.query.all()
    auths = SelectMultipleField(
        label="操作权限",
        validators=[DataRequired("请选择权限列表")],
        description="操作权限",
        coerce=int,
        choices=[(a.id,a.name) for a in auths_list],
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请选择权限列表！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class AdminForm(FlaskForm):
    """管理员添加表单"""
    name = StringField(
        label="管理员名称",
        validators=[DataRequired("请输入管理员名称！")],
        description="管理员名称",
        render_kw={
            "class ": "form-control",
            "id":"input_name",
            "placeholder":"请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[DataRequired("请输入管理员密码！")],
        description="管理员密码",
        render_kw={
            "class ": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入密码！",
        }
    )
    re_pwd = PasswordField(
        label="管理员重复密码",
        validators=[DataRequired("请输入管理员密码！"),EqualTo("pwd",message="两次输入密码不一致")],
        description="管理员重复密码",
        render_kw={
            "class ": "form-control",
            "id": "input_re_pwd",
            "placeholder": "请再次输入管理员密码！"
        }
    )
    roles = Role.query.all()
    role_id = SelectField(
        label = "所属角色",
        validators=[DataRequired("请选择角色")],
        coerce=int,
        choices=[(r.id,r.name) for r in roles],
        render_kw={
            "class ": "form-control",
            "id": "input_role_id",
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )
