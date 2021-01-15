from __future__ import absolute_import, unicode_literals

import logging
import os
import datetime

from myfundooNotes.models import User
from myfundoonote.settings import MINUTES_TO_SECOND, HOUR_TO_MINUTE, SECONDS_IN_A_DAY
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
    current_time = datetime.datetime.now()
    utc = pytz.UTC
    current_time = utc.localize(current_time)
    logger.debug(current_time)
    for note in Note.objects.exclude(reminder=None).filter(reminder__gt=current_time): #Checking whether any reminder is present in any note objects
        user = User.objects.get(id=note.user_id)
        difference = note.reminder - current_time
        minutes_remaining = (divmod(difference.days * SECONDS_IN_A_DAY + difference.seconds, MINUTES_TO_SECOND))
        if minutes_remaining[0] < HOUR_TO_MINUTE:
            data = {'email_body': 'This is a reminder' + note.title + ' is scheduled in an hour.',
                    'to_email': user.email,
                    'email_subject': 'Reminder for your note'}
            send_email.delay(data)
            logger.debug('sent reminder for ' + note.title)
