from django.shortcuts import render, redirect
from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, Idea
from core.forms import IdeaForm

# Create your views here.

def Dasboard_view(request):
    return render(request,'Empresas/dashboardEmpresa.html')

def GestionarProductos_view(request):
    return render(request,'Empresas/GestiProductos.html')

def Armarios_view2(request):
    armarios = Armarios.objects.all()
    context = {'armarios':armarios}
    return render(request, 'Empresas/GestiProductos.html', context)

def agregar_producto_view2(request):
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
        return redirect('GestiProductos')

    return render(request, 'Empresas/agregar_producto2.html')

def editar_producto_view2(request, producto_id):
    try:
        producto = Armarios.objects.get(id=producto_id)
    except Armarios.DoesNotExist:
        return redirect('GestiProductos')

    if request.method == 'POST':
        producto.nombre3 = request.POST.get('nombre')
        producto.descripcion3 = request.POST.get('descripcion')
        producto.precio3 = request.POST.get('precio')
        if 'imagen' in request.FILES:
            producto.imagen3 = request.FILES['imagen']
        producto.save()
        return redirect('GestiProductos')

    context = {'producto': producto}
    return render(request, 'Empresas/editar_producto2.html', context)

def eliminar_producto_view2(request, producto_id):
    try:
        producto = Armarios.objects.get(id=producto_id)
        producto.delete()
    except Armarios.DoesNotExist:
        pass
    return redirect('GestiProductos')

def listid(request):
    return render(request,'Empresas/listid.html')

def ideas_view2(request):
    """
    Maneja la creación y visualización de ideas usando ModelForm.
    """
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige para evitar el reenvío del formulario
            return redirect('idea')
    else:
        form = IdeaForm()

    # Recupera todas las ideas de la base de datos
    ideas = Idea.objects.all()
    
    # Renderiza la plantilla con el formulario y la lista de ideas
    return render(request, 'Empresas/listid.html', {
        'form': form,
        'ideas': ideas
        })
    
def perfilUsuario_view(request):
    return render(request,'Empresas/listid.html')