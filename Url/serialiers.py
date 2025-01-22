from rest_framework import serializers
from .models import Click
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

class ClickSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field= "email" # Permet d'utiliser le champ email
    )
    class Meta:
        model = Click
        fields = ['unique_code','user','url', 'clicks','url_output']