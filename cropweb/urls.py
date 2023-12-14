from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
   
        path('',home,name='home'),
        path('predictcrop/',predictcrop,name='predictcrop'),
        path('register/',UserRegisterView.as_view(),name='register'),
        path('login_view/',login_view,name='login_view'),
        

    path('logout/', logout_view, name='logout'),

]
