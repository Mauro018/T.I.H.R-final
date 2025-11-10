from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.models import UserClientes, Pedido, Pago, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios
from django.db.models import Sum, Count, Q

def estadisticas_view(request):
    """Vista para mostrar estadísticas de la empresa"""
    if 'usernameEmpresa' not in request.session:
        return redirect('loginEmpresa')
    
    # Estadísticas de usuarios
    total_usuarios = UserClientes.objects.count()
    usuarios_activos = UserClientes.objects.filter(is_active=True).count()
    
    # Estadísticas de productos
    total_mesas = Mesas.objects.count()
    total_sillas = Sillas.objects.count()
    total_armarios = Armarios.objects.count()
    total_cajoneras = Cajoneras.objects.count()
    total_escritorios = Escritorios.objects.count()
    total_utensilios = Utensilios.objects.count()
    total_productos = total_mesas + total_sillas + total_armarios + total_cajoneras + total_escritorios + total_utensilios
    
    # Estadísticas de pedidos
    total_pedidos = Pedido.objects.count()
    pedidos_procesando = Pedido.objects.filter(estado='procesando').count()
    pedidos_enviados = Pedido.objects.filter(Q(estado='enviado') | Q(estado='en_transito')).count()
    pedidos_entregados = Pedido.objects.filter(estado='entregado').count()
    
    # Estadísticas de pagos
    total_pagos = Pago.objects.count()
    pagos_pendientes = Pago.objects.filter(estado='pendiente').count()
    pagos_confirmados = Pago.objects.filter(estado='confirmado').count()
    pagos_rechazados = Pago.objects.filter(estado='rechazado').count()
    
    # Ingresos totales
    ingresos_totales = Pago.objects.filter(estado='confirmado').aggregate(total=Sum('monto_total'))['total'] or 0
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'total_productos': total_productos,
        'total_mesas': total_mesas,
        'total_sillas': total_sillas,
        'total_armarios': total_armarios,
        'total_cajoneras': total_cajoneras,
        'total_escritorios': total_escritorios,
        'total_utensilios': total_utensilios,
        'total_pedidos': total_pedidos,
        'pedidos_procesando': pedidos_procesando,
        'pedidos_enviados': pedidos_enviados,
        'pedidos_entregados': pedidos_entregados,
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_confirmados': pagos_confirmados,
        'pagos_rechazados': pagos_rechazados,
        'ingresos_totales': ingresos_totales,
    }
    
    return render(request, 'Empresas/estadisticas.html', context)

def inventario_view(request):
    """Vista para gestionar el inventario de productos"""
    if 'usernameEmpresa' not in request.session:
        return redirect('loginEmpresa')
    
    # Obtener todos los productos
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
    
    return render(request, 'Empresas/inventario.html', context)

@require_POST
def actualizar_inventario_view(request):
    """Vista para actualizar la cantidad disponible de un producto"""
    if 'usernameEmpresa' not in request.session:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)
    
    try:
        producto_tipo = request.POST.get('tipo')
        producto_id = request.POST.get('id')
        nueva_cantidad = int(request.POST.get('cantidad'))
        
        # Obtener el modelo correcto según el tipo
        modelos = {
            'mesa': Mesas,
            'silla': Sillas,
            'armario': Armarios,
            'cajonera': Cajoneras,
            'escritorio': Escritorios,
            'utensilio': Utensilios
        }
        
        modelo = modelos.get(producto_tipo)
        if not modelo:
            return JsonResponse({'success': False, 'error': 'Tipo de producto inválido'}, status=400)
        
        producto = modelo.objects.get(id=producto_id)
        producto.cantidad_disponible = nueva_cantidad
        producto.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Inventario actualizado: {nueva_cantidad} unidades disponibles'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
