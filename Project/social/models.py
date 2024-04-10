from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_post = models.ImageField(upload_to='post_images', blank=True)

    def __str__(self):
        return f"Post by {self.author} on {self.created_at}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user} likes {self.post}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Connections(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
    
    def __str__(self):
        return f"{self.follower} follows {self.followed}"
    

class Share(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shared_posts')
    comment = models.TextField(blank=True)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} shared on {self.shared_at}'
    
class Homepage:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def get_recent_posts(self):
        """
        Fetch recent posts from the user and their connections.
        """
        # Assuming a method to get user connections. This will be a simplified placeholder.
        # In practice, you would perform a database query here.
        connections = self.user_profile.following.all()
        connection_ids = [connection.followed.id for connection in connections]
        
        # Fetch posts from the user and their connections
        recent_posts = Post.objects.filter(
            author__in=connection_ids + [self.user_profile.id]
        ).order_by('-created_at')[:10]  # Just an example to limit to 10 recent posts
        
        return recent_posts

    def get_feed_items(self):
        """
        Aggregates feed items such as posts, likes, and comments for the homepage feed.
        """
        recent_posts = self.get_recent_posts()
        feed_items = []
        for post in recent_posts:
            post_details = {
                'post': post,
                'likes': post.likes.count(),
                'comments': post.comments.all(),
                'shares': post.shares.count(),
            }
            feed_items.append(post_details)
        return feed_items