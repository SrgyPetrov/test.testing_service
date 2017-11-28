from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    answers = models.ManyToManyField(
        'quizzes.Answer',
        related_name='users',
        verbose_name=_('Answers'),
        through='users.UserAnswer'
    )


class UserAnswer(models.Model):

    user = models.ForeignKey('users.User')
    answer = models.ForeignKey('quizzes.Answer')

    class Meta:
        verbose_name = _('User answer')
        verbose_name_plural = _('User answers')
