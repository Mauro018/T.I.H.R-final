/**
 * Script global para gestión del carrito de compras
 * Mantiene sincronizado el badge del carrito en todas las páginas
 */

// Función para obtener el carrito de sessionStorage
function getCartGlobal() {
    return JSON.parse(sessionStorage.getItem('carrito') || '[]');
}

// Función para actualizar el badge del carrito en todas las páginas
function updateCartBadgeGlobal() {
    const carrito = getCartGlobal();
    const badge = document.getElementById('cart-count-badge');
    
    if (!badge) return;
    
    const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    
    if (totalItems > 0) {
        badge.textContent = totalItems;
        badge.style.display = 'flex';
    } else {
        badge.style.display = 'none';
    }
}

// Actualizar badge cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    updateCartBadgeGlobal();
});

// Actualizar badge cuando cambia el almacenamiento (para múltiples pestañas)
window.addEventListener('storage', function(e) {
    if (e.key === 'carrito') {
        updateCartBadgeGlobal();
    }
});
