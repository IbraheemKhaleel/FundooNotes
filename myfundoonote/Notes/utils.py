"""
Author: Ibraheem Khaleel
Created on: Dec 20, 2020 
"""
import logging
import os

from labels.models import Label
from myfundooNotes.models import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s | %(message)s')

file_handler = logging.FileHandler(os.path.abspath("loggers/log_utils.log"))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def set_user(request, user_id):
    """[sets user email to associated user id and modifies request.data]
    Args:
        request ([QueryDict]): [post data]
    Raises:
        Account.DoesNotExist: [if given email isn't found in database]
    """
    request.POST._mutable = True

    request.data["user"] = user_id

    request.POST._mutable = False


def get_collaborator_list(request):
    """[maps collaborator emails to their user ids and modifies request.data]

    Args:  
        request ([QueryDict]): [post data]
    """
    request.POST._mutable = True
    collaborators_list = []  # holds ids associated to label names
    for collaborator_email in request.data.get('collaborators'):
        collab_qs = User.objects.filter(email=collaborator_email)
        if not collab_qs:
            raise User.DoesNotExist('No such user account exists')
        if collab_qs.exists() and collab_qs.count() == 1:
            collab_obj = collab_qs.first()  # assign object from queryset
            collaborators_list.append(collab_obj.id)  # append object id of the obtained object to list
    request.data["collaborators"] = collaborators_list
    request.POST._mutable = False


def get_label_list(request):
    """[maps label titles to their label ids and modifies request.data]

    Args:
        request ([QueryDict]): [post data]
    """
    request.POST._mutable = True
    label_list = []  # holds ids associated to label names
    for label_name in request.data.get('labels'):
        label_qs = Label.objects.filter(name=label_name)
        if not label_qs:
            raise Label.DoesNotExist('No such label exists')
        if label_qs.exists() and label_qs.count() == 1:
            label_obj = label_qs.first()  # assign object from queryset
            label_list.append(label_obj.id)  # append object id of the obtained object to list
    request.data["labels"] = label_list
    request.POST._mutable = False

def manage_response(**kwargs):
    """
    Created a method to provide response for the API
    @param kwargs: status: status of the request
                   @type:boolean
                   message: message for the user
                   @type:str
                   data: data provided by user, if it is successful
                   log: log message of the execution
                   @type:str
                   logger_obj: logger object object for the app
                   @type:object of logging.Logger
    @return:       status: status of the request
                   @type:boolean
                   message: message for the user
                   @type:str
                   data: data provided by user, if it is successful

    """
    result = {}
    result['status'] = kwargs['status']
    result['message'] = kwargs['message']

    if kwargs['status']:
        if 'data' in kwargs:
            result['data'] = kwargs['data']
        kwargs['logger_obj'].debug('validated data: {}'.format(kwargs['log']))
    else:
        kwargs['logger_obj'].error('error: {}'.format(kwargs['log']))
    return result

