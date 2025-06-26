from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
        max_length=30,
        required=True,
        help_text="Ingrese su nombre.",
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su pellido"}),
        max_length=30,
        required=True,
        help_text="Ingrese su apellido.",
    )
    email = forms.EmailField(required=True, help_text="Ingrese su correo electrónico.")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text="Confirme su contraseña.",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )
        labels = {
            "username": "Nombre de usuario",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["primer_nombre"]
        user.last_name = self.cleaned_data["segundo_nombre"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
