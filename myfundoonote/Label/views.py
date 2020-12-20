from django.shortcuts import render
import logging
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LabelSerializer
from .models import Label


default_error_response = {'message':'error', 'status':status.HTTP_400_BAD_REQUEST}
# Create your views here.
class Labels(APIView):
    """
    Created a class to display list of notes saved inside
    """
    
    serializer_class = LabelSerializer
    def get(self , request):
        """
        Created a method to display list of notes saved in
        Returns:
        json: list of notes with complete details
        """
        try:
            label = Label.objects.all() #accessing all the object details into a variable
            serializer = LabelSerializer(label, many=True) #serializing the variable using LabelSerializer
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(default_error_response)
    
    def post(self, request):
        """
        Created a method to create a new note
        Returns:
        json: new note's saved details
        """
        try:
            serializer = LabelSerializer(data=request.data) #serializing the input details given by user
            if serializer.is_valid(): #Checks whether the given details are valid or not using in built is_valid function
                serializer.save() #saving into database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(default_error_response)


class UpdateLabel(APIView):
    """
    Created a class to update a note
    
    """
    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(default_error_response)
    def get(self, request, pk):
        label = self.get_object(pk)
        serializer = LabelSerializer(label)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk):
        label = self.get_object(pk)
        serializer = LabelSerializer(label, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        label = self.get_object(pk)
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)