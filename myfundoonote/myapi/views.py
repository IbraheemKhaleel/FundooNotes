from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import AccountDetailSerializer
from .models import User
from django.contrib.auth import login
from django.urls import reverse
from .forms import CustomUserCreationForm
from rest_framework.permissions import IsAuthenticated

# views

class AccountView(ModelViewSet):
    """
    Creating class for viewing all the objects we stored in database
    Inheriting ModelviewSet so that it helps to carry out CRUD operations without
    defining seperate get,post,delete and put methods
    queryset:  It takes all the objects in database of User model.
    serializer_class: It takes serilised JSON data from AccountDetailSerializer class
    """

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountDetailSerializer

def dashboard(request):
    """
    paramter: request from user to render specific html page
    return: It returns dashboard html page which we defined in templates.
    """
    return render(request , "users/dashboard.html")   

def register(request):
    """
    creating a method for registration,login and logout of user
    parameter: request from user for particular service
    """
    if request.method == "GET":
        return render(
            request, "users/register.html",  #maps to register html page which we defined in templates
            {"form": CustomUserCreationForm} #contains the customer user creation form which is in built service of django
        )  
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST) #If the form is submitted, It will create a new usercreationform for new user
        if form.is_valid():                         #If the details are vaild, it will create new user and save it in database 
            user = form.save()                      
            login(request , user)                   #And the user will be logged in using login() inbuilt django function
            return redirect(reverse("dashboard"))   #it will render back to dashboard html webpage
        