import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from core.models import Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios

print("=== INVENTARIO DETALLADO POR PRODUCTO ===\n")

print("MESAS:")
for mesa in Mesas.objects.all():
    print(f"  - {mesa.nombre1}: {mesa.cantidad_disponible} unidades")
total_mesas = sum([m.cantidad_disponible for m in Mesas.objects.all()])
print(f"  TOTAL MESAS: {total_mesas} unidades\n")

print("SILLAS:")
for silla in Sillas.objects.all():
    print(f"  - {silla.nombre2}: {silla.cantidad_disponible} unidades")
total_sillas = sum([s.cantidad_disponible for s in Sillas.objects.all()])
print(f"  TOTAL SILLAS: {total_sillas} unidades\n")

print("ARMARIOS:")
for armario in Armarios.objects.all():
    print(f"  - {armario.nombre3}: {armario.cantidad_disponible} unidades")
total_armarios = sum([a.cantidad_disponible for a in Armarios.objects.all()])
print(f"  TOTAL ARMARIOS: {total_armarios} unidades\n")

print("CAJONERAS:")
for cajonera in Cajoneras.objects.all():
    print(f"  - {cajonera.nombre4}: {cajonera.cantidad_disponible} unidades")
total_cajoneras = sum([c.cantidad_disponible for c in Cajoneras.objects.all()])
print(f"  TOTAL CAJONERAS: {total_cajoneras} unidades\n")

print("ESCRITORIOS:")
for escritorio in Escritorios.objects.all():
    print(f"  - {escritorio.nombre5}: {escritorio.cantidad_disponible} unidades")
total_escritorios = sum([e.cantidad_disponible for e in Escritorios.objects.all()])
print(f"  TOTAL ESCRITORIOS: {total_escritorios} unidades\n")

print("UTENSILIOS:")
for utensilio in Utensilios.objects.all():
    print(f"  - {utensilio.nombre6}: {utensilio.cantidad_disponible} unidades")
total_utensilios = sum([u.cantidad_disponible for u in Utensilios.objects.all()])
print(f"  TOTAL UTENSILIOS: {total_utensilios} unidades\n")

print("="*50)
print(f"TOTAL GENERAL: {total_mesas + total_sillas + total_armarios + total_cajoneras + total_escritorios + total_utensilios} unidades")
