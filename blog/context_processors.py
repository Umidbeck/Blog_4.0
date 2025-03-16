from django.conf import settings
from .models import Category, Tag, Post

def global_context(request):
    return {
        'posts': Post.objects.all(),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }

def site_info(request):
    return {
        'SITE_NAME':settings.SITE_NAME,
        'SITE_DESCRIPTION':settings.SITE_DESCRIPTION,
    }