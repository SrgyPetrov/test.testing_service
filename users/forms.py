from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm):

    use_required_attribute = False

    class Meta(BaseUserCreationForm.Meta):
        model = User
