from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .forms import AnswerInlineFormSet
from .models import Answer, Question, Quiz


class AnswerInline(admin.StackedInline):

    model = Answer
    formset = AnswerInlineFormSet
    min_num = 2
    extra = 0


class QuestionAdmin(SortableAdminMixin, admin.ModelAdmin):

    inlines = [AnswerInline]
    list_filter = ['quiz']
    # list_select_related = ['quiz']


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
