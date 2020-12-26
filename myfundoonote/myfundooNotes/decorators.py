"""
Author: Ibraheem Khaleel
Created :  23 December 2020

"""

import json
import jwt

from django.http import HttpResponse

from rest_framework import status

from .models import User


def user_login_required(view_func): 
    """
    Created a decorator methpd for giving access to user to carryo out CRUD operations in notes

    """
    def wrapper(request, *args, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION'] #recieving the token from authorization header 
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"]) #decoding the stringified token for id
            id = decoded_token['id'] #Obtaining the id from the decoded token
            user = User.objects.get(id = id) #matching with existing database id with the decoded id
            if user and user.is_active: #if the id exists and user is active, it can carry out CRUD operations in notes
                request.user = user
                return view_func(request, *args, **kwargs)   
            response = {'success': False, 'message': 'User must be logged in'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response = {'success': False, 'message': 'please provide a valid token'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)       
    return wrapper