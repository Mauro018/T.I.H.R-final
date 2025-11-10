import re

# Lista de archivos de categorías a actualizar
archivos = [
    'Productos/templates/Productos/carpinteria.html',
    'Productos/templates/Productos/marroquineria.html',
    'Productos/templates/Productos/vidrieria.html',
    'Productos/templates/Productos/metaleria.html',
    'Productos/templates/Productos/tapiceria.html'
]

# Código para agregar la función updateCartBadge
codigo_badge = """
    // Función para actualizar el badge del carrito
    function updateCartBadge() {
        const carrito = JSON.parse(sessionStorage.getItem('carrito') || '[]');
        const badge = document.getElementById('cart-count-badge');
        const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
        
        if (totalItems > 0) {
            badge.textContent = totalItems;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
    
    // Actualizar badge al cargar la página
    document.addEventListener('DOMContentLoaded', function() {
        updateCartBadge();
    });
</script>"""

for archivo in archivos:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # 1. Agregar updateCartBadge() después de sessionStorage.setItem
        if "sessionStorage.setItem('carrito', JSON.stringify(carrito));" in contenido and \
           "updateCartBadge();" not in contenido:
            contenido = contenido.replace(
                "sessionStorage.setItem('carrito', JSON.stringify(carrito));",
                "sessionStorage.setItem('carrito', JSON.stringify(carrito));\n            updateCartBadge();"
            )
            print(f"✓ Agregado updateCartBadge() llamada en {archivo}")
        
        # 2. Agregar la función updateCartBadge antes del cierre de </script>
        # Buscar el último </script> antes de </body>
        if "function updateCartBadge()" not in contenido:
            # Encontrar el patrón de cierre de script antes del script de Carrito.js
            patron = r'(\s+}\s*</script>\s*<script src="{%\s*static\s*[\'"]core/javascript/Carrito\.js[\'"]\s*%}"></script>)'
            
            if re.search(patron, contenido):
                contenido = re.sub(
                    patron,
                    codigo_badge + r'\n\n<script src="{% static \'core/javascript/Carrito.js\' %}"></script>',
                    contenido
                )
                print(f"✓ Agregada función updateCartBadge() en {archivo}")
            else:
                print(f"⚠ No se encontró el patrón esperado en {archivo}")
        
        # Guardar cambios
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"✅ Archivo {archivo} actualizado correctamente\n")
        
    except Exception as e:
        print(f"❌ Error en {archivo}: {e}\n")

print("Proceso completado!")
