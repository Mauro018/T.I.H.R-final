from django import forms
from .models import UserClientes

class LoginForm(forms.Form):
    usernameCliente = forms.CharField(max_length=100)
    passwordCliente = forms.CharField(max_length=100, widget=forms.PasswordInput)
    
class LoginFormAdmin(forms.Form):
    usernameAdmin = forms.CharField(max_length=100)
    passwordAdmin = forms.CharField(max_length=100, widget=forms.PasswordInput)
    

class AgregarForm(forms.ModelForm):
    class Meta:
        model = UserClientes
        fields = ['usernameCliente','passwordCliente']

class LoginFormEmpresa(forms.Form):
    usernameEmpresa = forms.CharField(max_length=100)
    passwordEmpresa = forms.CharField(max_length=100, widget=forms.PasswordInput)