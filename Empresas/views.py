from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.utils import timezone
from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, Idea, UserEmpresa, UserClientes, Pago, Pedido
from core.forms import IdeaForm
import json

# Importar vistas adicionales
from .views_estadisticas import estadisticas_view, inventario_view, actualizar_inventario_view

# Create your views here.

def Dasboard_view(request):
    return render(request,'Empresas/dashboardEmpresa.html')

def GestionarProductos_view(request):
    # Obtener todos los productos de todas las categorías
    mesas = Mesas.objects.all()
    sillas = Sillas.objects.all()
    armarios = Armarios.objects.all()
    cajoneras = Cajoneras.objects.all()
    escritorios = Escritorios.objects.all()
    utensilios = Utensilios.objects.all()
    
    context = {
        'mesas': mesas,
        'sillas': sillas,
        'armarios': armarios,
        'cajoneras': cajoneras,
        'escritorios': escritorios,
        'utensilios': utensilios,
    }
    return render(request, 'Empresas/GestiProductos.html', context)

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
        categoria = request.POST.get('categoria')

        # Guardar el producto en el modelo correspondiente según la categoría
        if categoria == 'mesas':
            nuevo_producto = Mesas(
                nombre1=nombre,
                descripcion1=descripcion,
                precio1=precio,
                imagen1=imagen
            )
        elif categoria == 'sillas':
            nuevo_producto = Sillas(
                nombre2=nombre,
                descripcion2=descripcion,
                precio2=precio,
                imagen2=imagen
            )
        elif categoria == 'armarios':
            nuevo_producto = Armarios(
                nombre3=nombre,
                descripcion3=descripcion,
                precio3=precio,
                imagen3=imagen
            )
        elif categoria == 'cajoneras':
            nuevo_producto = Cajoneras(
                nombre4=nombre,
                descripcion4=descripcion,
                precio4=precio,
                imagen4=imagen
            )
        elif categoria == 'escritorios':
            nuevo_producto = Escritorios(
                nombre5=nombre,
                descripcion5=descripcion,
                precio5=precio,
                imagen5=imagen
            )
        elif categoria == 'utensilios':
            nuevo_producto = Utensilios(
                nombre6=nombre,
                descripcion6=descripcion,
                precio6=precio,
                imagen6=imagen
            )
        else:
            messages.error(request, 'Categoría no válida')
            return render(request, 'Empresas/agregar_producto2.html')
        
        nuevo_producto.save()
        messages.success(request, 'Producto agregado exitosamente')
        return redirect('GestiProductos')

    return render(request, 'Empresas/agregar_producto2.html')

def editar_producto_view2(request, categoria, producto_id):
    # Obtener el producto según la categoría
    producto = None
    modelo = None
    
    if categoria == 'mesas':
        modelo = Mesas
        try:
            producto = Mesas.objects.get(id=producto_id)
        except Mesas.DoesNotExist:
            return redirect('GestiProductos')
    elif categoria == 'sillas':
        modelo = Sillas
        try:
            producto = Sillas.objects.get(id=producto_id)
        except Sillas.DoesNotExist:
            return redirect('GestiProductos')
    elif categoria == 'armarios':
        modelo = Armarios
        try:
            producto = Armarios.objects.get(id=producto_id)
        except Armarios.DoesNotExist:
            return redirect('GestiProductos')
    elif categoria == 'cajoneras':
        modelo = Cajoneras
        try:
            producto = Cajoneras.objects.get(id=producto_id)
        except Cajoneras.DoesNotExist:
            return redirect('GestiProductos')
    elif categoria == 'escritorios':
        modelo = Escritorios
        try:
            producto = Escritorios.objects.get(id=producto_id)
        except Escritorios.DoesNotExist:
            return redirect('GestiProductos')
    elif categoria == 'utensilios':
        modelo = Utensilios
        try:
            producto = Utensilios.objects.get(id=producto_id)
        except Utensilios.DoesNotExist:
            return redirect('GestiProductos')
    else:
        return redirect('GestiProductos')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        
        # Actualizar según la categoría
        if categoria == 'mesas':
            producto.nombre1 = nombre
            producto.descripcion1 = descripcion
            producto.precio1 = precio
            if 'imagen' in request.FILES:
                producto.imagen1 = request.FILES['imagen']
        elif categoria == 'sillas':
            producto.nombre2 = nombre
            producto.descripcion2 = descripcion
            producto.precio2 = precio
            if 'imagen' in request.FILES:
                producto.imagen2 = request.FILES['imagen']
        elif categoria == 'armarios':
            producto.nombre3 = nombre
            producto.descripcion3 = descripcion
            producto.precio3 = precio
            if 'imagen' in request.FILES:
                producto.imagen3 = request.FILES['imagen']
        elif categoria == 'cajoneras':
            producto.nombre4 = nombre
            producto.descripcion4 = descripcion
            producto.precio4 = precio
            if 'imagen' in request.FILES:
                producto.imagen4 = request.FILES['imagen']
        elif categoria == 'escritorios':
            producto.nombre5 = nombre
            producto.descripcion5 = descripcion
            producto.precio5 = precio
            if 'imagen' in request.FILES:
                producto.imagen5 = request.FILES['imagen']
        elif categoria == 'utensilios':
            producto.nombre6 = nombre
            producto.descripcion6 = descripcion
            producto.precio6 = precio
            if 'imagen' in request.FILES:
                producto.imagen6 = request.FILES['imagen']
        
        producto.save()
        messages.success(request, 'Producto actualizado exitosamente')
        return redirect('GestiProductos')

    context = {
        'producto': producto,
        'categoria': categoria
    }
    return render(request, 'Empresas/editar_producto2.html', context)

