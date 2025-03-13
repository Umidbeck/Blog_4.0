from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out, user_logged_in
from .models import Post

@receiver(post_save, sender=Post)
@receiver(pre_delete, sender=Post)
def clear_post_cache(sender, **kwargs):
    print("Cache tozalanmoqda...")
    cache.delete("all_posts")


@receiver(user_logged_in)
def user_logged_in(sender,request, user, **kwargs):
    print("User logged in...")
    cache.clear()

@receiver(user_logged_out)
def user_logged_out(sender,request, user, **kwargs):
    print("User logged out...")
    cache.clear()