from django.contrib import admin
from django.urls import path
from .views import index
from django.conf import settings
from django.conf.urls.static import static


app_name='users'
urlpatterns = [
    path('',index,name='index'),

]
