from django.urls import include, path,re_path
from .views import *

urlpatterns = [
       path('addorganisation/', SaveOrganization.as_view(), name='add-organizations'),
       re_path(r'editorganisation/', SaveOrganization.as_view(), name='edit-organizations'),
       path('organisations-list/', SaveOrganization.as_view(), name='organizations-list'),
       path('addbranch/', Branch.as_view(), name='add-branch'),
       path('editbranch/', Branch.as_view(), name='add-branch'),
       path('branch-list/', Branch.as_view(), name='branch-list'),
       path('addOrgUser/', OrgUsers.as_view(), name='add-user'),
       path('editOrgUser/', OrgUsers.as_view(), name='edit-user'),
       path('orgcount/', get_org_count.as_view(), name='orgcount'),
       path('userlist/', OrgUsers.as_view(), name='user List'),
       path('subbranch/', SubBranch.as_view(), name='subbranch'),
       path('get_org/', get_org.as_view(), name='get_org'),

]