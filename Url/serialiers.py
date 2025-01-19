from rest_framework import serializers
from .models import Click


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['url', 'clicks', 'unique_code']