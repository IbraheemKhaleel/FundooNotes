"""
Author: Ibraheem Khaleel
Created :  25 November 2020

"""

import os, jwt, logging

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from .tasks import send_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views

from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, LoginSerializer
from services.exceptions import EmptyFieldError, ValidationError
from Notes import utils
from services.cache import Cache
from services.encrypt import Encrypt
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s | %(message)s')

file_handler = logging.FileHandler(os.path.abspath("loggers/myfundooNotes.log"))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


# defining a general error message if any unknown errors occur
default_error_message = {'error': 'Something went wrong', 'status': False}


class Login(generics.GenericAPIView):
    """[allows user login after verification and activation]

    Returns:
        [Response]: [username , email and status code]
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """[validates user email and password, sets user id in cache]
        Returns:
            [dictionary]: [token]
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.data['email'])
            token = Encrypt.encode(user.id)
            cache = Cache()
            cache.set_cache("TOKEN_" + str(user.id) + "_AUTH", token)
            result = utils.manage_response(status=True, message='Token generated', data=token, log=serializer.data,
                                           logger_obj=logger)
            return Response(result, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            result = utils.manage_response(status=False, message='Account does not exist', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            result = utils.manage_response(status=False, message='Please enter a valid token', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='some other issue.Please try again', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


class Registration(generics.GenericAPIView):
    """
    A Registration class for registration of users with right information
        
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Defined post method which register users with valid email and oher inputs.
        It checks the authenticity of the email by sending a token to the respective email

       Returns: The serialized user details in JSON format
        """
        try:
            user = request.data
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = 'Hi ' + user.user_name + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            send_email.delay(data)
            result = utils.manage_response(status=True, message='An email has been sent for verification',
                                           data=serializer.data, log='User registration request has been recieved',
                                           logger_obj=logger)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            result = utils.manage_response(status=False, message='Please enter proper details for each field',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except EmptyFieldError as e:
            result = utils.manage_response(status=False, message='Please dont leave the field empty', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(default_error_message, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(views.APIView):
    """
    Created class to verify the user email which used for verification

    """
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        """
        Created method for verifying email and successfully registering the user
        Returns:
           response message with status code
        """
        token = request.GET.get('token')  # retrieving query params token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            result = utils.manage_response(status=True, message='Email has been successfully activated',
                                           data=user.email, log='Email verification has been sucessful',
                                           logger_obj=logger)
            return Response(result, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logging.exception('Exception due to expired signature')
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logging.exception('Exception due to error in decoding')
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception('Exception due to other reasons')
            return Response(default_error_message, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestToEmail(generics.GenericAPIView):
    """
    Created class for sending request to email for password reset 
    """

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        """
        Created method to send base64 encoded token along with user details to email
            for password reset

        Returns:
            Response message along with status code
        """
        email = request.data.get('email', '')
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                redirect_url = request.data.get('redirect_url', '')
                absurl = 'http://' + current_site + relativeLink
                email_body = 'Hello, \n Use link below to reset your password  \n' + absurl + "?redirect_url=" + redirect_url
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your passsword'}
                send_email.delay(data)
            result = utils.manage_response(status=True, message='A reset password link has been sent successfully',
                                           data=user.email, log='Password reset link has been sent ', logger_obj=logger)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            result = utils.manage_response(status=False, message='Please enter proper details for each field',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except EmptyFieldError as e:
            result = utils.manage_response(status=False, message='Please dont leave the field empty', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """
    Created class for generating  token for successful reset of password

    """
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        """
        Method for generating base64 encoded token

        Args:
            request : It is the rerquest given by user to reset passsword
            uidb64 : user id encoded in base64
            token ([type]): the generated token for password reset

        Returns:
            Redirect to url to change the password
        """
        redirect_url = request.GET.get('redirect_url')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    logging.debug('Token validated')
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')
        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    logging.exception('Exception due to invalid token')
                    return CustomRedirect(redirect_url + '?token_valid=False')
            except UnboundLocalError as e:
                logging.exception('Exception due to variable being referenced before assignment')
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                logging.exception('Exception due to other reasons')
                return Response(default_error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception('Exception due to other reasons')
            return Response(default_error_message, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """
    Created class to set new password the respective user

    """
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """
        Created a method to set a new password for existing user

        Args:
            request : The request given by user to set the new password

        Returns:
            Response message with status code
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = utils.manage_response(status=True, message='Password reset successfully', data=serializer.data,
                                           log='Password reset has been done ', logger_obj=logger)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            result = utils.manage_response(status=False, message='Please enter proper details for each field',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except EmptyFieldError as e:
            result = utils.manage_response(status=False, message='Please dont leave the field empty', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong. Please try again later',
                                           log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
