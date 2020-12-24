"""
Author: Ibraheem Khalee
Created on: Dec 20, 2020 
"""
from Label.models import Label
from myfundooNotes.models import User

def get_user(request):
    """[sets user email to associated user id and modifies request.data]
    Args:
        request ([QueryDict]): [post data]
    Raises:
        Account.DoesNotExist: [if given email isn't found in database]
    """
    request.POST._mutable = True
    user_email=request.data.get('user')
    user_qs = User.objects.filter(email=user_email)
    if not user_qs:
        raise User.DoesNotExist('No such account exists')
    if user_qs.exists() and user_qs.count() == 1:
        user_obj = user_qs.first()              #assign object from queryset 
        user_id=user_obj.id                     #assign id of object
    request.data["user"] = user_id
    request.POST._mutable = False


def get_collaborator_list(request):
    """[maps collaborator emails to their user ids and modifies request.data]

    Args:  
        request ([QueryDict]): [post data]
    """
    request.POST._mutable = True
    collaborators_list=[]                                           #holds ids associated to label names
    for collaborator_email in request.data.get('collaborators'):
        collab_qs = User.objects.filter(email=collaborator_email)
        if not collab_qs:
            raise User.DoesNotExist('No such user account exists')
        if collab_qs.exists() and collab_qs.count() == 1:
            collab_obj = collab_qs.first()                         #assign object from queryset 
            collaborators_list.append(collab_obj.id)               # append object id of the obtained object to list
    request.data["collaborators"] = collaborators_list
    request.POST._mutable = False

def get_label_list(request):
    """[maps label titles to their label ids and modifies request.data]

    Args:
        request ([QueryDict]): [post data]
    """ 
    request.POST._mutable = True
    label_list=[]                                           #holds ids associated to label names
    for label_name in request.data.get('labels'):
        label_qs = Label.objects.filter(name=label_name)
        if not label_qs:
            raise Label.DoesNotExist('No such label exists')
        if label_qs.exists() and label_qs.count() == 1:
            label_obj = label_qs.first()                         #assign object from queryset 
            label_list.append(label_obj.id)               # append object id of the obtained object to list
    request.data["labels"] = label_list
    request.POST._mutable = False
    
    