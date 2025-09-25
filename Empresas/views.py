from django.shortcuts import render, redirect
from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios

# Create your views here.

def Dasboard_view(request):
    return render(request,'Empresas/dashboardEmpresa.html')

def GestionarProductos_view(request):
    return render(request,'Empresas/GestiProductos.html')
