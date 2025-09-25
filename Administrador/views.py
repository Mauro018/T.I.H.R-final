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

def Sillas_view(request):
    sillas = Sillas.objects.all()
    context = {'sillas':sillas}
    return render(request, 'Administrador/Gproductos.html', context)

def agregar_producto_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')

        nuevo_producto = Armarios(
            nombre3=nombre,
            descripcion3=descripcion,
            precio3=precio,
            imagen3=imagen
        )
        nuevo_producto.save()
        return redirect('Gproductos')

    return render(request, 'Administrador/agregar_producto.html')

def editar_producto_view(request, producto_id):
    try:
        producto = Armarios.objects.get(id=producto_id)
    except Armarios.DoesNotExist:
        return redirect('Gproductos')

    if request.method == 'POST':
        producto.nombre3 = request.POST.get('nombre')
        producto.descripcion3 = request.POST.get('descripcion')
        producto.precio3 = request.POST.get('precio')
        if 'imagen' in request.FILES:
            producto.imagen3 = request.FILES['imagen']
        producto.save()
        return redirect('Gproductos')

    context = {'producto': producto}
    return render(request, 'Administrador/editar_producto.html', context)

def eliminar_producto_view(request, producto_id):
    try:
        producto = Armarios.objects.get(id=producto_id)
        producto.delete()
    except Armarios.DoesNotExist:
        pass
    return redirect('Gproductos')