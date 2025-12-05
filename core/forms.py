from django import forms
from .models import UserClientes, Idea, Comentario
import re
import random

class LoginForm(forms.Form):
    usernameCliente = forms.CharField(max_length=100)
    passwordCliente = forms.CharField(max_length=100, widget=forms.PasswordInput)

class AgregarForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    passwordCliente = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        label='Contraseña',
        help_text='Mínimo 8 caracteres'
    )
    
    class Meta:
        model = UserClientes
        fields = ['usernameCliente', 'email', 'passwordCliente']
    
    def clean_usernameCliente(self):
        username = self.cleaned_data.get('usernameCliente')
        
        # Validar que solo contenga letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('El nombre de usuario solo puede contener letras, números y guiones bajos')
        
        # Verificar si el username ya existe
        if UserClientes.objects.filter(usernameCliente=username).exists():
            # Generar sugerencias de nombres disponibles
            sugerencias = []
            for i in range(3):
                numero = random.randint(1, 999)
                sugerencia = f"{username}{numero}"
                if not UserClientes.objects.filter(usernameCliente=sugerencia).exists():
                    sugerencias.append(sugerencia)
            
            # Agregar sugerencias con guiones bajos
            for sufijo in ['_user', '_01', '_pro']:
                sugerencia = f"{username}{sufijo}"
                if not UserClientes.objects.filter(usernameCliente=sugerencia).exists() and len(sugerencias) < 5:
                    sugerencias.append(sugerencia)
            
            mensaje = f'Nombre de usuario ya existente. Sugerencias disponibles: {", ".join(sugerencias)}'
            raise forms.ValidationError(mensaje)
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Validar formato de Gmail
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Solo se permiten correos de Gmail (@gmail.com)')
        
        # Verificar si el email ya existe en la base de datos
        if UserClientes.objects.filter(email=email).exists():
            raise forms.ValidationError('Correo ya utilizado. Por favor, utiliza otro correo electrónico.')
        
        # Verificar si el email existe en Gmail usando DNS
        try:
            from dns import resolver # type: ignore
            import re
            
            # Extraer el dominio
            domain = email.split('@')[1]
            
            # Verificar registros MX del dominio
            try:
                mx_records = resolver.resolve(domain, 'MX')
                if not mx_records:
                    raise forms.ValidationError('El dominio del correo no es válido.')
            except:
                raise forms.ValidationError('No se pudo verificar el correo. Asegúrate de que sea un correo de Gmail válido.')
            
            # Validación adicional del formato del email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
            if not re.match(email_pattern, email):
                raise forms.ValidationError('Formato de correo inválido.')
                
        except ImportError:
            # Si no está disponible la librería DNS, solo hacer validación básica
            pass
        
        return email
    
    def clean_passwordCliente(self):
        password = self.cleaned_data.get('passwordCliente')
        
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        return password

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
