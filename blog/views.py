from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Post, Comment
from django.urls import reverse_lazy
from .forms import  CommentForm
from django.contrib import messages



# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']



class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class BlogView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-date')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, "Fikr bildirish uchun avval tizimga kiring.")
            return redirect('login')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.object
            comment.save()
            messages.success(request, "Sizning kommentariyangiz muvaffaqiyatli qo'shildi!")
            return redirect('post_detail', pk=self.object.pk)

        messages.error(request, "Iltimos, to'g'ri ma'lumot kiriting.")
        return self.get(request, *args, **kwargs)



class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['category', 'title', 'text', 'admin', 'comment_count', 'hashtags', 'photo', ]
    success_url = reverse_lazy('home')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'comment_count', 'hashtags', 'photo', ]
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')

class PostListByCategory(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'])

class PostListByHashtag(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(hashtags__id=self.kwargs['pk'])

