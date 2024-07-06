from django.urls import path 
from landing.views import Index, Login, Sign_up

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/login', Login.as_view(), name='login'),
    path('accounts/signup', Sign_up.as_view(), name='sign-up')
]