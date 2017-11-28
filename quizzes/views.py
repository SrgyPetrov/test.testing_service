from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.detail import (DetailView, SingleObjectMixin,
                                         SingleObjectTemplateResponseMixin)
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.list import ListView

from .forms import QuestionForm
from .models import Quiz
from .utils import get_question_number, get_user_current_question


class QuizzesListView(LoginRequiredMixin, ListView):

    queryset = Quiz.objects.filter(is_active=True)
    paginate_by = 5


class QuestionView(AccessMixin, ProcessFormView, SingleObjectMixin,
                   SingleObjectTemplateResponseMixin, FormMixin):

    form_class = QuestionForm
    template_name = 'quizzes/quiz_question.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        self.object = get_user_current_question(request.user, self.pk)
        if self.object is None:
            return redirect('quizzes_result', pk=self.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_question_number(self.pk, self.object.pk))
        return context

    def form_valid(self, form):
        answers = form.cleaned_data['answers']
        self.request.user.answers.add(*answers)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['answers'] = self.object.answers
        return kwargs

    def get_success_url(self):
        return reverse('quizzes_detail', kwargs={'pk': self.pk})


class QuizResultView(LoginRequiredMixin, DetailView):

    model = Quiz

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if get_user_current_question(request.user, pk) is not None:
            return redirect('quizzes_detail', pk=pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