def eliminar_producto_view2(request, categoria, producto_id):
    # Eliminar el producto según la categoría
    try:
        if categoria == 'mesas':
            producto = Mesas.objects.get(id=producto_id)
        elif categoria == 'sillas':
            producto = Sillas.objects.get(id=producto_id)
        elif categoria == 'armarios':
            producto = Armarios.objects.get(id=producto_id)
        elif categoria == 'cajoneras':
            producto = Cajoneras.objects.get(id=producto_id)
        elif categoria == 'escritorios':
            producto = Escritorios.objects.get(id=producto_id)
        elif categoria == 'utensilios':
            producto = Utensilios.objects.get(id=producto_id)
        else:
            return redirect('GestiProductos')
        
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
    except:
        messages.error(request, 'Error al eliminar el producto')
    
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
                elif accion == 'finalizar' and idea.estado == 'completada':
                    if idea.empresa_asignada == empresa:
                        idea.estado = 'finalizada'
                        idea.save()
                        mensaje = "Idea marcada como finalizada"
                    else:
                        mensaje = "Error: No tienes permiso para finalizar esta idea"
            except Idea.DoesNotExist:
                mensaje = "Error: La idea no existe"
    
    # Clasificar las ideas por estado
    ideas_pendientes = ideas.filter(estado='pendiente')
    ideas_en_proceso = ideas.filter(estado='en_proceso')
    ideas_completadas = ideas.filter(estado='completada')
    ideas_finalizadas = ideas.filter(estado='finalizada')
    
    context = {
        'ideas_pendientes': ideas_pendientes,
        'ideas_en_proceso': ideas_en_proceso,
        'ideas_completadas': ideas_completadas,
        'ideas_finalizadas': ideas_finalizadas,
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

def gestion_pedidos_view(request):
    """Vista para gestión de pedidos por parte de la empresa"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    # Obtener todos los pedidos ordenados por fecha
    pedidos = Pedido.objects.all().select_related('cliente', 'pago').order_by('-fecha_creacion')
    
    # Parsear JSON de productos para cada pedido
    for pedido in pedidos:
        try:
            pedido.productos_parseados = json.loads(pedido.productos)
        except:
            pedido.productos_parseados = []
    
    context = {
        'pedidos': pedidos,
    }
    
    return render(request, 'Empresas/gestion_pedidos.html', context)

@require_POST
def actualizar_estado_pedido_view(request, pedido_id):
    """Vista para actualizar el estado de un pedido"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        numero_seguimiento = request.POST.get('numero_seguimiento', '')
        empresa_envio = request.POST.get('empresa_envio', '')
        
        # Validar estado
        estados_validos = ['procesando', 'empacado', 'enviado', 'en_transito', 'entregado', 'cancelado']
        if nuevo_estado not in estados_validos:
            return JsonResponse({'success': False, 'error': 'Estado no válido'}, status=400)
        
        pedido.estado = nuevo_estado
        
        if numero_seguimiento:
            pedido.numero_seguimiento = numero_seguimiento
        if empresa_envio:
            pedido.empresa_envio = empresa_envio
        
        # Si se marca como entregado, guardar fecha
        if nuevo_estado == 'entregado' and not pedido.fecha_entrega_real:
            pedido.fecha_entrega_real = timezone.now()
        
        pedido.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Estado del pedido actualizado'
        })
        
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def gestion_pagos_view(request):
    """Vista para gestión de pagos por parte de la empresa"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    # Obtener todos los pagos ordenados por fecha
    pagos = Pago.objects.all().select_related('cliente').order_by('-fecha_creacion')
    
    # Parsear JSON de productos para cada pago
    for pago in pagos:
        try:
            pago.productos_parseados = json.loads(pago.productos)
        except:
            pago.productos_parseados = []
    
    # Clasificar pagos por estado
    pagos_pendientes = pagos.filter(estado='pendiente')
    pagos_confirmados = pagos.filter(estado='confirmado')
    pagos_rechazados = pagos.filter(estado='rechazado')
    
    context = {
        'pagos_pendientes': pagos_pendientes,
        'pagos_confirmados': pagos_confirmados,
        'pagos_rechazados': pagos_rechazados,
    }
    
    return render(request, 'Empresas/gestion_pagos.html', context)

@require_POST
def confirmar_pago_view(request, pago_id):
    """Vista para confirmar un pago y crear pedido automáticamente"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        from core.models import Pedido
        from datetime import timedelta
        
        pago = Pago.objects.get(id=pago_id)
        pago.estado = 'confirmado'
        pago.fecha_confirmacion = timezone.now()
        
        # Obtener notas opcionales
        notas = request.POST.get('notas', '')
        if notas:
            pago.notas_empresa = notas
        
        pago.save()
        
        # Verificar si ya existe un pedido para este pago
        if not hasattr(pago, 'pedido'):
            # Crear el pedido SIN datos de envío (el cliente los completará después)
            pedido = Pedido.objects.create(
                pago=pago,
                cliente=pago.cliente,
                productos=pago.productos,
                monto_total=pago.monto_total,
                estado='procesando',
                fecha_entrega_estimada=timezone.now().date() + timedelta(days=7)
            )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Pago confirmado y pedido creado. El cliente debe completar sus datos de envío.'
        })
        
    except Pago.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pago no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def rechazar_pago_view(request, pago_id):
    """Vista para rechazar un pago"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        pago = Pago.objects.get(id=pago_id)
        pago.estado = 'rechazado'
        
        # Obtener notas obligatorias al rechazar
        notas = request.POST.get('notas', '')
        if not notas:
            return JsonResponse({'success': False, 'error': 'Debes proporcionar una razón para rechazar el pago'}, status=400)
        
        pago.notas_empresa = notas
        pago.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Pago rechazado'
        })
        
    except Pago.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pago no encontrado'}, status=404)
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

# La función estadisticas_view se importa desde views_estadisticas.py
# No debe estar duplicada aquí

@require_POST
def contactar_usuario_idea(request, idea_id):
    """Vista para que la empresa contacte al usuario sobre la idea"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        empresa = UserEmpresa.objects.get(usernameEmpresa=request.session['usernameEmpresa'])
        idea = Idea.objects.get(id=idea_id)
        
        # Verificar que la empresa es la asignada
        if idea.empresa_asignada != empresa:
            return JsonResponse({'success': False, 'error': 'No tienes permiso para contactar sobre esta idea'}, status=403)
        
        mensaje = request.POST.get('mensaje', '')
        if not mensaje:
            return JsonResponse({'success': False, 'error': 'Debes escribir un mensaje'}, status=400)
        
        idea.mensaje_empresa = mensaje
        idea.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Mensaje enviado al usuario exitosamente'
        })
        
    except Idea.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Idea no encontrada'}, status=404)
    except UserEmpresa.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Empresa no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def solicitar_permiso_publicacion(request, idea_id):
    """Vista para que la empresa solicite permiso para publicar la idea"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        empresa = UserEmpresa.objects.get(usernameEmpresa=request.session['usernameEmpresa'])
        idea = Idea.objects.get(id=idea_id)
        
        # Verificar que la empresa es la asignada y la idea está finalizada
        if idea.empresa_asignada != empresa:
            return JsonResponse({'success': False, 'error': 'No tienes permiso sobre esta idea'}, status=403)
        
        if idea.estado != 'finalizada':
            return JsonResponse({'success': False, 'error': 'La idea debe estar finalizada'}, status=400)
        
        mensaje = request.POST.get('mensaje', '')
        if not mensaje:
            return JsonResponse({'success': False, 'error': 'Debes escribir un mensaje de solicitud'}, status=400)
        
        idea.mensaje_empresa = mensaje
        idea.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Solicitud de permiso enviada al usuario'
        })
        
    except Idea.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Idea no encontrada'}, status=404)
    except UserEmpresa.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Empresa no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def publicar_idea_como_producto(request, idea_id):
    """Vista para publicar una idea como producto"""
    # Verificar si hay una sesión activa de empresa
    if 'usernameEmpresa' not in request.session:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    try:
        empresa = UserEmpresa.objects.get(usernameEmpresa=request.session['usernameEmpresa'])
        idea = Idea.objects.get(id=idea_id)
        
        # Verificar permisos
        if idea.empresa_asignada != empresa:
            messages.error(request, 'No tienes permiso sobre esta idea')
            return redirect('empresa_ideas')
        
        if not idea.permiso_publicacion:
            messages.error(request, 'No tienes permiso del usuario para publicar esta idea')
            return redirect('empresa_ideas')
        
        if idea.publicada_como_producto:
            messages.warning(request, 'Esta idea ya fue publicada como producto')
            return redirect('empresa_ideas')
        
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            cantidad = request.POST.get('cantidad', 0)
            categoria = request.POST.get('categoria')
            
            if not all([nombre, descripcion, precio, categoria]):
                messages.error(request, 'Todos los campos son obligatorios')
                return render(request, 'Empresas/publicar_idea_producto.html', {'idea': idea})
            
            # Crear el producto según la categoría seleccionada
            try:
                if categoria == 'mesas':
                    producto = Mesas.objects.create(
                        nombre1=nombre,
                        descripcion1=descripcion,
                        precio1=precio,
                        imagen1=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                elif categoria == 'sillas':
                    producto = Sillas.objects.create(
                        nombre2=nombre,
                        descripcion2=descripcion,
                        precio2=precio,
                        imagen2=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                elif categoria == 'armarios':
                    producto = Armarios.objects.create(
                        nombre3=nombre,
                        descripcion3=descripcion,
                        precio3=precio,
                        imagen3=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                elif categoria == 'cajoneras':
                    producto = Cajoneras.objects.create(
                        nombre4=nombre,
                        descripcion4=descripcion,
                        precio4=precio,
                        imagen4=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                elif categoria == 'escritorios':
                    producto = Escritorios.objects.create(
                        nombre5=nombre,
                        descripcion5=descripcion,
                        precio5=precio,
                        imagen5=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                elif categoria == 'utensilios':
                    producto = Utensilios.objects.create(
                        nombre6=nombre,
                        descripcion6=descripcion,
                        precio6=precio,
                        imagen6=idea.imagen if idea.imagen else None,
                        cantidad_disponible=int(cantidad)
                    )
                else:
                    messages.error(request, 'Categoría no válida')
                    return render(request, 'Empresas/publicar_idea_producto.html', {'idea': idea})
                
                # Marcar la idea como publicada
                idea.publicada_como_producto = True
                idea.fecha_publicacion = timezone.now()
                idea.save()
                
                messages.success(request, f'¡Idea publicada exitosamente como producto en la categoría {categoria}!')
                return redirect('GestiProductos')
                
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
                return render(request, 'Empresas/publicar_idea_producto.html', {'idea': idea})
        
        return render(request, 'Empresas/publicar_idea_producto.html', {'idea': idea})
        
    except Idea.DoesNotExist:
        messages.error(request, 'Idea no encontrada')
        return redirect('empresa_ideas')
    except UserEmpresa.DoesNotExist:
        messages.error(request, 'Empresa no encontrada')
        return redirect('loginEmpresa')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('empresa_ideas')


