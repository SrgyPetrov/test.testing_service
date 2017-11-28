from django.conf.urls import url

from .views import QuizzesListView, QuestionView


urlpatterns = [
    url(r'^$', QuizzesListView.as_view(), name='quizzes_list'),
    url(r'^quiz/(?P<pk>\d+)/$', QuestionView.as_view(),
        name='quizzes_detail'),
]
