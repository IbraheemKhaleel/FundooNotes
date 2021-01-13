from __future__ import absolute_import, unicode_literals

import logging
import os
import datetime

import pytz
from django.core.mail import EmailMessage
import threading
from celery import shared_task

from Notes.models import Note

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s | %(message)s')

file_handler = logging.FileHandler(os.path.abspath("loggers/tasks.log"))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class EmailThread(threading.Thread):
    """
    Created a class for email threading.
    """

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """
        this method gets called when the start() method is called
        """
        self.email.send()  # email is being sent


@shared_task
def send_email(data):
    """
    created a method to send email to respective user
    @param data: email body, subject and email of the reciever
    @type data: dict
    """
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()  # asking run() thread to execute


@shared_task
def check_reminder():
    """
    Reminds the user if any reminder set in their notes before an hour
    """
    print('something')
    current_time = datetime.datetime.now()
    print('something more')
    utc = pytz.UTC
    #print(utc)
    current_time = utc.localize(current_time)
    #print(current_times.tzinfo)
    #print(current_times)
    for note in Note.objects.filter(reminder__gt=current_time).exclude(reminder=None):
        #print('not in loop')
        difference = note.reminder - current_time
        seconds_in_day = 24 * 60 * 60
        minutes_remaining = (divmod(difference.days * seconds_in_day + difference.seconds, 60))
        if minutes_remaining[0] < 60:
            data = {'email_body': 'Hi!Reminder for ' + note.title + ' is scheduled within this hour.',
                    'to_email': 'ikhaleelem@gmail.com',
                    'email_subject': 'Reminder for your note'}
            send_email.delay(data)
            return 'done'  # sends reminder email to the user
        #return 'note not found'
    return 'not a reminder'