from django.urls import path
from .views import PostListView


urlpatters = [
    path('', PostListView.as_view(), name='post-list' ),
]