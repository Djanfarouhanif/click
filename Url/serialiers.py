from rest_framework import serializers
from .models import Click


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['unique_code','url', 'clicks','url_output']