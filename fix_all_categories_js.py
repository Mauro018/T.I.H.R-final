import re

# Código JavaScript que funciona (de ceramica.html)
js_correcto = '''
<script>
    let currentProduct = {};
    async function mostrarDetalles(tipo, id, nombre, descripcion, precio, imagen) {
        console.log('Mostrando detalles:', tipo, id, nombre);
        currentProduct = {tipo: tipo, id: id, nombre: nombre, descripcion: descripcion, precio: parseFloat(precio), imagen: imagen, cantidad_disponible: 0, cantidad_restante: 0};
        try {
            const url = `/api/producto/cantidad-disponible/?tipo=${tipo}&id=${id}`;
            const response = await fetch(url);
            if (!response.ok) {
                let errorMsg = `Error HTTP ${response.status}`;
                try { const errorData = await response.json(); errorMsg = errorData.error || errorMsg; } catch (e) { console.error('Error parsing:', e); }
                alert('Error al obtener disponibilidad: ' + errorMsg);
                return;
            }
            const data = await response.json();
            currentProduct.cantidad_disponible = data.cantidad_disponible || 0;
            let carrito = JSON.parse(sessionStorage.getItem('carrito') || '[]');
            let existente = carrito.find(item => item.tipo === tipo && item.id === id);
            let cantidadEnCarrito = existente ? existente.cantidad : 0;
            currentProduct.cantidad_restante = currentProduct.cantidad_disponible - cantidadEnCarrito;
            if (currentProduct.cantidad_disponible === 0) { alert('Este producto no está disponible en inventario.'); return; }
            if (currentProduct.cantidad_restante <= 0) { alert(`Ya tienes todas las unidades disponibles (${currentProduct.cantidad_disponible}) en tu carrito.`); return; }
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
    }
    function cerrarModal() { document.getElementById('productModal').style.display = 'none'; }
    function cambiarCantidad(delta) {
        let input = document.getElementById('quantity');
        let newValue = parseInt(input.value) + delta;
        let maxCantidad = currentProduct.cantidad_restante || 1;
        if (newValue < 1) return;
        if (newValue > maxCantidad) { alert(`Solo puedes agregar ${maxCantidad} unidades más de este producto.`); return; }
        input.value = newValue;
        actualizarTotal();
    }
    function actualizarTotal() {
        let cantidad = parseInt(document.getElementById('quantity').value);
        let total = currentProduct.precio * cantidad;
        document.getElementById('totalPrice').textContent = total.toFixed(2);
    }
    async function agregarAlCarrito() {
        let cantidad = parseInt(document.getElementById('quantity').value);
        if (!currentProduct.tipo || !currentProduct.id) { alert('Error: Información del producto no disponible'); return; }
        try {
            const response = await fetch(`/api/producto/cantidad-disponible/?tipo=${currentProduct.tipo}&id=${currentProduct.id}`);
            if (!response.ok) { alert('Error al verificar disponibilidad del producto. Código: ' + response.status); return; }
            const data = await response.json();
            let carrito = JSON.parse(sessionStorage.getItem('carrito') || '[]');
            let existente = carrito.find(item => item.tipo === currentProduct.tipo && item.id === currentProduct.id);
            let cantidadEnCarrito = existente ? existente.cantidad : 0;
            let cantidadTotal = cantidadEnCarrito + cantidad;
            if (data.cantidad_disponible === 0) { alert('Este producto no está disponible en inventario en este momento.'); return; }
            if (cantidadTotal > data.cantidad_disponible) { alert(`Solo hay ${data.cantidad_disponible} unidades disponibles en inventario. Ya tienes ${cantidadEnCarrito} en tu carrito.`); return; }
            if (existente) { existente.cantidad += cantidad; } 
            else { carrito.push({tipo: currentProduct.tipo, id: currentProduct.id, nombre: currentProduct.nombre, precio: currentProduct.precio, cantidad: cantidad, imagen: currentProduct.imagen, descripcion: currentProduct.descripcion}); }
            sessionStorage.setItem('carrito', JSON.stringify(carrito));
            updateCartBadge();
            alert('¡Producto agregado al carrito!');
            cerrarModal();
            if (confirm('¿Desea ir al carrito ahora?')) { window.location.href = '{% url "carrito" %}'; }
        } catch (error) { console.error('Error:', error); alert('Error al agregar el producto al carrito'); }
    }
    window.onclick = function(event) { let modal = document.getElementById('productModal'); if (event.target == modal) { cerrarModal(); } }
  function aplicarFiltros() {
        const categoria = document.getElementById('categoria').value;
        if (categoria) { window.location.href = '/' + categoria + '/'; } 
        else { window.location.href = '/productos/'; }
    }
    
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
</script>'''

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
        
        # Buscar el inicio del script y el final (antes del script de Carrito.js)
        patron_inicio = r'<script>\s*let currentProduct'
        patron_fin = r'</script>\s*<script src="{%\s*static\s*[\'"]core/javascript/Carrito\.js[\'"]\s*%}"></script>'
        
        # Buscar el inicio
        inicio = re.search(patron_inicio, contenido)
        if not inicio:
            print(f"⚠ No se encontró el inicio del script en {archivo}")
            continue
            
        # Buscar el fin
        fin = re.search(patron_fin, contenido)
        if not fin:
            print(f"⚠ No se encontró el fin del script en {archivo}")
            continue
        
        # Extraer la parte antes y después del script
        antes_script = contenido[:inicio.start()]
        despues_script = contenido[fin.start():]
        
        # Construir el nuevo contenido
        nuevo_contenido = antes_script + js_correcto + '\n\n' + despues_script
        
        # Guardar
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print(f"✅ {archivo} actualizado correctamente")
        
    except Exception as e:
        print(f"❌ Error en {archivo}: {e}")

print("\n¡Proceso completado!")
