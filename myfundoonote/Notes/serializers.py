from rest_framework import serializers
from .models import Note
from myfundooNotes.models import User
from rest_framework.response import Response
from Label.models import Label

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

    
   