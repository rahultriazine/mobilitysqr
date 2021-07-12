from rest_framework import serializers
from .models import Letters
class LettersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields = '__all__'