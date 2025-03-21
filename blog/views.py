from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.urls import reverse_lazy
from .forms import  CommentForm
from django.contrib import messages
from django.views.decorators.cache import cache_page



# Create your views here.
@method_decorator(cache_page(60 * 5), name='dispatch')
class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']





class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

@method_decorator(cache_page(60 * 5), name='dispatch')
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



class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title_uz', 'title_en', 'text_uz', 'text_en','admin' ,'category', 'photo', 'slug']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Agar foydalanuvchi title_en yoki text_en ni kiritmasa, avtomatik o‘zbek tilidan olish
        if not form.instance.title_en:
            form.instance.title_en = form.instance.title_uz
        if not form.instance.text_en:
            form.instance.text_en = form.instance.text_uz
        cache.delete()

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title_uz', 'title_en', 'text_uz', 'text_en' ,'category', 'photo', 'slug']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')
    cache.clear()

    def test_func(self):
        return self.request.user.is_superuser

class DeletePostView(UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_authenticated


    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.clear()  # Cache ni tozalash
        return response

@method_decorator(cache_page(60 * 5), name='dispatch')
class PostListByCategory(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'])

@method_decorator(cache_page(60 * 5), name='dispatch')
class PostListByHashtag(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(hashtags__id=self.kwargs['pk'])

class SearchView(ListView):
    model = Post
    template_name = 'search_result.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 4

    def normalize_query(self, query):
        # Kiril yozuvini lotin yozuviga o'zgartirish
        transliteration_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j',
            'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        }
        normalized_query = ''.join(transliteration_map.get(char, char) for char in query)
        return normalized_query

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            normalized_query = self.normalize_query(query)  # Normalizatsiya qilish
            # Qidiruvni amalga oshirish
            return Post.objects.filter(
                Q(title__icontains=query) |  # Lotin yozuvidagi qidiruv
                Q(title__icontains=normalized_query)  # Kiril yozuvidagi normalizatsiya qilingan qidiruv
            )
        return Post.objects.none()  # Agar qidiruv so'rovi bo'lmasa, bo'sh queryset qaytaring

