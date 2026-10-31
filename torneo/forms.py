from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroCapitanForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono de Contacto")
    comuna = forms.CharField(max_length=50, required=True, label="Comuna o Ciudad")

    class Meta:
        model = User
        fields = ['username', 'email']