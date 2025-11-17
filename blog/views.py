from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
import json
from .models import Comment, Click, Article, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import UserForm, ArticleForm, ProfileForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import os


# Create your views here.

def index(request):
    featured_title = Article.objects.order_by('-clicks')[:1]
    # featured_title = get_object_or_404(Article, pk=1)
    top_story = Article.objects.order_by('-created_at')[:3]
    trending_articles = Article.objects.all()[:3]
    featured = Article.objects.all()[:2]
    context = {
        'featured_title': featured_title,
        'top_story': top_story,
        'trending_articles': trending_articles,
        'featured': featured,
        }
    return render(request, 'blog/index.html', context)

def profile(request, username):
    g_user = User.objects.get(username=username)
    try:
        profile = g_user.profile
        p = ProfileForm(instance=profile)
        old_img = profile.profile.path if profile.profile else None
    except:
        profile = None
        p = ProfileForm()
        old_img = None

    if request.method == 'GET':
        context = {'profile': p, 'p': profile}
        return render(request, "blog/profile.html", context)
    else:
        p = ProfileForm(request.POST, request.FILES, instance=profile)
        if p.is_valid():
            # if model has = user = models.OneToOneField(User, on_delete=models.CASCADE)
            profile = p.save(commit=False)  # Don't save to DB yet
            profile.user = g_user # Set the user field manually
            
            # delete old image if different
            if old_img and 'profile' in request.FILES:
                # if os.path.isfile(old_img):
                if os.path.exists(old_img):
                    os.remove(old_img)

            profile.save() # Now save
        return redirect("blog:profile", g_user.username)

def read(request, article_id, article_title):
    article = Article.objects.get(pk=article_id)
    
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        agent = request.META.get('HTTP_USER_AGENT')
        article = Article.objects.get(pk=article_id)
        user_comment = request.POST['comment']
    
        post_comment = Comment(
            articles=article, user=request.user, comment=user_comment, user_agent=agent, ip_address=ip,
            )
        post_comment.save()
        return redirect("blog:read", article_id=article_id, article_title=article_title)

    article_text = get_object_or_404(Article, pk=article_id, title=article_title)
    articles = Article.objects.all()[:5]
    comment = Comment.objects.filter(articles=article)[:5]
    context = {'article_text': article_text, 'articles': articles, 'comment': comment}
    return render(request, 'blog/read.html', context)

def about(request):
    # img = {}
    
    # x = Article.objects.get(pk=4)
    # try:
    #     x = Article.objects.get(pk=4)
    #     a = get_object_or_404(Click, articles=x, user=request.user)
    # except:
    #     x = Article.objects.get(pk=3)
    #     a = get_object_or_404(Click, articles=x, user=request.user)
    return render(request, 'blog/about.html', {'a': ""})

def category(request):
    return render(request, 'blog/category.html', {})
 
def contact(request):
    return render(request, 'blog/contact.html', {})

def search(request):
    search_text = request.GET.get('search')
    article = Article.objects.filter(title__icontains=search_text)
    pages = Paginator(article, 1)
    pg_number = request.GET.get('page')
    pg_object = pages.get_page(pg_number)
    context = {
        'txt': search_text,
         'pg_object': pg_object,
    }
    return render(request, 'blog/search.html', context)

def signup(request):
    user_form = UserForm()
    if request.method == 'GET':
        return render(request, 'blog/signup.html', {"user": user_form})
    
    if request.method == 'POST':
        password = request.POST['password']
        confirmpwd = request.POST['confirm']

        if password != confirmpwd:
            return render(request, 'blog/signup.html', {"user": user_form, 'msg': 'Incorrect Password'}) 
        
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()

    return HttpResponseRedirect(reverse("blog:index"))
    
def signin(request):
    # logout(reques)
    if request.method == 'GET':
        return render(request, 'blog/signin.html', {})
    
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        return render(request, 'blog/signin.html', {'msg': 'woong username or password'})
    
def logout_user(request):
    messages.success(request, ('log out complete'))
    logout(request)
    return HttpResponseRedirect(reverse("blog:signin"))

def upload(request):
    if request.method == 'GET':
        article_form = ArticleForm()
        return render(request, 'blog/upload.html', {'article_form': article_form})
    else:
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse("blog:index"))
        
def comments(request, article_id):
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        agent = request.META.get('HTTP_USER_AGENT')
        article = Article.objects.get(pk=article_id)
        user_comment = request.POST['comment']
    
        post_comment = Comment(
            articles=article, user=request.user, comment=user_comment, user_agent=agent, ip_address=ip,
            )
        post_comment.save()

@csrf_exempt
def log_time(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        article_id = Article.objects.get(pk=data.get('article_id'))
        time_spent = data.get('time_spent')
        ip = request.META.get('REMOTE_ADDR')
        agent = request.META.get('HTTP_USER_AGENT')

        try:
            check_click = get_object_or_404(Click, articles=article_id, user=request.user)
            # save last ip address and agent used if seen before
            check_click.viewed_time += time_spent
            check_click.ip_address = ip
            check_click.user_agent = agent
            check_click.save()
            return JsonResponse({}, status=204)
        except:
            if request.user.is_authenticated:
                clicks = Click(
                    articles=article_id, user=request.user, user_agent=agent, ip_address=ip, viewed_time=time_spent
                    )
                clicks.save()
                article_id.clicks += 1
                article_id.save()    
            else:
                clicks = Click(
                    articles=article_id, user_agent=agent, ip_address=ip, viewed_time=time_spent
                    )
                clicks.save()
                article_id.clicks += 1
                article_id.save() 
            return JsonResponse({}, status=204)
        else:
            return JsonResponse({'error': 'invalid method'}, status=405)
