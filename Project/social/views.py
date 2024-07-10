from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.db.models import Count, Case, When, Q
from .recommender import recommend_posts_for_user

# Create your views here.
class PostListView(LoginRequiredMixin, View): #in future views put loginrequired/userpassesstest before the inherited view else won't work
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


class PostDetailView(LoginRequiredMixin, View):
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

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs ={'pk':pk})
    
    def test_func(self) -> bool | None: #check for user == author of the post before allowing edit. test with localhost/social/post/edit/*post number*
        post = self.get_object()
        return self.request.user == post.author 

    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self) -> bool | None: #check for user == author of the post before allowing delete. test with localhost/social/post/delete/*post number*
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        return self.request.user == post.author
    
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False
        
        for follower in followers:
            if follower == request.user: #check if follower == user 
                is_following = True
                break
            else:
                is_following = False #if they're not following set to false

        number_of_followers = len(followers)

        context ={
            'user':user,
            'profile':profile,
            'posts':posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,


        }
        return render(request,'social/profile.html', context)
    
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'profile_picture']
    template_name = 'social/edit_profile.html'

    def get_success_url(self) -> str:
        pk=self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk':pk})
    
    def test_func(self) -> bool | None:
        profile=self.get_object()
        return self.request.user == profile.user 
    
class Follow(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)

class Unfollow(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        return redirect('profile', pk=profile.pk)
    
class Like(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_list = Post.objects.annotate(
            liked=Count(Case(When(likes=user, then=1)))
        )
        context['post_list'] = post_list
        return context


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query =self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query)
        )

        context ={
            'profile_list':profile_list
        }
        return render(request, 'social/search.html', context)
    

class RecommendedPostsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        recommended_posts = recommend_posts_for_user(user.id)
        
        context = {
            'recommended_posts': recommended_posts
        }
        return render(request, 'social/recommended_posts.html', context)