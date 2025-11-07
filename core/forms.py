from django import forms
from .models import UserClientes, Idea, Comentario

class LoginForm(forms.Form):
    usernameCliente = forms.CharField(max_length=100)
    passwordCliente = forms.CharField(max_length=100, widget=forms.PasswordInput)

class AgregarForm(forms.ModelForm):
    class Meta:
        model = UserClientes
        fields = ['usernameCliente','passwordCliente']

class LoginFormEmpresa(forms.Form):
    usernameEmpresa = forms.CharField(max_length=100)
    passwordEmpresa = forms.CharField(max_length=100, widget=forms.PasswordInput)

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['titulo', 'descripcion', 'imagen', 'modelo_3d']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'modelo_3d': 'Modelo 3D (.glb)',
        }
        help_texts = {
            'modelo_3d': 'Sube un archivo de modelo 3D en formato .glb',
        }

class IdeaUpdateForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['estado']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe tu comentario aqu�...',
                'class': 'form-control'
            }),
        }
        labels = {
            'contenido': 'Tu comentario',
        }

class PerfilUsuarioForm(forms.ModelForm):
    passwordCliente_actual = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contrase�a actual'}),
        required=False,
        label='Contrase�a actual'
    )
    passwordCliente_nueva = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contrase�a'}),
        required=False,
        label='Nueva contrase�a'
    )
    passwordCliente_confirmar = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contrase�a'}),
        required=False,
        label='Confirmar contrase�a'
    )
    
    class Meta:
        model = UserClientes
        fields = ['usernameCliente', 'email', 'foto_perfil']
        widgets = {
            'usernameCliente': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }
        labels = {
            'usernameCliente': 'Nombre de usuario',
            'email': 'Correo electr�nico',
            'foto_perfil': 'Foto de perfil',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password_actual = cleaned_data.get('passwordCliente_actual')
        password_nueva = cleaned_data.get('passwordCliente_nueva')
        password_confirmar = cleaned_data.get('passwordCliente_confirmar')
        
        if password_nueva or password_confirmar:
            if not password_actual:
                raise forms.ValidationError('Debes ingresar tu contrase�a actual para cambiarla')
            if password_nueva != password_confirmar:
                raise forms.ValidationError('Las contrase�as nuevas no coinciden')
            if len(password_nueva) < 6:
                raise forms.ValidationError('La contrase�a debe tener al menos 6 caracteres')
        
        return cleaned_data
