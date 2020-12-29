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
from myfundooNotes.decorators import user_login_required



# Create your views here.

#logging.basicConfig(filename='Labels.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

#TODO : Add Exceptions and messages


@method_decorator(user_login_required, name='dispatch')
class LabelsOverview(APIView):
    """
    Created a class for displaying overview of urls using in operations

    """
    
    def get(self , request):
        """
        Created a method for displaying overview of urls 

        """
        api_urls = {    
            'label-CreateAndRetrieve':'/label/',
            'label-Update':'/label-update/<int:pk>/',
            'Label-CreateAndRetrieve': '/label/',
            'Label-UpdateAndDelete':'/label-update/<int:pk>/',
        }
        return Response(api_urls)
       
@method_decorator(user_login_required, name='dispatch')
class LabelsView(APIView):
    """
    Created a class to creating and retrieving  labels saved inside
    """
    serializer_class = LabelSerializer
    
    def get(self , request):
        """
        Created a method to display list of labels saved in
        Returns:
        json: list of labels with complete labels
        """
        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            labels = Label.objects.filter(is_deleted=False) #accessing all the object Labels into a variable
            serializer = LabelSerializer(labels, many=True) #serializing the variable using LabelSerializer
            response['message'] = 'label retrieved successfully' 
            response['status'] = True 
            response['data'] = serializer.data
            status_code = status.HTTP_202_ACCEPTED
        except Label.DoesNotExist:
            response['message'] = 'The Labels does not exist. Please create a Label'  
        except Exception as e:
            response['message'] = str(e)    
        finally:
            return Response(response, status_code)
        
    
    def post(self, request):
        """
        Created a method to create a new Label
        Returns:
        json: new Label's saved Labels
        """
        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            serializer = LabelSerializer(data=request.data) #serializing the input labels given by user
            if serializer.is_valid(): #Checks whether the given labels are valid or not using in built is_valid function
                serializer.save() #saving into database
                response['message'] = 'label added successfully'
                response['status'] = True
                response['data'] = serializer.data
                status_code = status.HTTP_201_CREATED
            response['message'] = serializer.errors   
        except PermissionError:
            response['message'] = 'Please login to carryout request' 
        except Exception as e:
            response['message'] = str(e)
        finally:
            return Response(response, status_code)


class LabelView(APIView):
    """
    Created a class to update and delete a label
    
    """
    serializer_class = LabelSerializer
    def get_object(self, pk):
        """
        Created a method to retrieve an object labels

        parameter:  primary key given to retrieve labels of particular user

        return: user labels of particular user
        """
        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            return Label.objects.get(id = pk, is_deleted = False) #calls get method to retrieve a particular user Labels
        except Label.DoesNotExist:
            response['message'] = 'Label does not exists. Please create a Label'
            return Response(response, status_code)
        except TypeError:
            response['message'] = 'Please enter an integer'  
            return Response(response, status_code) 
        except Exception as e:
            response['message'] = str(e)
            return Response(response, status_code)  
            

    def get(self, request, pk):

        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            labels = self.get_object(pk=pk)
            serializer = LabelSerializer(labels)
            response['message'] = 'Respective label retrieved successfully'
            response['status'] = True
            response['data']= serializer.data
            status_code = status.HTTP_202_ACCEPTED
        except TypeError:
            response['message'] = 'Please enter an integer'  
        except Exception as e:
            response['message'] = str(e)    
        finally:
            return Response(response, status_code)

    def put(self, request, pk):
        """
        Created a put method to edit particular user labels
        Args:
            pk (integer): id of particular user to edit their labels

        Returns:
                Updated user labels with status message
        """
        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            labels = self.get_object(pk)
            serializer = LabelSerializer(labels, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                response['message'] = 'label updated successfully'
                response['status'] = True
                response['data']= serializer.data
                status_code = status.HTTP_200_OK
            response['message'] = serializer.errors
        except TypeError:
            response['message'] = 'Please enter an integer'  
        except PermissionError:
            response['message'] = 'Please login to carryout request'   
        except Exception as e:
            response['message'] = str(e) 
        finally:
            return Response(response, status_code)

            
    def delete(self, request, pk):
        """
        Created a method to delete a particular user's label

        Args:
            pk (integer): id of particular user to delete their labels

        Returns:
            Delete the user labels with status message
        """
        response= {'message':'error', 'status':False}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            labels = self.get_object(pk)
            labels.soft_delete() #soft deleteing particular label. it will be hidden for user to retirieve.
            response['message'] = 'label deleted successfully'
            response['status'] = True
            status_code = status.HTTP_200_OK
        except PermissionError:
            response['message'] = 'Please login to carryout request'
        except Exception as e:
            response['message'] = str(e)
        finally:
            return Response(response, status_code)