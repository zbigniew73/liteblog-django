from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:slug>.html', views.detail, name='post_detail'),
    path('<slug:slug>/', views.category, name='category_detail'),
    path('tag/<slug:slug>/', views.tag, name='tag_detail'),
]
