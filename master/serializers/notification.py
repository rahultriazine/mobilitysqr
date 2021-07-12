from rest_framework import serializers
from mobility_apps.master.models import Notification

class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Notification
        # fields = ('firstname','lastname')
        fields = '__all__'

