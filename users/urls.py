from django.conf.urls import url
from django.contrib.auth.views import logout_then_login

from .views import UserCreateView, LoginView

urlpatterns = [
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
]
