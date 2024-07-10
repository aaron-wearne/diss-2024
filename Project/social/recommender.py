from django.contrib.auth.models import User
from .models import Post
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_user_likes_matrix():
    users = list(User.objects.all())
    posts = list(Post.objects.all())
    user_likes = np.zeros((len(users), len(posts)))

    for i, user in enumerate(users):
        for j, post in enumerate(posts):
            if user in post.likes.all():
                user_likes[i, j] = 1
    
    return user_likes, users, posts

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
