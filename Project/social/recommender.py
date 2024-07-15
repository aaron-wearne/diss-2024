from django.contrib.auth.models import User
from .models import Post, Tag
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to generate the user-likes matrix
def get_user_likes_matrix():
    users = list(User.objects.all())
    posts = list(Post.objects.all())
    user_likes = np.zeros((len(users), len(posts)))

    for i, user in enumerate(users):
        for j, post in enumerate(posts):
            if user in post.likes.all():
                user_likes[i, j] = 1
    
    return user_likes, users, posts

# Function to recommend posts based on user similarity
def recommend_posts_for_user(user_id, num_recommendations=10):
    user_likes, users, posts = get_user_likes_matrix()
    user_index = [user.id for user in users].index(user_id)

    user_similarity = cosine_similarity(user_likes)
    similar_users = np.argsort(-user_similarity[user_index])[1:]

    recommended_posts = set()

    for similar_user_index in similar_users:
        if len(recommended_posts) >= num_recommendations:
            break
        similar_user = users[int(similar_user_index)]
        similar_user_posts = Post.objects.filter(author=similar_user)
        for post in similar_user_posts:
            if len(recommended_posts) >= num_recommendations:
                break
            if post not in recommended_posts:
                recommended_posts.add(post)

    recommended_posts = list(recommended_posts)[:num_recommendations]
    return recommended_posts

# New class to recommend posts based on tags
class TagRecommender:
    
    @staticmethod
    def get_tags_liked_by_user(user):
        liked_posts = Post.objects.filter(likes=user)
        tags = Tag.objects.filter(post__in=liked_posts).distinct()
        return tags

    @staticmethod
    def get_recommended_posts_for_user_by_tags(user, num_recommendations=10):
        tags = TagRecommender.get_tags_liked_by_user(user)
        tag_recommended_posts = Post.objects.filter(tags__in=tags).distinct().exclude(author=user)
        return tag_recommended_posts[:num_recommendations]