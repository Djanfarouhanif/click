from rest_framework import serializers
from .models import Click
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())]) # Vérifier que l'email est uniqe

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def create(self,validated_data):
            # Crée un nouvel utilisateur avec les données validées
            user = User.objects.create_user(
                username=validate_data['username'],
                email = validate_data['eamil'],
                password=validated_data['password']
            )

            return user

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