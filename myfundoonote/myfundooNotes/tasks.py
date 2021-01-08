from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
import threading
from celery import shared_task


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
    @type data: string
    """
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()  # asking run() thread to execute

