from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .models import Category, Tag, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'opisc']
    prepopulated_fields = {'slug': ('title',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'opist']
    prepopulated_fields = {'slug': ('title',)}

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'body']
    list_display = ['title', 'slug', 'category', 'pub_date', 'status', 'display_image']
    list_filter = ['category', 'pub_date', 'status']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['clone_posts']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="100" />', obj.image.url)
        else:
            return None
    display_image.short_description = 'Image'

    def clone_posts(self, request, queryset):
        for post in queryset:
            post.pk = None  # reset primary key to create a new instance
            post.title += ' (Clone)'
            post.save()
        self.message_user(request, "Posty zostały sklonowane.")

    clone_posts.short_description = "Sklonuj wybrane posty"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.site_header = 'Administracja LiteBlog-Django'
