from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = RichTextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    photo = models.ImageField(upload_to='media/photos/%Y/%m/%d')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Slugni faqat birinchi saqlashda yaratish
        if not self.slug:
            self.slug = slugify(self.title)

        # Birinchi save() chaqiriladi
        super().save(*args, **kwargs)

        # Rasmni ochish va kichraytirish
        img = Image.open(self.photo.path)
        if img.width > 800 or img.height > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.photo.path)  # O'zgarishni saqlash

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

