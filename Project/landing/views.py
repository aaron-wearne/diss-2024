from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register/index.html')

