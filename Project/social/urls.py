from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, ProfileEditView, Follow, Unfollow, Like, UserSearch


urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='edit-profile'),
    path('profile/<int:pk>/followers/add', Follow.as_view(), name='follow'),
    path('profile/<int:pk>/followers/remove', Unfollow.as_view(), name='unfollow'),
    path('post/<int:pk>/like', Like.as_view(), name='like'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    
]