from rest_framework import serializers

from .models import User

class AccountDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name' , 'email' , 'password' , 'created')