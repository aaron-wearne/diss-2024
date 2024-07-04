from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.
class PostListView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()


        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'social/post_list.html', context)

    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user 
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'social/post_list.html', context)


class PostDetailView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')


        context = {
            'post': post,
            'form': form,
            'comments': comments,

        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form, 
            'comments': comments,
        }
        return render(request, 'social/post_detail.html', context)

class PostEditView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs ={'pk':pk})
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        return self.request.user == post.author 

    
class PostDeleteView(DeleteView):
    model = Post 
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self) -> str:
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['post_pk'] = comment.post.pk
        return context