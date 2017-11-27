from django.conf.urls import url

from .views import QuizzesListView


urlpatterns = [
    url(r'^$', QuizzesListView.as_view(), name='quizzes_list'),
]
