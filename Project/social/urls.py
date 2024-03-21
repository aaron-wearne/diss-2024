from django.urls import path
from . import views


#urlConf
urlpatterns = [
    path("", views.index, name = "index")
    
]