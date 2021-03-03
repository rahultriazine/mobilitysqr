from rest_framework import serializers
from .models import Organizations,Organization_branches,Organization_users,Sub_Organization_branches
from mobility_apps.employee.models import Userinfo

class OrganizationsSerializers(serializers.ModelSerializer):
    contact_person_email = serializers.EmailField(allow_blank=True,allow_null=True)
    org_name = serializers.CharField(max_length=100,required=True)
    class Meta:
        model = Organizations
        fields = '__all__'
    '''
    def validate_org_name(self, value):
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
    '''
    '''
    def validate_contact_person_email(self, value):
        if value:
            check_query = Organization_users.objects.filter(contact_person_email=value)
            if self.instance:
                check_query = check_query.exclude(pk=self.instance.pk)
                # if self.parent is not None and self.parent.instance is not None:
                # genre = getattr(self.parent.instance, self.field_name)
                # check_query = check_query.exclude(pk=genre.pk)

            if check_query.exists():
                raise serializers.ValidationError('username already exists')
        return value
    '''
class Organization_branchesSerializers(serializers.ModelSerializer):
    contact_person_email = serializers.EmailField()
    class Meta:
        model = Organization_branches
        fields = '__all__'


class Sub_Organization_branchesSerializers(serializers.ModelSerializer):
    #contact_person_email = serializers.EmailField()
    class Meta:
        model = Sub_Organization_branches
        fields = '__all__'

class Organization_usersSerializers(serializers.ModelSerializer):
    #email = serializers.EmailField(allow_blank=True,allow_null=True)
    class Meta:
        model = Organization_users
        fields = '__all__'
    '''
    def validate_username(self, value):
        if value:
            check_query = Organization_users.objects.filter(email=value)
            if self.instance:
                check_query = check_query.exclude(pk=self.instance.pk)
                #if self.parent is not None and self.parent.instance is not None:
                #genre = getattr(self.parent.instance, self.field_name)
                #check_query = check_query.exclude(pk=genre.pk)

            if check_query.exists():
                raise serializers.ValidationError('username already exists')
        return value
    '''

class UserinfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = '__all__'
