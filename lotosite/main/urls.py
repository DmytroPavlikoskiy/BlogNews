from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='home'),
    path('news', news_home, name='news'),
    path('one_news/<int:news_id>/', one_news, name='one_news'),
    path('create', CreatePostView.as_view(), name='create'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register_user, name='register'),
    path('like/<int:news_id>', add_like, name='like'),
    path('comments/<int:news_id>', add_comments, name='comment'),
    path('one_news/<int:news_id>/<int:comment_id>', like_comments, name='like_comment'),
    path('yours_news', yours_news, name='yours_news'),
    path('yours_news/<int:pk>/update', NewsUpdate.as_view(), name='news-update'),
    path('delete/<int:news_id>', delete_news, name='delete_news')
]

