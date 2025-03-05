from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm


# **1. Ro‘yxatdan o‘tish (Signup) - CreateView yordamida**
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Ro‘yxatdan o‘tgan userni avtomatik login qilish
        messages.success(self.request, "Account created successfully!")
        return redirect('home')


# **2. Login - FormView yordamida**
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Login successful!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)


# **3. Logout - Oddiy View yordamida**
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('login')
