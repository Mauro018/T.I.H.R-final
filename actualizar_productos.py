import os
import re

# Script para actualizar todos los templates de productos con la nueva funcionalidad

archivos_producto = [
    'Productos/templates/Productos/carpinteria.html',
    'Productos/templates/Productos/marroquineria.html',
    'Productos/templates/Productos/vidrieria.html',
    'Productos/templates/Productos/metaleria.html',
    'Productos/templates/Productos/tapiceria.html',
]

# HTML para el texto de disponibilidad (agregar después del precio)
texto_disponibilidad = '<p id="disponibilidadText" style="color: #28a745; font-weight: bold; margin: 10px 0;"></p>'

print("Actualizando templates de productos...")

for archivo in archivos_producto:
    archivo_path = os.path.join(r'c:\Users\SENA\Documents\T.I.H.R-final', archivo)
    
    if not os.path.exists(archivo_path):
        print(f"❌ No se encontró: {archivo}")
        continue
    
    print(f"📝 Procesando: {archivo}")
    
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar si ya tiene el texto de disponibilidad
    if 'id="disponibilidadText"' in contenido:
        print(f"  ✓ Ya tiene el texto de disponibilidad")
    else:
        # Agregar el texto de disponibilidad después del precio
        contenido = re.sub(
            r'(<p class="precio-destacado">Precio: \$<span id="modalProductPrice"></span></p>)',
            r'\1\n                ' + texto_disponibilidad,
            contenido
        )
        print(f"  ✓ Agregado texto de disponibilidad")
    
    # Guardar el archivo
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"  ✅ Actualizado: {archivo}")

print("\n✅ Todos los archivos han sido actualizados!")
