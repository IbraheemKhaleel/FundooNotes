"""
Author: Ibraheem Khaleel
Created on: 15th December 20 
"""

import logging

from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NoteSerializer

from .models import Note
from . import utils
from myfundooNotes.decorators import user_login_required


# Create your views here.


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s | %(message)s')

file_handler = logging.FileHandler('log_notes.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
    
    def get(self , request):
        """
        Created a method to display list of notes saved in
        Returns:
        json: list of notes with complete notes
        """
        try:
            notes = Note.objects.filter(is_deleted=False) #accessing all the object notes into a variable
            serializer = NoteSerializer(notes, many=True) #serializing the variable using NoteSerializer
            result = utils.manage_response(status=True,message='retrieved successfully',data=serializer.data)
            logger.debug('validated note list: {}'.format(serializer.data))
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Something went wrong')
            result = utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)
        
    
    def post(self, request):
        """
        Created a method to create a new note
        Returns:
        json: new note's saved notes
        """
        
        
        try:
            notes_data = request.data
            if notes_data.get('user'):
                utils.get_user(request)
            if notes_data.get('collaborators'):
                utils.get_collaborator_list(request)
            if notes_data.get('labels'):
                utils.get_label_list(request)
            serializer = NoteSerializer(data=request.data) #serializing the input notes given by user
            if serializer.is_valid(): #Checks whether the given notes are valid or not using in built is_valid function
                result = utils.manage_response(status=True,message='created successfully',data=serializer.data)
                logger.debug('validated new note details: {}'.format(serializer.data))
                return Response(result,status.HTTP_201_CREATED)
            else:
                logger.error('Invalid note details entered')
                result = utils.manage_response(status=False,message=serializer.errors)
                return Response(result,status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            logger.exception('Requested note does not exist')
            result = utils.manage_response(status=False,message='note not found')
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Something went wrong')
            result = utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)

@method_decorator(user_login_required, name='dispatch')
class NoteView(APIView):
    """
    Created a class to update and delete a note
    
    """
    serializer_class = NoteSerializer
    def get_object(self, pk):
        """
        Created a method to retrieve an object notes

        parameter:  primary key given to retrieve notes of particular user

        return: user notes of particular user
        """
        try:
            return Note.objects.get(id = pk, is_deleted = False) #calls get method to retrieve a particular user notes
        except Note.DoesNotExist:
            logger.exception('Requested note does not exist')
            result=utils.manage_response(status=False,message='note not found')
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Something went wrong')
            result=utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)
            

    def get(self, request, pk):
        
        
        try:
            notes = self.get_object(pk=pk)
            serializer = NoteSerializer(notes)
            result=utils.manage_response(status=True,message='retrieved successfully',data=serializer.data)
            logger.debug('validated note detail: {}'.format(serializer.data))
            return Response(result , status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Something went wrong')
            result=utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Created a put method to edit particular user notes
        Args:
            pk (integer): id of particular user to edit their notes

        Returns:
                Updated user notes with status message
        """
        
        
        try:
            notes = self.get_object(pk)
            notes_data = request.data
            if notes_data.get('user'): # fetching the details of particular email provided
                utils.get_user(request)
            if notes_data.get('collaborators'): # fetching the details of particular collaborator provided
                utils.get_collaborator_list(request)
            if notes_data.get('labels'): # fetching the details of particular label provided
                utils.get_label_list(request)
            serializer = NoteSerializer(notes, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger.debug('validated updated note data: {}'.format(serializer.data))
                result=utils.manage_response(status=True,message='updated successfully',data=serializer.data)
                return Response(result, status.HTTP_200_OK)
            logger.error('Invalid note details entered')
            result=utils.manage_response(status=False,message=serializer.errors)
            return Response(result,status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            logger.exception('Requested note does not exist')
            result=utils.manage_response(status=False,message='note not found')
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Something went wrong')
            result=utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)


            
    def delete(self, request, pk):
        """
        Created a method to delete a particular user's note

        Args:
            pk (integer): id of particular user to delete their notes

        Returns:
            Delete the user notes with status message
        """
       
        try:
            notes = self.get_object(pk)
            notes.soft_delete() #soft deleteing particular note. it will be hidden for user to retirieve.
            logger.debug('deleted note with id: {}'.format(pk))
            result=utils.manage_response(status=True,message='deleted successfully')
            return Response(result,status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            logger.exception('Requested note does not exist')
            result=utils.manage_response(status=False,message='note not found')
            return Response(result,status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Something went wrong')
            result=utils.manage_response(status=False,message='something wrong')
            return Response(result,status.HTTP_400_BAD_REQUEST)

