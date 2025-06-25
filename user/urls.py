from tempfile import template


from django.urls import path
from django.views import View
from user.views import RegisterView,LoginView,ProfileUpdateView,ProfileView, ProfileDetailView, UserListView


urlpatterns = [
   # path('create_user/', views.create_user, name='create_user')
    path('registr/',RegisterView.as_view(), name='register'),
    path ('login/',LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/',LoginView.as_view(), name='logout'),
    path('profile/update/<int:pk>',ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:pk>',ProfileView.as_view(), name='profile'),
    path('profile/detail/<int:pk>',ProfileDetailView.as_view(), name='profile_detail'),
    path('users/', UserListView.as_view(), name='user_list'),

]