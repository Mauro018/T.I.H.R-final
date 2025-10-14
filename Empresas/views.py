from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, Idea, UserEmpresa
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

def empresa_ideas_view(request):
    """
    Vista para que las empresas gestionen las ideas.
    """
    # Verificar si hay una sesión activa de empresa
    empresa = None
    if 'usernameEmpresa' in request.session:
        try:
            empresa = UserEmpresa.objects.get(usernameEmpresa=request.session['usernameEmpresa'])
        except UserEmpresa.DoesNotExist:
            return redirect('loginEmpresa')
    else:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')

    # Obtener todas las ideas ordenadas por fecha
    ideas = Idea.objects.all().order_by('-fecha_creacion')
    mensaje = None
    
    if request.method == 'POST':
        idea_id = request.POST.get('idea_id')
        accion = request.POST.get('accion')
        
        if idea_id and accion:
            try:
                idea = Idea.objects.get(pk=idea_id)
                if accion == 'aceptar' and idea.estado == 'pendiente':
                    idea.estado = 'en_proceso'
                    idea.empresa_asignada = empresa
                    idea.save()
                    mensaje = "Idea aceptada exitosamente"
                elif accion == 'completar' and idea.estado == 'en_proceso':
                    if idea.empresa_asignada == empresa:
                        idea.estado = 'completada'
                        idea.save()
                        mensaje = "Idea marcada como completada"
                    else:
                        mensaje = "Error: No tienes permiso para completar esta idea"
            except Idea.DoesNotExist:
                mensaje = "Error: La idea no existe"
    
    # Clasificar las ideas por estado
    ideas_pendientes = ideas.filter(estado='pendiente')
    ideas_en_proceso = ideas.filter(estado='en_proceso')
    ideas_completadas = ideas.filter(estado='completada')
    
    context = {
        'ideas_pendientes': ideas_pendientes,
        'ideas_en_proceso': ideas_en_proceso,
        'ideas_completadas': ideas_completadas,
        'mensaje': mensaje,
        'empresa': empresa
    }
    
    return render(request, 'Empresas/ideas_empresa.html', context)
    
def perfilUsuario_view(request):
    return render(request,'Empresas/listid.html')