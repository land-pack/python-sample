import os
from threading import Thread
from flask import Flask, render_template
from flask.ext.mail import Mail, Message

# create a flask app
app = Flask(__name__)

# mail = Mail(app)

SECRET_KEY = 'development key'
# Email Server
MAIL_SERVER = 'smtp.sina.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# load configure from current file
app.config.from_object(__name__)
# administrator list
ADMINS = ['landpack@sina.com']

mail = Mail(app)


# This is the part of block !! so put it on the thread ...
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


# Create a helper function that sends an email.

def send_email(subject, sender, recipients, text_body, html_body):
    # with app.app_context():
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()


@app.route("/")
def index():
    # In the view , you auto have app context
    send_email("Hello Guys",
               ADMINS[0],
               ['1063489610@qq.com'],
               render_template('sample.txt'),
               render_template('sample.html'))
    print app.app_context()
    return '<h1>Okay!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
