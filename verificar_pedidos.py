import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from core.models import Pedido

print("=" * 50)
print("VERIFICACIÓN DE PEDIDOS")
print("=" * 50)

pedidos = Pedido.objects.all()
print(f"\nTotal de pedidos: {pedidos.count()}")

for pedido in pedidos:
    print(f"\nPedido #{pedido.id}")
    print(f"  Cliente: {pedido.cliente.usernameCliente}")
    print(f"  Nombre: {pedido.nombre_completo}")
    print(f"  Dirección: {pedido.direccion}")
    print(f"  Teléfono: {pedido.telefono}")
    print(f"  Ciudad: {pedido.ciudad}")
    print(f"  Estado: {pedido.estado}")
    print(f"  Tiene datos completos: {bool(pedido.direccion and pedido.telefono and pedido.nombre_completo)}")

print("\n" + "=" * 50)
