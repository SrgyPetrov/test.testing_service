from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserCreationForm


class UserCreateView(CreateView):

    form_class = UserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('quizzes')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result
