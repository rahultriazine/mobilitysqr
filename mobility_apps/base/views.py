# from braces.views import CsrfExemptMixin
# from django.contrib.auth.models import User
# # Create your views here.
# from oauth2_provider.settings import oauth2_settings
# from oauth2_provider.views.mixins import OAuthLibMixin
# from rest_framework import viewsets, views
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
#
#
# class RegistrationSerialiser(views.Serializer):
#     # client_id = views.CharField(required=False)
#     # client_secret = views.CharField(required=False)
#     # grant_type = views.CharField(required=False)
#     password = views.CharField(required=True)
#     email = views.EmailField(required=True)
#     first_name = views.CharField(required=True)
#     last_name = views.CharField(required=True)
#
#
# class RegistrationViewset(viewsets.ViewSet, CsrfExemptMixin, OAuthLibMixin):
#     permission_classes = (AllowAny,)
#     server_class = oauth2_settings.OAUTH2_SERVER_CLASS
#     validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
#     oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
#
#     def create(self, request, *args, **kwargs):
#
#         serialiser = RegistrationSerialiser(data=request.data)
#         serialiser.is_valid(raise_exception=True)
#         user, is_new_user = self.create_or_get_user(serialiser.data)
#         return Response(status=200)
#
#     def create_or_get_user(self, validated_data):
#         password = validated_data.get('password')
#         username = validated_data.get('email')
#         first_name = validated_data.get('first_name')
#         last_name = validated_data.get('last_name')
#         try:
#             user = User.objects.get(username=username)
#             return user, False
#         except:
#             user = User.objects.create(username=username, password=password, email=username, first_name=first_name,
#                                        last_name=last_name)
#
#             return user, True
#
#     # def handle_token_task(self, request, is_new_user, user):
#     #     print(dir(request))
#     #     print("***************")
#     #     print(request.user)
#     #     print("###########")
#     #     print(request.data)
#     #     print(request.POST._mutable)
#     #     print(dir(request.POST))
#     #     print(request.POST._assert_mutable)
#     #
#     #     if not request.POST._mutable:
#     #         request.POST._mutable = True
#     #         print(request.POST._mutable)
#     #     request.POST.__setitem__('username',user.username)
#     #     url, headers, body, status = self.create_token_response(request)
#     #     response_data = json.loads(body)
#     #     response_data['new_user'] = is_new_user
#     #     return Response(response_data, status=status)
