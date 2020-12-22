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

#logging.basicConfig(filename='notes.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

#TODO : Add Exceptions and messages

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
        try:
            return Response(api_urls)
        except Exception as e:
            response= {'message' : str(e), 'status' : False}
            return Response(response, status.HTTP_404_NOT_FOUND)


class NotesView(APIView):
    """
    Created a class to display list of notes saved inside
    """
    
    
    def get(self , request):
        """
        Created a method to display list of notes saved in
        Returns:
        json: list of notes with complete notes
        """
        response= {'message':'error', 'status':False}

        try:
            notes = Note.objects.filter(is_deleted=False) #accessing all the object notes into a variable
            serializer = NoteSerializer(notes, many=True) #serializing the variable using NoteSerializer
            response['message'] = 'Note retrieved successfully' 
            response['status'] = True 
            response['data'] = serializer.data
            return Response(response, status.HTTP_202_ACCEPTED)
        except FileNotFoundError:
            response['message'] = 'The notes does not exist. Please create a note'
            response['status'] = False
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False
            return Response(response, status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """
        Created a method to create a new note
        Returns:
        json: new note's saved notes
        """
        response= {'message':'error', 'status':False}
        try:
            notes_details = request.data
            if notes_details.get('user'):
                utils.get_user(request)
            if notes_details.get('collaborators'):
                utils.get_collaborator_list(request)
            if notes_details.get('labels'):
                utils.get_label_list(request)
            serializer = NoteSerializer(data=request.data) #serializing the input notes given by user
            if serializer.is_valid(): #Checks whether the given notes are valid or not using in built is_valid function
                serializer.save() #saving into database
                response['message'] = 'Note added successfully'
                response['status'] = True
                response['data'] = serializer.data
                return Response(response, status.HTTP_201_CREATED)
            response['message'] = serializer.errors
            response['status']= False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except PermissionError:
            response['message'] = 'Please login to carryout request'
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
    """
    Created a class to update a note
    
    """
    
    def get_object(self, pk):
        """
        Created a method to retrieve an object notes

        parameter:  primary key given to retrieve notes of particular user

        return: user notes of particular user
        """
        response= {'message':'error', 'status':False}
        try:
            return Note.objects.get(id = pk, is_deleted = False) #calls get method to retrieve a particular user notes
        except Note.DoesNotExist:
            response['message'] = 'Note does not exists. Please create a note'
            response['status'] = False 
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk):
        response= {'message':'error', 'status':False}

        try:
            notes = self.get_object(pk=pk)
            serializer = NoteSerializer(notes)
            response['message'] = 'Respective Note retrieved successfully'
            response['status'] = True
            response['data']= serializer.data
            return Response(response, status.HTTP_202_ACCEPTED)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Created a put method to edit particular user notes
        Args:
            pk (integer): id of particular user to edit their notes

        Returns:
                Updated user notes with status message
        """
        response= {'message':'error', 'status':False}
        try:
            notes = self.get_object(pk)
            notes_details = request.data
            if notes_details.get('user'): # fetching the details of particular email provided
                utils.get_user(request)
            if notes_details.get('collaborators'): # fetching the details of particular collaborator provided
                utils.get_collaborator_list(request)
            if notes_details.get('labels'): # fetching the details of particular label provided
                utils.get_label_list(request)
            serializer = NoteSerializer(notes, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                response['message'] = 'Note updated successfully'
                response['status'] = True
                response['data']= serializer.data
                return Response(response, status.HTTP_200_OK)
            response['message'] = serializer.errors
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except PermissionError:
            response['message'] = 'Please login to carryout request'
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, pk):
        """
        Created a method to delete a particular user's note

        Args:
            pk (integer): id of particular user to delete their notes

        Returns:
            Delete the user notes with status message
        """

        response= {'message':'error', 'status':False}
        try:
            notes = self.get_object(pk)
            notes.soft_delete() #soft deleteing particular note. it will be hidden for user to retirieve.
            response['message'] = 'Note deleted successfully'
            response['status'] = True
            return Response(response, status.HTTP_202_ACCEPTED)
        except PermissionError:
            response['message'] = 'Please login to carryout request'
            response['status'] = False
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST) 

