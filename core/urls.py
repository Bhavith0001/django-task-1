from django.urls import path
from . import views


urlpatterns = [
    path('user-list/', views.user_list),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('me/', views.me),
]