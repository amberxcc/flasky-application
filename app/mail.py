from flask import render_template, current_app
from . import mail
from flask_mail import Message
from threading import Thread


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)