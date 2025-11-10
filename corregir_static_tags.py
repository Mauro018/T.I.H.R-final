import re

archivos = [
    'Productos/templates/Productos/carpinteria.html',
    'Productos/templates/Productos/marroquineria.html',
    'Productos/templates/Productos/metaleria.html',
    'Productos/templates/Productos/tapiceria.html'
]

for archivo in archivos:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Corregir las comillas escapadas en el static tag
        contenido_corregido = contenido.replace(
            "{% static \\'core/javascript/Carrito.js\\' %}",
            "{% static 'core/javascript/Carrito.js' %}"
        )
        
        # Verificar si falta el cierre de llave de aplicarFiltros()
        # Buscar el patrón problemático
        patron_error = r"(else \{ window\.location\.href = '/productos/'; \}\s*)(// Función para actualizar el badge del carrito)"
        
        if re.search(patron_error, contenido_corregido):
            # Agregar la llave faltante
            contenido_corregido = re.sub(
                patron_error,
                r"\1}\n    \n    \2",
                contenido_corregido
            )
            print(f"✓ Agregada llave faltante en {archivo}")
        
        # Guardar cambios
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        print(f"✅ Archivo {archivo} corregido\n")
        
    except Exception as e:
        print(f"❌ Error en {archivo}: {e}\n")

print("¡Corrección completada!")
