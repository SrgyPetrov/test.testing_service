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


class QuizAdmin(admin.ModelAdmin):

    list_display = ['title', 'created_at', 'is_active']
    list_editable = ['is_active']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
