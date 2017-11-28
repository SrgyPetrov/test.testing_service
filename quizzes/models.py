import textwrap

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Quiz(models.Model):

    title = models.CharField(_('Title'), max_length=192)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Is active?'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quizzes_detail', args=[self.pk])


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, verbose_name=_('Quiz'),
                             related_name='questions')
    text = models.TextField(_('Text'))
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['order']

    def __str__(self):
        return textwrap.shorten(self.text, width=100, placeholder="...")


class Answer(models.Model):

    question = models.ForeignKey(Question, verbose_name=_('Question'),
                                 related_name='answers')
    text = models.CharField(_('Text'), max_length=255)
    is_valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return textwrap.shorten(self.text, width=100, placeholder="...")
