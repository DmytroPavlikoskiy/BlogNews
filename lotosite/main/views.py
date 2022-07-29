from django.shortcuts import render, redirect, get_object_or_404
from .models import News, LikeNews, CommentsNews, LikeComment
from .forms import UserRegisterForm, UserLogin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView, CreateView, FormView, UpdateView


def home(request):
    news = News.objects.order_by('-date')
    return render(request, 'main/home.html', {'news': news})


def news_home(request):
    news = News.objects.order_by('-date')
    return render(request, 'main/news_home.html', {'news': news})


def one_news(request, news_id):
    user_id = request.user.id
    news = News.objects.get(id=news_id)
    comments = CommentsNews.objects.filter(news_id=news.id)
    for comment in comments:
        comment.if_user_like = LikeComment.objects.filter(comment_id=comment.id, user_id=request.user.id)
    likes = LikeNews.objects.filter(news_id=news.id, user_id=user_id)
    return render(request, 'main/one_news.html', {'news': news, 'likes': likes,
                                                  'comments': comments})


class CreatePostView(CreateView):
    model = News
    template_name = 'main/create_news.html'
    fields = ['title', 'anons', 'full_text', 'image_post', 'date', 'user']



def yours_news(request):
    user_id = request.user.id
    user_news = News.objects.filter(user_id=user_id)
    return render(request, 'main/your_news.html', {'user_news': user_news})


class NewsUpdate(UpdateView):
    model = News
    template_name = 'main/update_news.html'
    fields = ['title', 'anons', 'full_text', 'image_post', 'date', 'user']


def delete_news(request, news_id):
    news = News.objects.get(id=news_id)
    news.delete()
    return redirect('yours_news')



def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Ви успішно зареєстрованні!')
            return redirect('login')
        else:
            messages.seccess(request,'Упсс, щось пішло не так')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLogin()
    return render(request, 'main/login_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def add_like(request, news_id):
    user_id = request.user.id
    likes = LikeNews.objects.filter(news_id=news_id, user_id=user_id)
    if likes:
        likes.delete()
    else:
        like = LikeNews()
        like.news_id = news_id
        like.user_id = request.user.id
        like.save()
    return redirect('/one_news/' + str(news_id))


def add_comments(request, news_id):
    user_id = request.user.id
    comment = CommentsNews()
    comment.news_id = news_id
    comment.user_id = user_id
    comment.comment = request.POST.get('comments')
    comment.save()
    return redirect('/one_news/' + str(news_id))


def like_comments(request, news_id, comment_id):
     user_id = request.user.id
     likes_comment = LikeComment.objects.filter(user_id=user_id, comment_id=comment_id)
     comment = CommentsNews.objects.get(id=comment_id)
     if likes_comment:
         likes_comment.delete()
     else:
        like = LikeComment()
        like.user = request.user
        like.comment = comment
        like.save()
     return redirect('/one_news/' + str(news_id))