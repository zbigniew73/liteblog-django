from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.contrib import sitemaps
from django.urls import reverse

from blog.models import Category, Post, Tag

class TagSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Tag.objects.all()

class CategorySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()

class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(status=Post.ACTIVE)

    def lastmod(self, obj):
        return obj.pub_date

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = "daily"

    def items(self):
        return ["frontpage", "about", "kontakt"]

    def location(self, item):
        return reverse(item)
