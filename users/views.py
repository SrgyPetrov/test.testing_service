from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm


class UserCreateView(CreateView):

    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('quizzes_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginView(BaseLoginView):

    template_name = 'users/login.html'
