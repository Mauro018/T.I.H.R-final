from django.shortcuts import render

def carpinteria(request):
    return render(request,"Productos/carpinteria.html")

def marroquineria(request):
    return render(request,"Productos/marroquineria.html")

def tapiceria(request):
    return render(request,"Productos/tapiceria.html")

def vidrieria(request):
    return render(request,"Productos/vidrieria.html")

def metaleria(request):
    return render(request,"Productos/metaleria.html")

def ceramica(request):
    return render(request,"Productos/ceramica.html")

# Create your views here.
