from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from .. import db
from ..models import User
from ..mail import send_email
from .forms import LoginForm, RegistrationForm
from flask_login import current_user


# 登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 第一个参数：传入登陆成功的user对象用于管理，第二个参数选择是否会话是否持久（布尔值）
            login_user(user, form.remember_me.data)
            # 登陆前有没有访问需要授权的页面，若有则登陆后跳转回去
            next_page = request.args.get('next')
            # 登陆前没有访问需要授权的页面或不是相对地址时，跳回到首页
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


# 退出登录
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


# 注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# 确认邮箱
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))
    

# 返回未确认用户的页面
@auth.route('/unconfirmed')
def unconfirmed():
    # 匿名用户、已确认用户访问直接返回主页
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))

    # 已注册但未确认用户，返回提醒确认页面
    return render_template('auth/unconfirmed.html')


# 用于重发确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


# 注册到全局的钩子函数
@auth.before_app_request
def before_request():
    # 若每次请求的登录凭据有效，则更新最近上线时间
    if current_user.is_authenticated:
        current_user.ping()

    # 若每次请求的用户已登录、未确认、请求url不是auth域、不是请求静态文件：都重定向到待确认页面
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))