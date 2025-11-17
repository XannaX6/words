from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("category/", views.category, name="category"),
    path("contact", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout_user, name="logout"),
    path("search/", views.search, name="search"),
    path("upload/", views.upload, name="upload"),
    path("read/<int:article_id>/<str:article_title>", views.read, name="read"),
    path("logtime/", views.log_time, name='logtime'),
    path("comment/<int:article_id>", views.comments, name="comment"),
    path("profile/<str:username>", views.profile, name="profile"),
]