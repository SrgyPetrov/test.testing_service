from django import forms
from django.utils.translation import ugettext_lazy as _


class AnswerInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data.get('is_valid'):
                return
        raise forms.ValidationError(
            _("Question must have at least one valid answer.")
        )


class QuestionForm(forms.Form):

    def __init__(self, answers, **kwargs):
        super().__init__(**kwargs)
        self.fields['answers'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=answers
        )
