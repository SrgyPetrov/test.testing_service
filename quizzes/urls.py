from django.conf.urls import url

from .views import QuizzesListView, QuestionView, QuizResultView


urlpatterns = [
    url(r'^$', QuizzesListView.as_view(), name='quizzes_list'),
    url(r'^quiz/(?P<pk>\d+)/$', QuestionView.as_view(),
        name='quizzes_detail'),
    url(r'^result/(?P<pk>\d+)/$', QuizResultView.as_view(),
        name='quizzes_result'),
]
