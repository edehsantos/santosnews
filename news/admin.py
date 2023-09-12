from django.contrib import admin
from .models import *


@admin.register(News_Category)
class NewsCategory(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 5
    
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'description']    
    list_filter = ['user', 'description']
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['category', 'author', 'title', 'slug', 'created', 'updated', 'published']  
    list_filter = ['category', 'author', 'title', 'slug', 'created', 'updated', 'published']  
    search_fields = ['title', 'publish', 'category']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 5
    ordering = ['status', 'publish']
        
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    
            
            
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    list_filter = ['name', 'email', 'subject', 'message']
                
        