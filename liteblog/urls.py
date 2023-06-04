"""
URL configuration for liteblog project.

"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import include, path

from .feeds import LatestPostsFeed, AtomSiteNewsFeed
from .sitemaps import TagSitemap, CategorySitemap, PostSitemap, StaticViewSitemap
from blog.views import frontpage, archive, year_archive
from page.views import kontakt, about, robots_txt

app_name = 'blog'

sitemaps = {'tag': TagSitemap, 'category': CategorySitemap, 'post': PostSitemap, "static": StaticViewSitemap,}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('about.html', about, name='about'),
    path('kontakt.html', kontakt, name='kontakt'),
    path('', include('blog.urls')),
    path('', frontpage, name='frontpage'),
    path('archive/<int:year>/<int:month>/', archive, name='archive'),
    path('archive/<int:year>/', year_archive, name='year_archive'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path('feed/atom/', AtomSiteNewsFeed()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
