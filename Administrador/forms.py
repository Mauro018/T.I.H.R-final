from django import forms
from core.models import UserClientes

class AgregarForm(forms.ModelForm):
    class Meta:
        model = UserClientes
        fields = ['usernameCliente','passwordCliente', 'email']