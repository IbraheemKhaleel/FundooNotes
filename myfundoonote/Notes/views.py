"""
Author: Ibraheem Khaleel
Created on: 15th December 20 
"""

import logging
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NoteSerializer,LabelSerializer
from .models import Note,Label
# Create your views here.

default_error_response = {'message':'error', 'status':status.HTTP_400_BAD_REQUEST}

class NotesOverview(APIView):
    """
    Created a class for displaying overview of urls using in operations

    """
    def get(self , request):
        """
        Created a method for displaying overview of urls 

        """
        api_urls = {
            'Note-List': '/note-list/',
            'Note-Detail - View':'/note-detail/<int:pk>/',
            'Note-Create':'/note-create/',
            'Note-Update':'/note-update/<int:pk>/',
            'Note-Delete':'/note-delete/<int:pk>/',
            'Label-List': '/label-list/',
            'Label-Create':'/label-create/',
            'Label-Update':'/label-update/<int:pk>/',
            'Label-Delete':'/label-delete/<int:pk>/',
        }
        return Response(api_urls)

class NotesList(APIView):
    """
    Created a class to display list of notes saved inside
    """
    
    serializer_class = NoteSerializer
    def get(self , request):
        """
        Created a method to display list of notes saved in
        Returns:
        json: list of notes with complete details
        """
        try:
            notes = Note.objects.all() #accessing all the object details into a variable
            serializer = NoteSerializer(notes, many=True) #serializing the variable using NoteSerializer
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class NotesDetail(APIView):
    """
    Created a class for displaying a particular notes using id

    Returns:
        json: details of note with specified id
    """
    serializer_class = NoteSerializer
    def get(self , request, pk):
        try:
            notes = Note.objects.get(id=pk) #accessing a particular note details using id 
            serializer = NoteSerializer(notes, many=False)
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class CreateNote(APIView):
    """
    Created a class to create new note
    """

    serializer_class = NoteSerializer
    def post(self, request):
        """
        Created a method to create a new note
        Returns:
        json: new note's saved details
        """
        try:
            serializer = NoteSerializer(data=request.data) #serializing the input details given by user
            if serializer.is_valid(): #Checks whether the given details are valid or not using in built is_valid function
                serializer.save() #saving into database
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class UpdateNote(APIView):
    """
    Created a class to update a note
    
    """
    serializer_class = NoteSerializer
    def post(self, request, pk):
        """
        Created a method to update a particular note using id provided
        Returns:
            json: updated note's saved details

        """
        try:
            note = Note.objects.get(id=pk)
            serializer = NoteSerializer(instance=note, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class DeleteNote(APIView):
    """
    Created a class to delete a note
    """
    serializer_class = NoteSerializer
    def delete(self , request , pk):
        """
        Created a method to delete a particular note using id
        Args:
            pk ([int]): id

        Returns:
           A String message with a status
        """
        try:
            note = Note.objects.get(id=pk)
            note.delete()
            return Response('Note successfully deleted.')
        except:
            return Response(default_error_response)


class LabelList(APIView):
    """
    Created a class to display labels

   
    """
    serializer_class = LabelSerializer
    def get(self , request):
        """
        Created a method to display list of labels used by user
        Returns:
            json: list of note labels saved
        """
        try:
            labels = Label.objects.all()
            serializer = LabelSerializer(labels, many=True)
            return Response(serializer.data)
        except:
            return Response(default_error_response)


class CreateLabel(APIView):
    """
    Created a class for creating labels
   
    """
    serializer_class = LabelSerializer
    def post(self, request):
        """
        Created a method to create new labels
        Returns:
            json: details of the created label
        """
        try:
            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class UpdateLabel(APIView):
    """
    Created a class to update an existing label

    """
    serializer_class = LabelSerializer
    def post(self, request, pk):
        """
        Created a method to update an existing label using id
        Returns:
            json: [updated label's saved details]
        """
        try:
            label = Label.objects.get(id=pk)
            serializer = LabelSerializer(instance=label, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except:
            return Response(default_error_response)

class DeleteLabel(APIView):
    """
    Created a class to delete a label

    """
    serializer_class = LabelSerializer
    def delete(self , request , pk):
        """
        Created a method to delete a particular with  id
        Returns:
            string: message with status
        """
        try:
            label = Label.objects.get(id=pk) #accessing a particular label using id to delete
            label.delete()
            return Response('Label successfully deleted.')
        except:
            return Response(default_error_response)