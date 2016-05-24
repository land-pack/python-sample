import os
from flask import Flask, current_app, render_template, redirect, flash, request, session, url_for
from flask.ext.mail import Mail, Message
from celery import Celery

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
MAIL_DEFAULT_SENDER = MAIL_USERNAME

# AMQP configure ..
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp'

# administrator list
ADMINS = ['app4landpack@sina.com', 'abc@sina.com']

# load configure from current file
app.config.from_object(__name__)

print app.config['MAIL_PASSWORD']

# Extend the flask ...
mail = Mail(app)
celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# This is the part of block !! so put it on the thread ...

@celery.task
def send_async_email(to, subject, body='', html=''):
    with app.app_context():
        msg = Message(subject=subject,
                      sender=MAIL_DEFAULT_SENDER,
                      recipients=['1063489610@qq.com', to])
        msg.body = body
        msg.html = html

        mail.send(msg)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # Send the email
    to = request.form['email']
    subject = 'Landpack Inc'
    body = request.form['body']
    html = render_template('sample.html')

    if request.form['submit'] == 'Send':
        # Send right away

        send_async_email.delay(to=to, subject=subject, body=body, html=html)
        # mail.send(msg)
        flash('Sending email to {0}'.format(email))
    else:
        # Send in one minute
        send_async_email.apply_async(args=[to, body], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
