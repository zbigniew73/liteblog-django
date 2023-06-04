import sys
import django
import platform
import resource
import psutil
import calendar
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import generic
from blog.models import Post, Category, Tag
from collections import defaultdict
from django.db.models import Count
from datetime import datetime

# redis cache
#from django.views.decorators.cache import cache_page
def archive(request, year, month):
    date = datetime(int(year), int(month), 1)
    posts = Post.objects.filter(pub_date__year=year, pub_date__month=month, status=Post.ACTIVE)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
    archive = archive_posts(posts)

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024) # w megabajtach
    memory_usage = round(memory_usage, 1) # zaokrąglenie do jednego miejsca po przecinku

    context = {
        'year': year,
        'month': date.strftime('%B'),
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'archive': archive,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/archive.html', context)

def year_archive(request, year):
    posts = Post.objects.filter(pub_date__year=year)
    archive_list = archive_posts(posts)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024) # w megabajtach
    memory_usage = round(memory_usage, 1) # zaokrąglenie do jednego miejsca po przecinku


    context = {
        'year': year,
        'archive_list': archive_list,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,

    }
    return render(request, 'blog/archive_year.html', context)

def archive_posts(posts):
    archive = defaultdict(int)
    for post in posts:
        year = post.pub_date.year
        month = post.pub_date.month
        archive[(year, month)] += 1

    archive_list = []
    for (year, month), count in archive.items():
        archive_list.append({
            'year': year,
            'month': month,
            'count': count
        })
    return archive_list

# @cache_page(60 * 1)  # Cache na 1 minuta
def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE).order_by('-pub_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
    archive = archive_posts(posts)

    paginator = Paginator(posts, 4)  # Podział na 10 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024) # w megabajtach
    memory_usage = round(memory_usage, 1) # zaokrąglenie do jednego miejsca po przecinku

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'archive': archive,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/frontpage.html', context)

# @cache_page(60 * 1)  # Cache na 1 minuta
def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
        
    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)
    memory_usage = round(memory_usage, 1)

    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/detail.html', context)

# @cache_page(60 * 15)  # Cache na 15 minut
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE).order_by('-pub_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
    archive = archive_posts(posts)

    paginator = Paginator(posts, 4)  # Podział na 5 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)
    memory_usage = round(memory_usage, 1)

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'archive': archive,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/category.html', context)

# @cache_page(60 * 15)  # Cache na 15 minut
def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.post_set.filter(status=Post.ACTIVE).order_by('-pub_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
    archive = archive_posts(posts)

    paginator = Paginator(posts, 4)  # Podział na 5 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)
    memory_usage = round(memory_usage, 1)

    context = {
        'tag': tag,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'archive': archive,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/tag.html', context)

# @cache_page(60 * 1)  # Cache na 1 minuta
def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-pub_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_posts = Post.objects.filter(status='active').order_by('-pub_date')[:9]
    archive = archive_posts(posts)
    
    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)
    memory_usage = round(memory_usage, 1)
    
    context = {
        'posts': posts,
        'query': query,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'archive': archive,
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'blog/search.html', context)
