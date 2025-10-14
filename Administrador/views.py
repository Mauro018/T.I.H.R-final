from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.utils import timezone
from core.models import User, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, UserClientes, UserEmpresa
from django.contrib.auth.decorators import login_required

# Create your views here.

def Dasboard_view(request):
    return render(request,'Administrador/dashboard.html')

@ensure_csrf_cookie
def Usuarios_view(request):
    users = UserClientes.objects.all()
    empresas = UserEmpresa.objects.all()
    context = {
        'users': users,
        'empresas': empresas,
        'csrf_token': get_token(request)
    }
    return render(request,'Administrador/usuarios2.html', context)

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
        return JsonResponse({'success': False}, status=404)

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