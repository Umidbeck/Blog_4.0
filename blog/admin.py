from django.contrib import admin
from .models import Post, Comment, Tag, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # TranslationAdmin ni olib tashladik
    list_display = ('title_en', 'date')
    prepopulated_fields = {'slug': ('title_uz',)}
    exclude = ('title', 'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'date')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
