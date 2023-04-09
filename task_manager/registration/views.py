from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from registration.forms import CustomUserLoginForm
from django.contrib.auth import authenticate,login
from django.views import View

from registration.forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        success_url = reverse_lazy('registration:login')
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(success_url)
        else:
            return render(request, self.template_name, {'form': form})

def index(request):
    return render(request, 'registration/start_page.html')

class LoginView(View):
    def get(self, request):
        form = CustomUserLoginForm()
        return render(request, 'registration/login.html', { 'form': form })
    
    def post(self, request):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page:tasks')
            else:
                form.add_error(None, "Invalid user or username")
        return render(request, 'registration/login.html', { 'form': form })
