from django.views.generic import ListView

from .models import Quiz


class QuizzesListView(ListView):

    model = Quiz
    paginate_by = 9
