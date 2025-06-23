from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView,ListView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.views import View
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import LoginForm
from user.models import Profile
import logging
from .forms import ProfileForm,CombinedProfileForm


logger = logging.getLogger(__name__)

def create_user(request):
    user = User.objects.create_user(username='test', password='test',email='test@mail.com')
    return HttpResponse(f'Пользователь создан {user.username} ')

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('home')




class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

''' Допилить обновлять можно только свой профиль'''
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = CombinedProfileForm
    template_name = 'user/profile_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('user_list')
'''Доделывать вроде не надо'''
class ProfileView(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, user__id=pk)
        return render(request, 'user/profile.html', {'profile': profile})



class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user/profile_detail.html'
    context_object_name = 'profile'

'''Допилить ссылки на профили'''
class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'



# Create your views here.
