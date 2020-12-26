import json
import jwt

from .models import User
from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework_jwt.settings import api_settings
from rest_framework import status


def user_login_required(view_func): 
    def wrapper(request, *args, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
            id = decoded_token['id']
            user = User.objects.get(id = id)
            if user and user.is_active:
                request.user = user
                return view_func(request, *args, **kwargs)   
            response = {'success': False, 'message': 'User must be logged in'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response = {'success': False, 'message': 'please provide a valid token'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)       
    return wrapper