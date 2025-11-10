import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from core.models import Pedido

# Actualizar pedido existente para que no tenga datos
pedido = Pedido.objects.first()
if pedido:
    pedido.nombre_completo = None
    pedido.direccion = None
    pedido.telefono = None
    pedido.ciudad = None
    pedido.departamento = None
    pedido.save()
    print(f"Pedido #{pedido.id} actualizado - ahora SIN datos de envío")
