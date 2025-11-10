import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from core.models import Pedido, Pago, UserClientes

print("=" * 50)
print("VERIFICACIÓN DE PEDIDOS")
print("=" * 50)

# Total de pedidos
total_pedidos = Pedido.objects.count()
print(f"\nTotal de pedidos en la BD: {total_pedidos}")

# Listar todos los pedidos
if total_pedidos > 0:
    print("\nPedidos encontrados:")
    for pedido in Pedido.objects.all():
        print(f"  - Pedido #{pedido.id}")
        print(f"    Cliente: {pedido.cliente.usernameCliente}")
        print(f"    Estado: {pedido.get_estado_display()}")
        print(f"    Fecha: {pedido.fecha_creacion}")
        print(f"    Monto: ${pedido.monto_total}")
        print()
else:
    print("\n⚠️  No hay pedidos en la base de datos")

# Verificar pagos confirmados sin pedidos
print("\n" + "=" * 50)
print("PAGOS CONFIRMADOS SIN PEDIDO")
print("=" * 50)

pagos_confirmados = Pago.objects.filter(estado='confirmado')
print(f"\nTotal pagos confirmados: {pagos_confirmados.count()}")

for pago in pagos_confirmados:
    tiene_pedido = hasattr(pago, 'pedido')
    print(f"\n  - Pago #{pago.id}")
    print(f"    Cliente: {pago.cliente.usernameCliente}")
    print(f"    Monto: ${pago.monto_total}")
    print(f"    Tiene pedido: {'✓ SÍ' if tiene_pedido else '✗ NO'}")
    if tiene_pedido:
        print(f"    Pedido asociado: #{pago.pedido.id}")

print("\n" + "=" * 50)
