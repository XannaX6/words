from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.FileField(upload_to='profile/', max_length=200, null=False, blank=False)
    user_type = models.CharField(max_length=5, default="user")
    country = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user_type}, {self.country}"
    
class Article(models.Model):
    BOOK = "book"
    MOVIE = "movie"
    ENT = "entertain"
    POLITICS = 'politics'
    WN = 'world news'
    
    TITLE_CHOICES = [
    (MOVIE, "Movies"),
    (BOOK, "Books"),
    (ENT, "Entertain"),
    (POLITICS, "Politics"),
    (WN, "World News"),
    ]

    title = models.CharField(max_length=200, null=False, blank=False)
    cover = models.FileField(upload_to='cover/', max_length=200, null=False, blank=False)
    content = models.TextField()
    summary = models.CharField(max_length=220, null=False, blank=False)
    category = models.CharField(max_length=10, null=False, blank=False, choices=TITLE_CHOICES,)
    comments = models.IntegerField(default=0, null=False, blank=False)
    clicks = models.IntegerField(default=0, null=False, blank=False)
    created_at = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}, {self.summary}"

class Comment(models.Model):
    articles = models.ForeignKey(Article, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    user_agent = models.CharField(max_length=300, null=True, blank=True)
    ip_address = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.comment}, {self.ip_address}, {self.user_agent}"

class Click(models.Model):
    articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_agent = models.CharField(max_length=300, null=True, blank=True)
    ip_address = models.CharField(max_length=300, null=True, blank=True)
    viewed_time = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user_agent}, {self.ip_address}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=300)
    created_at = models.DateField(default=datetime.date.today)
