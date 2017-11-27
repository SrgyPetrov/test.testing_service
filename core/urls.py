import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'', include('quizzes.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve, {
            'document_root': os.path.join(
                settings.BASE_DIR, 'core/static'
            )
        }),
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]
