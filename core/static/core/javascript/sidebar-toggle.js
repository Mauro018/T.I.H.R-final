/**
 * Sidebar Toggle para Dispositivos Móviles y Tablets
 * Gestiona la apertura y cierre del sidebar en pantallas < 1366px
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const sidebar = document.querySelector('.sidebar');
    
    // Solo ejecutar si existe el sidebar
    if (!sidebar) {
        return;
    }

    // Crear botón toggle si no existe
    let toggleBtn = document.querySelector('.sidebar-toggle');
    if (!toggleBtn) {
        toggleBtn = createToggleButton();
        // Insertar en el header
        const header = document.querySelector('header');
        if (header) {
            header.insertBefore(toggleBtn, header.firstChild);
        } else {
            document.body.appendChild(toggleBtn);
        }
    }

    // Crear overlay si no existe
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = createOverlay();
        document.body.appendChild(overlay);
    }

    // Event listeners
    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Cerrar sidebar al hacer clic en un enlace (solo en móvil)
    const sidebarLinks = sidebar.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 1366) {
                closeSidebar();
            }
        });
    });

    // Cerrar sidebar al redimensionar a pantalla grande
    window.addEventListener('resize', function() {
        if (window.innerWidth > 1366) {
            closeSidebar();
        }
    });

    // Manejar tecla Escape para cerrar
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebar();
        }
    });

    /**
     * Crea el botón toggle del sidebar
     */
    function createToggleButton() {
        const btn = document.createElement('button');
        btn.className = 'sidebar-toggle';
        btn.setAttribute('aria-label', 'Toggle sidebar');
        btn.innerHTML = '☰';
        return btn;
    }

    /**
     * Crea el overlay oscuro
     */
    function createOverlay() {
        const div = document.createElement('div');
        div.className = 'sidebar-overlay';
        return div;
    }

    /**
     * Alterna la visibilidad del sidebar
     */
    function toggleSidebar() {
        const isActive = sidebar.classList.contains('active');
        
        if (isActive) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    /**
     * Abre el sidebar
     */
    function openSidebar() {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        toggleBtn.innerHTML = '✕';
        
        // Prevenir scroll del body
        document.body.style.overflow = 'hidden';
        
        // Accesibilidad
        sidebar.setAttribute('aria-hidden', 'false');
        toggleBtn.setAttribute('aria-expanded', 'true');
    }

    /**
     * Cierra el sidebar
     */
    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        toggleBtn.innerHTML = '☰';
        
        // Restaurar scroll del body
        document.body.style.overflow = '';
        
        // Accesibilidad
        sidebar.setAttribute('aria-hidden', 'true');
        toggleBtn.setAttribute('aria-expanded', 'false');
    }

    // Soporte para gestos táctiles (swipe)
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    /**
     * Maneja gestos de swipe
     */
    function handleSwipe() {
        // Solo en dispositivos móviles
        if (window.innerWidth > 1366) {
            return;
        }

        const swipeDistance = touchEndX - touchStartX;
        const minSwipeDistance = 50;

        // Swipe desde la izquierda para abrir
        if (touchStartX < 50 && swipeDistance > minSwipeDistance) {
            openSidebar();
        }

        // Swipe hacia la izquierda para cerrar
        if (sidebar.classList.contains('active') && swipeDistance < -minSwipeDistance) {
            closeSidebar();
        }
    }

    // Estado inicial correcto basado en el tamaño de pantalla
    if (window.innerWidth <= 1366) {
        closeSidebar();
    }
});
