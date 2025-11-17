from django.contrib import admin

from .models import Article, Profile, Click, Comment

# Register your models here.

class ArticlesAdmin(admin.ModelAdmin):
    fields = [
        "title", "cover", "content", "summary", "category", "comments", "clicks", "created_at", "user"
        ]
    
class ProfileAdmin(admin.ModelAdmin):
    fields = [
        "profile", "user_type", "country", "state", "mobile", "user"
        ]

admin.site.register(Article, ArticlesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Click)
admin.site.register(Comment)