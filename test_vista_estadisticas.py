import os
import django
from django.http import HttpRequest
from django.contrib.sessions.middleware import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from Empresas.views_estadisticas import estadisticas_view
from core.models import *

# Crear request simulado
request = HttpRequest()
request.method = 'GET'

# Agregar sesión
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request)
request.session['usernameEmpresa'] = 'test'
request.session.save()

# Ejecutar la vista
response = estadisticas_view(request)

print("Status Code:", response.status_code)

# Intentar extraer el contexto del HTML
content = response.content.decode('utf-8')

# Buscar valores en el HTML
import re

print("\n=== VALORES ENCONTRADOS EN EL HTML ===")

# Buscar números en stat-number
stat_numbers = re.findall(r'<p class="stat-number">([^<]+)</p>', content)
print(f"Números en stat-number: {stat_numbers}")

# Buscar números en categoria-cantidad
categoria_cantidades = re.findall(r'<p class="categoria-cantidad">([^<]+)</p>', content)
print(f"Números en categoria-cantidad: {categoria_cantidades}")

# Buscar números en estado-numero
estado_numeros = re.findall(r'<p class="estado-numero">([^<]+)</p>', content)
print(f"Números en estado-numero: {estado_numeros}")

print("\n=== VERIFICACIÓN DE DATOS EN BD ===")
print(f"Total productos en BD: {Mesas.objects.count() + Sillas.objects.count() + Armarios.objects.count() + Cajoneras.objects.count() + Escritorios.objects.count() + Utensilios.objects.count()}")
print(f"Total pedidos en BD: {Pedido.objects.count()}")
print(f"Total pagos en BD: {Pago.objects.count()}")


