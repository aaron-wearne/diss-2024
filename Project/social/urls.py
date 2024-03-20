from django.urls import path
from . import views


#urlConf
urlpatterns = [
    path('home', views.home)
    
]