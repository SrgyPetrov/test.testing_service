from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin, ProcessFormView

from .forms import QuestionForm
from .models import Question, Quiz


class QuizzesListView(ListView):

    queryset = Quiz.objects.filter(is_active=True)
    paginate_by = 5


class QuestionView(DetailView, ProcessFormView, FormMixin):

    model = Question
    form_class = QuestionForm
    template_name = 'quizzes/quiz_detail.html'

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get(self.pk_url_kwarg)
        user_answers = user.answers.filter(question__quiz_id=pk)
        qs = self.model.objects.filter(quiz_id=pk)
        qs = qs.exclude(answers__in=user_answers)
        return qs.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        questions = self.model.objects.filter(quiz_id=pk)
        question_pks = list(questions.values_list('pk', flat=True))
        context['questions_count'] = len(question_pks)
        context['question_number'] = question_pks.index(self.object.pk) + 1
        return context

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse('quizzes_detail', kwargs={'pk': pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        answers = form.cleaned_data['answers']
        self.request.user.answers.add(*answers)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['answers'] = self.object.answers
        return kwargs
