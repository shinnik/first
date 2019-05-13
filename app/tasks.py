from flask_mail import Message
from app import celery, mail


@celery.task()
def plus(a, b):
    return a + b


@celery.task()
def send_mail():
    print('sending...')
    msg = Message(
        "Hello",
        recipients=["izrailev@phystech.edu"]
    )
    msg.html = "<h1><3</h1>"
    mail.send(msg)
    return None


celery.conf.beat_schedule = {
        'add-every-30-seconds': {
            'task': 'app.tasks.plus',
            'schedule': 30.0,
            'args': (16, 16)
        },
    }
celery.conf.timezone = 'UTC'