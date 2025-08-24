from django.shortcuts import render, redirect
from core.models import User, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios

# Create your views here.

def Dasboard_view(request):
    return render(request,'Administrador/dashboard.html')

def Usuarios_view(request):
    usuarios = User.objects.all()
    context = {'usuarios':usuarios}
    return render(request,'Administrador/usuarios.html', context)

def GestionarUsuarios_view(request):
    return render(request,'Administrador/GestionarUsuarios.html')

def GestionarProductos_view(request):
    return render(request,'Administrador/GestionarProductos.html')

def Armarios_view(request):
    armarios = Armarios.objects.all()
    context = {'armarios':armarios}
    return render(request, 'Administrador/Gproductos.html', context)

def sillas_view(request):
    Productos = Sillas.objects.all()
    context = {'productos':Productos}
    return render(request, 'Administrador/Sillas.html', context)

