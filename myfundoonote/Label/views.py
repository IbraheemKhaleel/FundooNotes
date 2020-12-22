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
from .serializers import LabelSerializer
from .models import Label



# Create your views here.

#logging.basicConfig(filename='labels.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


#TODO : Add Exceptions and messages

class LabelsView(APIView):
    """
    Created a class to display list of Labels saved inside
    """
    
    
    def get(self , request):
        """
        Created a method to display list of labels saved in
        Returns:
        json: list of labels with complete labels
        """
        response= {'message':'error', 'status':False}

        try:
            labels = Label.objects.filter(is_deleted=False) #accessing all the object labels into a variable
            serializer = LabelSerializer(labels, many=True) #serializing the variable using LabelSerializer
            response['message'] = 'success' 
            response['status'] = True 
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except FileNotFoundError:
            response['message'] = 'The labels does not exist. Please create a Label'
            response['status'] = False
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False
            return Response(response, status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """
        Created a method to create a new Label
        Returns:
        json: new Label's saved labels
        """
        response= {'message':'error', 'status':False}
        try:
            serializer = LabelSerializer(data=request.data) #serializing the input labels given by user
            if serializer.is_valid(): #Checks whether the given labels are valid or not using in built is_valid function
                serializer.save() #saving into database
                response['message'] = 'success'
                response['status'] = True
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)
            response['message'] = 'Please fill valid entries'
            response['status']= False 
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except PermissionError:
            response['message'] = 'Please login to carryout request'
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)


class LabelView(APIView):
    """
    Created a class to update a Label
    
    """
    
    def get_object(self, pk):
        """
        Created a method to retrieve an object labels

        parameter:  primary key given to retrieve labels of particular user

        return: user labels of particular user
        """
        response= {'message':'error', 'status':False}
        try:
            return Label.objects.get(id = pk, is_deleted = False) #calls get method to retrieve a particular user labels
        except Label.DoesNotExist:
            response['message'] = 'Label does not exists. Please create a Label'
            response['status'] = False 
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        response= {'message':'error', 'status':False}

        try:
            labels = self.get_object(pk=pk)
            serializer = LabelSerializer(labels)
            response['message'] = 'success'
            response['status'] = True
            response['data']= serializer.data
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Created a put method to edit particular user Labels
        Args:
            pk (integer): id of particular user to edit their Labels

        Returns:
                Updated user Labels with status message
        """
        response= {'message':'error', 'status':False}
        try:
            labels = self.get_object(pk)
            serializer = LabelSerializer(labels, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                response['message'] = 'success'
                response['status'] = True
                response['data']= serializer.data
                return Response(response, status=status.HTTP_200_OK)
            response['message'] = 'Please fill valid entries'
            response['status'] = False 
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
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
        Created a method to delete a particular user's Label

        Args:
            pk (integer): id of particular user to delete their Labels

        Returns:
            Delete the user Labels with status message
        """ 
        response= {'message':'error', 'status':False}
        try:
            labels = self.get_object(pk)
            labels.soft_delete() #soft deleteing particular label. it will be hidden for user to retirieve. #soft deleteing particular label. it will be hidden for user to retirieve.
            response['message'] = 'success'
            response['status'] = True
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except PermissionError:
            response['message'] = 'Please login to carryout request'
            response['status'] = False
        except Exception as e:
            response['message'] = str(e)
            response['status'] = False 
            return Response(response, status.HTTP_400_BAD_REQUEST) 