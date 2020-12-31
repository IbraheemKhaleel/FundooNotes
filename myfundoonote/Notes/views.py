"""
Author: Ibraheem Khaleel
Created on: 15th December 2020 
"""

import logging

from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NoteSerializer

from .models import Note
from . import utils
from myfundooNotes.models import User
from myfundooNotes.decorators import user_login_required
from services.cache import Cache


# Create your views here.


class NotesOverview(APIView):
    """
    Created a class for displaying overview of urls using in operations

    """
    
    def get(self , request):
        """
        Created a method for displaying overview of urls 

        """
        api_urls = {    
            'Note-CreateAndRetrieve':'/note/',
            'Note-Update':'/note-update/<int:pk>/',
            'Label-CreateAndRetrieve': '/label/',
            'Label-UpdateAndDelete':'/label-update/<int:pk>/',
        }
        return Response(api_urls)
       
@method_decorator(user_login_required, name='dispatch')
class NotesView(APIView):
    """
    Created a class to creating and retrieving  notes saved inside
    """
    serializer_class = NoteSerializer
    
    def get(self , request, **kwargs):
        """
        Created a method to display list of notes saved in
        Returns:
        json: list of notes with complete notes
        """
        try:
            notes = Note.objects.filter(is_deleted=False) #accessing all the object notes into a variable
            serializer = NoteSerializer(notes, many=True) #serializing the variable using NoteSerializer
            result = utils.manage_response(status=True,message='retrieved successfully',data=serializer.data, log= serializer.data)
            #logger.debug('validated note list: {}'.format())
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            #logger.exception('Something went wrong')
            result = utils.manage_response(status=False,message='something wrong', log = str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)
        
    def post(self, request , **kwargs):
        """[creates new note]
        Returns:
            [Response]: [result data and status]
        """
        try:
            data = request.data
            utils.set_user(request,kwargs['userid'])
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):              
                serializer.save()
                result = utils.manage_response(status=True,message='created successfully',data=serializer.data,log=serializer.data)
                return Response(result,status.HTTP_201_CREATED)
            result = utils.manage_response(status=False,message=serializer.errors , log=serializer.errors)
            return Response(result,status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False,message='note not found',log=str(e))
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False,message=str(e),log=str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)

@method_decorator(user_login_required, name='dispatch')
class NoteView(APIView):
    """
    Created a class to update and delete a note
    
    """
    serializer_class = NoteSerializer
    def get_object(self , pk):
        """[fetches and returns specific note]
        Args:
            pk ([int]): [id]
        """
        try:
            return Note.objects.get(id = pk, is_deleted = False) 
        except Note.DoesNotExist as e:
            result=utils.manage_response(status=False,message='note not found',log=str(e))
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result=utils.manage_response(status=False,message='Something went wrong.Please try again.',log=str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk,**kwargs):
        """[displays specific note]
        Returns:
            [Response]: [note details]
        """
        try:
            note = self.get_object(pk)
            #print(note.user_id)
            if kwargs['userid'] == note.user_id:
                serializer = NoteSerializer(note)
                result=utils.manage_response(status=True,message='retrieved successfully',data=serializer.data,log=serializer.data)
                return Response(result , status.HTTP_200_OK)
            else:
                result=utils.manage_response(status=False,message='no such user for this note',log= 'bad request')
                return Response(result,status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result=utils.manage_response(status=False,message='Something went wrong.Please try again.',log=str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk,**kwargs):
        """[updates existing note]
        Returns:
            [Response]: [updated details and status]
        """
        try:
            note = self.get_object(pk)
            if kwargs['userid'] == note.user_id:
                data = request.data
                if data.get('collaborators'):
                    utils.get_collaborator_list(request)
                if data.get('labels'):
                    utils.get_label_list(request)
                serializer = NoteSerializer(note, data=request.data , partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                else:
                    result=utils.manage_response(status=False,message=serializer.errors,log= serializer.errors)
                    return Response(result,status.HTTP_400_BAD_REQUEST)
                result=utils.manage_response(status=True,message='updated successfully',data=serializer.data,log=serializer.data)
                return Response(result, status.HTTP_200_OK)
            else:
                result=utils.manage_response(status=False,message='no such user for this note',log= 'bad request')
                return Response(result,status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            result=utils.manage_response(status=False,message='note not found',log=str(e))
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result=utils.manage_response(status=False,message='Something went wrong.Please try again.',log=str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)
       
    def delete(self,request,pk,**kwargs):
        """[soft deletes existing note]
        Returns:
            [Response]: [confirmation message and status]
        """
        try:
            note = self.get_object(pk)
            if kwargs['userid'] == note.user_id:
                note.soft_delete()
                result=utils.manage_response(status=True,message='deleted successfully',log=('deleted note with id: {}'.format(pk)))
                return Response(result,status.HTTP_204_NO_CONTENT)
            else:
                result=utils.manage_response(status=False,message='no such user for this note',log= 'bad request')
                return Response(result,status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            result=utils.manage_response(status=False,message='note not found',log=str(e))
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result=utils.manage_response(status=False,message='Something went wrong.Please try again.',log=str(e))
            return Response(result,status.HTTP_400_BAD_REQUEST)

