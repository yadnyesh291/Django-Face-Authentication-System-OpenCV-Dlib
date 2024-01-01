from django.urls import path 
from .import views
urlpatterns = [
    path('index/',views.login, name='login'), 
    path('', views.home), 
    path('register/',views.register),
]