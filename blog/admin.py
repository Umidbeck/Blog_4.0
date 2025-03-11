from django.contrib import admin
from .models import Post, Comment, Tag, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # TranslationAdmin ni olib tashladik
    list_display = ('title', 'date')
    prepopulated_fields = {'slug': ('title',)}

    fields = ('category', 'title', 'title_en','text', 'text_en', 'admin', 'hashtags', 'photo', 'slug' )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'date')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
