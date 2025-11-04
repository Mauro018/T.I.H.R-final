from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Mesas(models.Model):
    nombre1 = models.CharField(max_length=100)
    descripcion1 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio1 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen1 = models.ImageField(upload_to='uploads/productos/')
    
class Sillas(models.Model):
    nombre2 = models.CharField(max_length=100)
    descripcion2 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio2 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen2 = models.ImageField(upload_to='uploads/productos/')
    
class Armarios(models.Model):
    nombre3 = models.CharField(max_length=100)
    descripcion3 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio3 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen3 = models.ImageField(upload_to='uploads/productos/')
    
class Cajoneras(models.Model):
    nombre4 = models.CharField(max_length=100)
    descripcion4 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio4 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen4 = models.ImageField(upload_to='uploads/productos/')
    
class Escritorios(models.Model):
    nombre5 = models.CharField(max_length=100)
    descripcion5 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio5 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen5 = models.ImageField(upload_to='uploads/productos/')
    
class Utensilios(models.Model):
    nombre6 = models.CharField(max_length=100)
    descripcion6 = models.CharField(max_length=250, default='', blank=True,null=True)
    precio6 = models.DecimalField(max_digits=10, decimal_places=2)
    imagen6 = models.ImageField(upload_to='uploads/productos/')

class UserClientes(models.Model):
    usernameCliente = models.CharField(max_length=100, unique=True)
    passwordCliente = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    status_changed_at = models.DateTimeField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='uploads/perfiles/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.is_active != getattr(self, '_original_is_active', True):
            self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)
        self._original_is_active = self.is_active
    
    def __str__(self):
        return self.usernameCliente
    
class UserEmpresa(models.Model):
    usernameEmpresa = models.CharField(max_length=100, unique=True)
    passwordEmpresa = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    status_changed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active != getattr(self, '_original_is_active', True):
            self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)
        self._original_is_active = self.is_active

    def __str__(self):
        return self.usernameEmpresa
    
class Idea(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    ]
    
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250, default='', blank=True, null=True)
    autor = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='uploads/ideas/', blank=True, null=True)
    modelo_3d = models.FileField(upload_to='uploads/ideas/modelos3d/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    empresa_asignada = models.ForeignKey(UserEmpresa, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    usuario = models.ForeignKey(UserClientes, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Comentario de {self.usuario.usernameCliente} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
