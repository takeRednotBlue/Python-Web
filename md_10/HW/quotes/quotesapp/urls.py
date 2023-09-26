from django.urls import path

from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('author/<str:author_name>/', views.author_info, name='author'),
]