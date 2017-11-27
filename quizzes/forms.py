from django.forms import BaseInlineFormSet, ValidationError
from django.utils.translation import ugettext_lazy as _


class AnswerInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data.get('is_valid'):
                return
        raise ValidationError(
            _("Question must have at least one valid answer.")
        )
