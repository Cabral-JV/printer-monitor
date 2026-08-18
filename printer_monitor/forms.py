from django import forms
from .models import Printer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ["setor", "ip", "numero_serie", "status", "data_remaining"]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_superuser"]


class CustomUserChangeForm(UserChangeForm):
    password = None  # remove o campo de senha (edição de senha é feita à parte)

    class Meta:
        model = User
        fields = ["username", "email", "is_superuser", "is_active"]
