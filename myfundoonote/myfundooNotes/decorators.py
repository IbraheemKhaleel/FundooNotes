"""
Author: Ibraheem Khaleel
Created :  23 December 2020

"""

from rest_framework import status
from django.http import HttpResponse
import json
from .models import User
import jwt
from services.cache import Cache
from services.encrypt import Encrypt
import logging


def user_login_required(view_func): 
    """
    Created a decorator methpd for giving access to user to carryo out CRUD operations in notes and labels

    """
    def wrapper(request, *args, **kwargs):
        result = {'message': 'some other issue please try after some time', 'status': False}
        try:
            token = request.META.get('HTTP_AUTHORIZATION') #recieving the token from authorization header 
            decoded_token = Encrypt.decode(token)
            cache = Cache() #decoding the stringified token for id
            if cache.get_cache("TOKEN_"+str(decoded_token['id'])+"_AUTH") is not None: #Checking whether the token exists in redis
                request.user = User.objects.get(id=decoded_token['id'])
                result['message'] = 'token verification successful'
                result['status'] = True
                logging.debug('{} status_code = {}'.format(result, status.HTTP_200_OK))
                return view_func(request, *args, **kwargs)
            result['message'] = "logged in user's token is not provided" #change message to you need to login first
            logging.debug('{} status_code = {}'.format(result, status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as e:
            result['message'] = 'Activation Expired'
            logging.exception('{} exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            result['message'] = 'Invalid Token'
            logging.exception('{}, exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['message'] = 'some other issue please try after some time'
            logging.exception('{}, exception = {}, status_code = {}'.format(result, str(e),  status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
    return wrapper
           