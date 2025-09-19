from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
     
class UserAdmin(models.Model):
    usernameAdmin= models.CharField(max_length=100, unique=True)
    passwordAdmin = models.CharField(max_length=100)
    
    def __str__(self):
        return self.usernameAdmin

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
    
    def __str__(self):
        return self.usernameCliente
    
class UserEmpresa(models.Model):
    usernameEmpresa= models.CharField(max_length=100, unique=True)
    passwordEmpresa = models.CharField(max_length=100)