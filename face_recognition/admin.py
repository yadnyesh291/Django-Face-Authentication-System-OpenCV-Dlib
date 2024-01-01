from django.contrib import admin

from django.contrib.auth.models import Group 
from face_recognition.models import UserProfile




          #admin.site.register (UserProfile) 
@admin.register(UserProfile)
class UserProfile (admin.ModelAdmin): 
    list_display = ('name', 'username', 'email')
admin.site.site_header ='WEB APP AUTHENICATION USING FACE RECOGNITION DASHBOARD'
# Class UserCreationForm(admin.ModelAdmin):
# list_display = ('name', 'username', 'password', 'image')
# list_filter ('created',)
#1 change_list_template = 'face_recognition/home.html'
