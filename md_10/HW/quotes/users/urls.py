from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.loginuser, name='login'),
    path('signup/', views.signupuser, name='signup'),
    path('logout/', views.logoutuser, name='logout'),
]