from django.shortcuts import render
from core.models import Armarios, Escritorios, Sillas, Cajoneras, Mesas, Utensilios

def carpinteria(request):
    armarios = Armarios.objects.all()
    context = {'armarios': armarios}
    return render(request, "Productos/carpinteria.html", context)

def marroquineria(request):
    escritorios = Escritorios.objects.all()
    context = {'escritorios': escritorios}
    return render(request, "Productos/marroquineria.html", context)

def tapiceria(request):
    utensilios = Utensilios.objects.all()
    context = {'utensilios': utensilios}
    return render(request, "Productos/tapiceria.html", context)

def vidrieria(request):
    sillas = Sillas.objects.all()
    context = {'sillas': sillas}
    return render(request, "Productos/vidrieria.html", context)

def metaleria(request):
    cajoneras = Cajoneras.objects.all()
    context = {'cajoneras': cajoneras}
    return render(request, "Productos/metaleria.html", context)

def ceramica(request):
    mesas = Mesas.objects.all()
    context = {'mesas': mesas}
    return render(request, "Productos/ceramica.html", context)

# Create your views here.
