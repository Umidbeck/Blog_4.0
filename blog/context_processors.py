from .models import Category, Tag, Post

def global_context(request):
    return {
        'posts': Post.objects.all(),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }