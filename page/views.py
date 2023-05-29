import sys
import django
import platform
import psutil
from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

def about(request):
    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024) # w megabajtach
    memory_usage = round(memory_usage, 1) # zaokrąglenie do jednego miejsca po przecinku

    context = {
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'page/about.html', context)

def kontakt(request):
    django_version = django.get_version()
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024) # w megabajtach
    memory_usage = round(memory_usage, 1) # zaokrąglenie do jednego miejsca po przecinku

    context = {
        'django_version': django_version,
        'python_version': python_version,
        'memory_usage': memory_usage,
    }

    return render(request, 'page/kontakt.html', context)

def robots_txt(request):
    text = [
        "User-Agent: *",
        "Crawl-delay: 5",
        "Allow: /",
        "Disallow: /admin/",
        "Sitemap: https://dev.liteblog.eu/sitemap.xml",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")
