"""
Author: Ibraheem Khaleel
Created on: 15th December 20
"""
import os
import logging
from django.db.models import Q
from django.utils.decorators import method_decorator
from myfundooNotes.decorators import user_login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import LabelSerializer
from .models import Label
from Notes import utils

# custom exceptions,test case ,put ,delete-delete existing from cache
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')

file_handler = logging.FileHandler(os.path.abspath("loggers/log_labels.log"))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@method_decorator(user_login_required, name='dispatch')
class ManageLabel(APIView):
    """[allows viewing labels for get and creates new label for post]
    Returns:
        [json]: [list of labels with complete details or creation confirmation and status code]
    """

    def get(self, request, **kwargs):
        """[displays specific label and all labels depends on user input]
        args: kwargs[userid]: user id of the user decoded from token
        Returns:
            Response: status , message and data
            @type: status: Boolean, message:str, data: list
        """
        try:
            current_user = kwargs['userid']

            if kwargs.get('pk'):
                label = Label.objects.get(Q(id=kwargs.get('pk')), Q(is_deleted=False),
                                          Q(user=current_user))
                serializer = LabelSerializer(label)

            else:
                labels = Label.objects.filter(Q(user=current_user)).exclude(is_deleted=True)
                serializer = LabelSerializer(labels, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log='retrieved labels', logger_obj=logger)
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result = utils.manage_response(status=False, message='Something label went wrong.Please try again.',
                                           log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)

    def post(self, request, **kwargs):
        """
        A method to post labels of the user
        @param request: name: name for the label
                        @type:str

        @param kwargs[userid]: user id of the user decoded from token
        @type kwargs[userid]: int

        @return: status, message and status code
        @rtype: status: boolean, message: str
        """
        try:
            utils.set_user(request, kwargs['userid'])
            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  # Return a 400 response if the data was invalid.
                serializer.save()
                result = utils.manage_response(status=True, message='created successfully', data=serializer.data,
                                               log='created new label', logger_obj=logger)
                return Response(result, status.HTTP_201_CREATED)
            else:

                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors,
                                               logger_obj=logger)
                return Response(result, status.HTTP_400_BAD_REQUEST)
        except Label.DoesNotExist as e:

            result = utils.manage_response(status=False, message='label not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message=str(e), log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        """[soft deletes existing label]
        Returns:
            [Response]: [confirmation message and status]
        """
        try:
            label = Label.objects.get(Q(id=pk), Q(is_deleted=False),
                                      Q(user=kwargs['userid']))

            label.soft_delete()
            result = utils.manage_response(status=True, message='label deleted successfully',
                                           log=('deleted label with id: {}'.format(pk)), logger_obj=logger)
            return Response(result, status.HTTP_204_NO_CONTENT)

        except Label.DoesNotExist as e:

            result = utils.manage_response(status=False, message='label not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:

            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, **kwargs):
        """
        A method to update labels
        @param request: name: name of label
                        @type:str

        @param kwargs[userid]: user id of the user decoded from token
        @type kwargs[userid]: int

        @return: status, message,data and status code
        @rtype: status: boolean, message: str, data:list
        """
        try:

            label = Label.objects.get(Q(id=pk), Q(is_deleted=False),
                                      Q(user=kwargs['userid']))

            serializer = LabelSerializer(label, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors,
                                               logger_obj=logger)
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result = utils.manage_response(status=True, message='updated successfully', data=serializer.data,
                                           log='updated label', logger_obj=logger)
            return Response(result, status.HTTP_200_OK)

        except Label.DoesNotExist as e:

            result = utils.manage_response(status=False, message='label not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:

            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


