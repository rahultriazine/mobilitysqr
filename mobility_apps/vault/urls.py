from django.urls import include, path, re_path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('get_post_vault_type/', getPostVaultType.as_view(), name='get_post_vault_type'),
    path('get_post_vault_document/', getPostVaultDocument.as_view(), name='get_post_vault_document'),
    path('update_delete_vault_document/<int:pk>/',updateDeleteVaultDocument.as_view(), name='update_delete_vault_document'),
    path('get_post_compliance/', getPostCompliance.as_view(), name='get_post_compliance'),
    path('get_post_compliance_answer/', getPostComplianceAnswer.as_view(), name='get_post_compliance_answer'),

]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL+'/vaultDocument/', document_root=settings.MEDIA_ROOT+'/vaultDocument/')