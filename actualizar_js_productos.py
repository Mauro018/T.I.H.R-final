import os
import re

# Script completo para actualizar la función mostrarDetalles en todos los templates

# Nueva función mostrarDetalles completa
nueva_funcion_mostrar = '''    async function mostrarDetalles(tipo, id, nombre, descripcion, precio, imagen) {
        console.log('Mostrando detalles:', tipo, id, nombre);
        currentProduct = {
            tipo: tipo,
            id: id,
            nombre: nombre,
            descripcion: descripcion,
            precio: parseFloat(precio),
            imagen: imagen,
            cantidad_disponible: 0,
            cantidad_restante: 0
        };
        
        try {
            const url = `/api/producto/cantidad-disponible/?tipo=${tipo}&id=${id}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                let errorMsg = `Error HTTP ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) {
                    console.error('Error parsing:', e);
                }
                alert('Error al obtener disponibilidad: ' + errorMsg);
                return;
            }
            
            const data = await response.json();
            currentProduct.cantidad_disponible = data.cantidad_disponible || 0;
            
            let carrito = JSON.parse(sessionStorage.getItem('carrito') || '[]');
            let existente = carrito.find(item => item.tipo === tipo && item.id === id);
            let cantidadEnCarrito = existente ? existente.cantidad : 0;
            currentProduct.cantidad_restante = currentProduct.cantidad_disponible - cantidadEnCarrito;
            
            if (currentProduct.cantidad_disponible === 0) {
                alert('Este producto no está disponible en inventario.');
                return;
            }
            
            if (currentProduct.cantidad_restante <= 0) {
                alert(`Ya tienes todas las unidades disponibles (${currentProduct.cantidad_disponible}) en tu carrito.`);
                return;
            }
            
            document.getElementById('modalProductName').textContent = nombre;
            document.getElementById('modalProductDescription').textContent = descripcion;
            document.getElementById('modalProductPrice').textContent = precio;
            document.getElementById('modalImage').src = imagen;
            document.getElementById('quantity').value = 1;
            document.getElementById('quantity').max = currentProduct.cantidad_restante;
            
            const dispText = document.getElementById('disponibilidadText');
            if (cantidadEnCarrito > 0) {
                dispText.textContent = `Disponibles: ${currentProduct.cantidad_restante} unidades (${cantidadEnCarrito} ya en tu carrito)`;
                dispText.style.color = currentProduct.cantidad_restante < 5 ? '#ff9800' : '#28a745';
            } else {
                dispText.textContent = `Disponibles: ${currentProduct.cantidad_disponible} unidades`;
                dispText.style.color = currentProduct.cantidad_disponible < 5 ? '#ff9800' : '#28a745';
            }
            
            actualizarTotal();
            document.getElementById('productModal').style.display = 'block';
        } catch (error) {
            console.error('Error completo:', error);
            alert('Error al cargar la información del producto: ' + error.message);
        }
    }'''

# Nueva función cambiarCantidad
nueva_funcion_cambiar = '''    function cambiarCantidad(delta) {
        let input = document.getElementById('quantity');
        let newValue = parseInt(input.value) + delta;
        let maxCantidad = currentProduct.cantidad_restante || 1;
        
        if (newValue < 1) return;
        if (newValue > maxCantidad) {
            alert(`Solo puedes agregar ${maxCantidad} unidades más de este producto.`);
            return;
        }
        
        input.value = newValue;
        actualizarTotal();
    }'''

archivos = [
    'Productos/templates/Productos/carpinteria.html',
    'Productos/templates/Productos/marroquineria.html',
    'Productos/templates/Productos/vidrieria.html',
    'Productos/templates/Productos/metaleria.html',
    'Productos/templates/Productos/tapiceria.html',
]

print("Actualizando funciones JavaScript...")

for archivo in archivos:
    archivo_path = os.path.join(r'c:\Users\SENA\Documents\T.I.H.R-final', archivo)
    
    if not os.path.exists(archivo_path):
        print(f"❌ No se encontró: {archivo}")
        continue
    
    print(f"📝 Procesando: {archivo}")
    
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar función mostrarDetalles (busca desde function hasta el cierre antes de cerrarModal)
    patron_mostrar = r'(\s*)function mostrarDetalles\(tipo, id, nombre, descripcion, precio, imagen\)\s*\{[^}]*?\{[^}]*?\}[^}]*?\}'
    if re.search(patron_mostrar, contenido):
        contenido = re.sub(patron_mostrar, nueva_funcion_mostrar, contenido, count=1)
        print(f"  ✓ Actualizada mostrarDetalles")
    
    # Reemplazar función cambiarCantidad
    patron_cambiar = r'(\s*)function cambiarCantidad\(delta\)\s*\{[^}]*?\}'
    if re.search(patron_cambiar, contenido):
        contenido = re.sub(patron_cambiar, nueva_funcion_cambiar, contenido, count=1)
        print(f"  ✓ Actualizada cambiarCantidad")
    
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"  ✅ Completado: {archivo}")

print("\n✅ Todos los archivos JavaScript han sido actualizados!")
