"""
Author: Ibraheem Khaleel
Created on: 15th December 20 
"""

import logging
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NoteSerializer
from .models import Note
from . import utils


# Create your views here.

default_error_response = {'message':'error', 'status':False}


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

class Notes(APIView):
    """
    Created a class to display list of notes saved inside
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
            success_message = {'message':'success', 'status':True, 'data' : serializer.data }
            return Response(success_message, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """
        Created a method to create a new note
        Returns:
        json: new note's saved notes
        """
        try:
            if request.data.get('user'):
                utils.get_user(request)
            if request.data.get('collaborators'):
                utils.get_collaborator_list(request)
            if request.data.get('labels'):
                utils.get_label_list(request)
            serializer = NoteSerializer(data=request.data) #serializing the input notes given by user
            if serializer.is_valid(): #Checks whether the given notes are valid or not using in built is_valid function
                serializer.save() #saving into database
                success_message = {'message':'success', 'status': True, 'data' : serializer.data }
                return Response(success_message, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST)


class UpdateNote(APIView):
    """
    Created a class to update a note
    
    """
    serializer_class = NoteSerializer
    def get_object(self, pk):
        """
        Created a method to retrieve an object notes

        parameter:  primary key given to retrieve notes of particular user

        return: user notes of particular user
        """
        try:
            return Note.objects.get(id = pk) #calls get method to retrieve a particular user notes
        except Note.DoesNotExist:
            default_error_response['message'] = 'Note does not exist'
            return Response(default_error_response,status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk):
        try:
            notes = self.get_object(pk=pk)
            serializer = NoteSerializer(notes)
            success_message = {'message':'success', 'status': True, 'data' : serializer.data }
            return Response(success_message, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST)

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
            serializer = NoteSerializer(notes, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                success_message = {'message':'success', 'status':True, 'data' : serializer.data }
                return Response(success_message, status=status.HTTP_200_OK)
            return Response(default_error_response, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST)
            
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
            notes.soft_delete()
            response_message = {'message' : 'successfully deleted', 'status' : True}
            return Response(response_message, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(default_error_response, status.HTTP_400_BAD_REQUEST) 

