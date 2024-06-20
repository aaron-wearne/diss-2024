from django.shortcuts import render
from django.views import View 
from .models import Post

# Create your views here.
class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')

        context = {
            'post_list': posts,
        }

        return render(request, 'post_list.html', context)