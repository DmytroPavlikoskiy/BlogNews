from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField
from django.urls import reverse
from django.utils import timezone



class News(models.Model):
    title = models.CharField('Назва', max_length=255)
    anons = models.CharField('Анонс', max_length=255)
    full_text = models.TextField('Новина')
    image_post = models.ImageField(upload_to='image/pdfs/', blank=True)
    date = models.DateTimeField('Дата Публікації')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '|' + str(self.user)

    def get_absolute_url(self):
        return reverse('home')


    class Meta:
        verbose_name = 'Новини'
        verbose_name_plural = 'Новини'



class LikeNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class CommentsNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    news = models.ForeignKey(News, related_name='comments' ,on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField('Дата Публікації', default=timezone.now())
    likes = models.ManyToManyField('LikeComment')


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    comment = models.ForeignKey(CommentsNews, on_delete=models.CASCADE, null=True)