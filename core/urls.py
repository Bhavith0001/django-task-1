from django.urls import path
from . import views


urlpatterns = [
    path('user-list/', views.user_list, name='user_list'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('current-user/', views.current_user, name='current_user'),
]