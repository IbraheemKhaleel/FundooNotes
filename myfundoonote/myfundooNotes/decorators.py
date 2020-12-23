import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework_jwt.settings import api_settings
from rest_framework import status


def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        
        if request.session:
            user = request.user
            if user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                response = {'success': False, 'message': 'Users credential not provided..!!'}
                return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'success': False, 'message': 'Users credential not provided..!!'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)

    return wrapper