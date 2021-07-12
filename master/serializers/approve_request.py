from rest_framework import serializers
from mobility_apps.master.models import Approval_Hierarchy,Request_Approvals,Status_Master


class Approve_RequestSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Approval_Hierarchy
        # fields = ('firstname','lastname')
        fields = '__all__'

class Request_ApprovalsSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Request_Approvals
        # fields = ('firstname','lastname')
        fields = '__all__'




class Status_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Status_Master
        # fields = ('firstname','lastname')
        fields = '__all__'