from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/index.html')

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/login.html')
    
class Sign_up(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/signup.html')