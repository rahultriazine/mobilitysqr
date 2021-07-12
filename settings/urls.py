"""family URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
# """
# from django.conf.urls import url, include
# from django.contrib import admin
# # from rest_framework.urlpatterns import format_suffix_patterns
# # from mobility_apps.employee import views
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#
# #     url('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
# #     url(r'^api/', include('mobility_apps.base.urls')),
#  ]
#
# #
# from rest_framework.decorators import authentication_classes, permission_classes, api_view
# from rest_framework.permissions import IsAuthenticated
# from django.conf.urls import url
# from django.contrib import admin
# # from .customer.urls import urlpatterns as customer_urls
# from django.urls import include, path
# from django.views.decorators.csrf import csrf_exempt

# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


from django.contrib import admin
from django.urls import include , path
from rest_framework import routers
from api.views import UserViewSet,Helloview
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mobility_apps.employee.views import jwt_custom_login

# from api import urls

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', include(router.urls)),
     path('', include("api.urls")),
     path('', include('mobility_apps.employee.urls')),
     path('', include('mobility_apps.master.urls')),
	 path('', include('mobility_apps.visa.urls')),
	 path('', include('mobility_apps.travel.urls')),
     path('', include('mobility_apps.letter.urls')),
     path('', include('mobility_apps.superadmin.urls')),
     path('', include('mobility_apps.reports.urls')),
     path('', include('mobility_apps.vault.urls')),
    # path('api-auth/', include("rest_framework.urls")),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('api/login/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
     path('api/custom/login/',jwt_custom_login.as_view(), name="login"),
     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_refresh'),
     # path(r'^api/rest_auth/"', django.conf.urls.include("rest_auth.urls")),

 ]
#from django.conf.urls.static import static
#from django.conf import settings




