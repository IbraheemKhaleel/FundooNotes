"""
Author: Ibraheem Khaleel
Created :  23 December 2020

"""

from rest_framework import status
from django.http import HttpResponse
import json
import jwt
from services.cache import Cache
from services.encrypt import Encrypt
import logging


def user_login_required(view_func):
    """[gets token and fetches user id verifying active status.
    If everything is proper delegates to the requested view]

    Args:
        view_func ([request]): [the get,post etc view requested]
    """

    def wrapper(request, *args, **kwargs):
        result = {}
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = Encrypt.decode(token)
            cache = Cache()
            if cache.get_cache("TOKEN_" + str(decoded_token['id']) + "_AUTH") is not None:
                kwargs['userid'] = decoded_token['id']
                return view_func(request, *args, **kwargs)
            return HttpResponse('Unauthorized access is detected', status.HTTP_403_FORBIDDEN)
        except jwt.ExpiredSignatureError as e:
            result['message'] = 'Activation Expired'
            logging.exception('{} exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            result['message'] = 'Invalid Token'
            logging.exception(
                '{}, exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['message'] = 'some other issue please try after some time'
            logging.exception(
                '{}, exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
    return wrapper
