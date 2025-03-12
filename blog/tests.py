import tempfile
from PIL import Image

from django.contrib.auth.models import User
from django.core.files import temp
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .models import Post, Category, Tag


# Create your tests here.

# Model uchun test

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="test")
        self.user = User.objects.create(username="test")
        self.tag = Tag.objects.create(name="test")
        image = Image.new("RGB", (200, 200))
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(temp_file, format="JPEG")
        temp_file.seek(0)

        self.photo = SimpleUploadedFile('test.jpg', temp_file.read(), content_type="image/jpeg")




    def assertNotContains(self):
        post = Post.objects.create(
            category=self.category,
            title='Post Title',
            text='Post Text',
            slug='post-title',
            admin = self.user,
            photo=self.photo,

        )
        self.assertEqual(post.title, 'Post Title')
        self.assertEqual(post.text, 'Post Text')
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.admin, self.user)

    def test_slug_generation(self):
        post = Post.objects.create(
            category=self.category,
            title='Post Title',
            text='Post Text',
            admin = self.user,
            photo=self.photo,
        )
        self.assertEqual(post.slug, 'post-title')

    def test_photo_resizing(self):
        post = Post.objects.create(
            category=self.category,
            title='Post Title',
            text='Post Text',
            admin = self.user,
            photo=self.photo,
        )
        img = Image.open(post.photo.path)
        self.assertLessEqual(img.width, 200)
        self.assertLessEqual(img.height, 200)



