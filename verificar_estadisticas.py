import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from core.models import UserClientes, Pedido, Pago, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios
from django.db.models import Sum

print("=== VERIFICACIÓN DE ESTADÍSTICAS ===\n")

# Estadísticas de usuarios
total_usuarios = UserClientes.objects.count()
usuarios_activos = UserClientes.objects.filter(is_active=True).count()
print(f"Usuarios Totales: {total_usuarios}")
print(f"Usuarios Activos: {usuarios_activos}\n")

# Estadísticas de productos
total_mesas = Mesas.objects.count()
inventario_mesas = Mesas.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_sillas = Sillas.objects.count()
inventario_sillas = Sillas.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_armarios = Armarios.objects.count()
inventario_armarios = Armarios.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_cajoneras = Cajoneras.objects.count()
inventario_cajoneras = Cajoneras.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_escritorios = Escritorios.objects.count()
inventario_escritorios = Escritorios.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_utensilios = Utensilios.objects.count()
inventario_utensilios = Utensilios.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0

total_productos = total_mesas + total_sillas + total_armarios + total_cajoneras + total_escritorios + total_utensilios
total_inventario = inventario_mesas + inventario_sillas + inventario_armarios + inventario_cajoneras + inventario_escritorios + inventario_utensilios

print("PRODUCTOS POR CATEGORÍA:")
print(f"Mesas: {total_mesas} productos, {inventario_mesas} unidades")
print(f"Sillas: {total_sillas} productos, {inventario_sillas} unidades")
print(f"Armarios: {total_armarios} productos, {inventario_armarios} unidades")
print(f"Cajoneras: {total_cajoneras} productos, {inventario_cajoneras} unidades")
print(f"Escritorios: {total_escritorios} productos, {inventario_escritorios} unidades")
print(f"Utensilios: {total_utensilios} productos, {inventario_utensilios} unidades")
print(f"\nTotal Productos: {total_productos}")
print(f"Total Inventario: {total_inventario}\n")

# Estadísticas de pedidos
total_pedidos = Pedido.objects.count()
pedidos_procesando = Pedido.objects.filter(estado='procesando').count()
pedidos_enviado = Pedido.objects.filter(estado='enviado').count()
pedidos_en_transito = Pedido.objects.filter(estado='en_transito').count()
pedidos_entregado = Pedido.objects.filter(estado='entregado').count()

print("PEDIDOS:")
print(f"Total: {total_pedidos}")
print(f"Procesando: {pedidos_procesando}")
print(f"Enviado: {pedidos_enviado}")
print(f"En Tránsito: {pedidos_en_transito}")
print(f"Entregado: {pedidos_entregado}\n")

# Estadísticas de pagos
total_pagos = Pago.objects.count()
pagos_pendientes = Pago.objects.filter(estado='pendiente').count()
pagos_confirmados = Pago.objects.filter(estado='confirmado').count()
pagos_rechazados = Pago.objects.filter(estado='rechazado').count()

print("PAGOS:")
print(f"Total: {total_pagos}")
print(f"Pendientes: {pagos_pendientes}")
print(f"Confirmados: {pagos_confirmados}")
print(f"Rechazados: {pagos_rechazados}\n")

# Ingresos totales
ingresos_totales = Pago.objects.filter(estado='confirmado').aggregate(total=Sum('monto_total'))['total'] or 0
print(f"Ingresos Totales: ${ingresos_totales}")
