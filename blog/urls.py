from xml.etree.ElementInclude import include

from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    path('post/create/', PostCreateView.as_view(), name='post-create'),

    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),

    path('category/<int:pk>/', PostListByCategory.as_view(), name='category_posts'),
    path('hashtag/<int:pk>/', PostListByHashtag.as_view(), name='hashtag_posts'),
]