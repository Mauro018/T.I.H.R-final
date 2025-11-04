from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.utils import timezone
from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, Idea, UserEmpresa, UserClientes
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

def ver_imagen_idea(request, idea_id):
    """
    Vista para que las empresas vean la imagen de una idea.
    """
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    idea = get_object_or_404(Idea, pk=idea_id)
    
    context = {
        'idea': idea
    }
    
    return render(request, 'Empresas/ver_imagen_idea.html', context)

def ver_modelo_3d_idea(request, idea_id):
    """
    Vista para que las empresas vean el modelo 3D de una idea.
    """
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    idea = get_object_or_404(Idea, pk=idea_id)
    
    context = {
        'idea': idea
    }
    
    return render(request, 'Empresas/ver_modelo_3d_idea.html', context)

@ensure_csrf_cookie
def usuarios_view(request):
    """
    Vista para gestión de usuarios (clientes y empresas)
    """
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    users = UserClientes.objects.all()
    empresas = UserEmpresa.objects.all()
    context = {
        'users': users,
        'empresas': empresas,
        'csrf_token': get_token(request)
    }
    return render(request,'Empresas/usuarios2.html', context)

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@require_POST
def toggle_user_status(request, user_id, user_type, action):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    if action not in ['enable', 'disable']:
        return JsonResponse({'success': False, 'error': 'Acción inválida'}, status=400)
        
    try:
        if user_type == 'cliente':
            user = UserClientes.objects.get(id=user_id)
        elif user_type == 'empresa':
            user = UserEmpresa.objects.get(id=user_id)
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de usuario inválido'}, status=400)
            
        # Actualizar el estado
        new_status = action == 'enable'
        if user.is_active == new_status:
            return JsonResponse({'success': False, 'error': 'El usuario ya está en ese estado'}, status=400)
            
        user.is_active = new_status
        user.status_changed_at = timezone.now()
        user.save()
        
        return JsonResponse({
            'success': True,
            'status': 'Activo' if user.is_active else 'Inactivo',
            'action': 'disable' if user.is_active else 'enable'
        })
    except (UserClientes.DoesNotExist, UserEmpresa.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def update_user(request):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
        
    try:
        user_id = request.POST.get('userId')
        user_type = request.POST.get('userType')
        username = request.POST.get('username')
        
        if not user_id or not user_type or not username:
            return JsonResponse({'success': False, 'error': 'Faltan datos requeridos'}, status=400)
        
        if user_type == 'cliente':
            user = UserClientes.objects.get(id=user_id)
            # Verificar si el nombre de usuario ya existe
            if UserClientes.objects.filter(usernameCliente=username).exclude(id=user_id).exists():
                return JsonResponse({'success': False, 'error': 'El nombre de usuario ya está en uso'}, status=400)
            
            # Validar email
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'success': False, 'error': 'El email es requerido'}, status=400)
                
            user.usernameCliente = username
            user.email = email
        elif user_type == 'empresa':
            user = UserEmpresa.objects.get(id=user_id)
            # Verificar si el nombre de usuario ya existe
            if UserEmpresa.objects.filter(usernameEmpresa=username).exclude(id=user_id).exists():
                return JsonResponse({'success': False, 'error': 'El nombre de usuario ya está en uso'}, status=400)
            user.usernameEmpresa = username
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de usuario inválido'}, status=400)
            
        user.save()
        return JsonResponse({
            'success': True,
            'message': 'Usuario actualizado correctamente',
            'data': {
                'id': user.id,
                'username': username,
                'email': getattr(user, 'email', None),
                'type': user_type,
                'is_active': user.is_active
            }
        })
    except (UserClientes.DoesNotExist, UserEmpresa.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)