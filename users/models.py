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

    user = models.ForeignKey('users.User', verbose_name=_('User'))
    answer = models.ForeignKey('quizzes.Answer', verbose_name=_('Answer'))

    class Meta:
        verbose_name = _('User answer')
        verbose_name_plural = _('User answers')

    def __str__(self):
        return 'user_id: {}, answer_id: {}'.format(
            self.user_id, self.answer_id
        )
