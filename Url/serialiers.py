from rest_framework import serializers
from .models import Click
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

class ClickSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),  # Récupère les utilisateurs disponibles
        slug_field="email"           # Utilise l'email pour identifier l'utilisateur
        )
    #user = UserSerializer()
    
    class Meta:
        model = Click
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)