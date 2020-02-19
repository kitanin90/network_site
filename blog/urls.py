from django.contrib.auth.views import LogoutView
from django.urls import path

from blog import views
from blog.views import UpdateGroup
from blog.views import UpdateProfile, HomeView, LoginView, UserWorkflow, CreateGroup, GroupDelete

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('panel/login', LoginView.as_view(), name='login'),
    path('panel/logout/', LogoutView.as_view(), name='logout'),
    path('panel/workflow/', UserWorkflow.as_view(), name='workflow'),
    # work with group
    path('panel/group/', views.group, name='group'),
    path('panel/group/delete/<int:pk>/', GroupDelete.as_view(), name='group-delete'),
    path('panel/group/creategroup', CreateGroup.as_view(), name='creategroup'),
    path('panel/group/<name>/', views.group_detail, name='group_detail'),
    # work with friend
    path('panel/my_profile/<str:slug>', UpdateProfile.as_view(), name='my_profile-detail'),
    path('panel/group/edit/<int:pk>/', UpdateGroup.as_view(), name='edit-group'),

    path('panel/users/', views.user_list, name='user_list'),
    path('panel/users/<username>/', views.user_detail, name='user_detail'),
]
