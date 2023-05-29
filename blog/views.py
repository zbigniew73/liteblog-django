import sys
import django
import platform
import resource
import psutil
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import generic
from blog.models import Post, Category, Tag

# redis cache
# from django.views.decorators.cache import cache_page

# @cache_page(60 * 1)  # Cache na 1 minuta
def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE).order_by('-pub_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()

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

    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)
    memory_usage = round(memory_usage, 1)

    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
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

    return render(request, 'blog/search.html', {'posts': posts, 'query': query, 'categories': categories, 'tags': tags})
