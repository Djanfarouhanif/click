from rest_framework import serializers
from .models import Click
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ClickSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Click
        fields = ['unique_code','user','url', 'clicks','url_output']