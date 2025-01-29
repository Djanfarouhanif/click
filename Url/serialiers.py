from rest_framework import serializers
from .models import Click
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())]) # Vérifier que l'email est uniqe
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self,validated_data):
            # Crée un nouvel utilisateur avec les données validées
        user = User.objects.create_user(
        username=validated_data['username'],
        email = validated_data['email'],
        password=validated_data['password']
            )      
        return user
class ClickSerializer(serializers.ModelSerializer):

    # user = serializers.SlugRelatedField(
    #     queryset=User.objects.all(),  # Récupère les utilisateurs disponibles
    #     slug_field="email"           # Utilise l'email pour identifier l'utilisateur
    #     )
    #user = UserSerializer()

    link_name = serializers.CharField(max_length=200, required=True)
    
    class Meta:
        model = Click
        fields = ['id','link_name', 'url', 'clicks', 'url_output']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)