from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    answers = models.ManyToManyField('quizzes.Answer', related_name='users',
                                     verbose_name=_('Answers'))
