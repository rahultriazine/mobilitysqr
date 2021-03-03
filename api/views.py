from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from api.models import User
from rest_framework.response import Response
from api.serializers import UserProfileSerializer
from rest_framework import viewsets
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from api.permission import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


    def get_permissions(self):
        import ipdb;ipdb.set_trace()
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny,]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'delete':
            permission_classes = [IsLoggedInUserOrAdmin,]
        elif self.action == 'list' or self.action == 'destroy':
             permission_classes = [IsAdminUser,]
        return [permission() for permission in permission_classes]


# Create your views here.

def http_status_codes(rgs):
    pass

class jwt_check(object):

    def __call__(self, func, *args, **kwargs):
            def wrap(class_obj, *args, **kwargs):
                # Use same http key in which you are sending key
                request_token = class_obj.request.META.get('HTTP_AUTHORIZATION', None)
                if request_token:
                    return func(class_obj, *args, **kwargs)
                else:
                 return Response({'message': 'please login first to access url', 'data': {}},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)

            return wrap


class Helloview(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        content={"message":'hello word'}
        return Response(content)