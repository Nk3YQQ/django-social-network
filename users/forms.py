from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterView(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "birthday_date", "gender", "password1", "password2")
        widgets = {
            'birthday_date': forms.DateInput(attrs={'type': 'date'}),
        }
