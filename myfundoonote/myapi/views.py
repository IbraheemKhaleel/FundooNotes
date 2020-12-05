from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AccountDetailSerializer
from .models import User
# Create your views here.

class AccountView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = AccountDetailSerializer