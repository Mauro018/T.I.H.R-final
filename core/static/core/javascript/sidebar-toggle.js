// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content-wrapper');
    
    // No hacer nada si no hay sidebar (ej: landing page)
    if (!sidebar) return;
    
    // Crear botón toggle si no existe
    let toggleBtn = document.querySelector('.sidebar-toggle');
    if (!toggleBtn) {
        toggleBtn = document.createElement('button');
        toggleBtn.className = 'sidebar-toggle';
        toggleBtn.innerHTML = '☰';
        toggleBtn.setAttribute('aria-label', 'Toggle sidebar');
        document.body.appendChild(toggleBtn);
    }
    
    // Recuperar estado del sidebar desde localStorage
    const sidebarState = localStorage.getItem('sidebarCollapsed') === 'true';
    if (sidebarState) {
        sidebar.classList.add('collapsed');
        if (mainContent) mainContent.classList.add('sidebar-collapsed');
        // Botón en posición fija cuando está colapsado
        toggleBtn.classList.add('sidebar-inside');
        toggleBtn.innerHTML = '☰';
    } else {
        // Botón afuera del sidebar cuando está expandido
        toggleBtn.classList.remove('sidebar-inside');
        toggleBtn.innerHTML = '✕';
    }
    
    // Event listener para el botón toggle
    toggleBtn.addEventListener('click', () => {
        const isCollapsed = sidebar.classList.toggle('collapsed');
        
        if (mainContent) {
            mainContent.classList.toggle('sidebar-collapsed', isCollapsed);
        }
        
        // Cambiar clase del botón
        if (isCollapsed) {
            // Colapsado: botón en posición fija sobre el sidebar colapsado
            toggleBtn.classList.add('sidebar-inside');
            toggleBtn.innerHTML = '☰';
        } else {
            // Expandido: botón en posición fija afuera
            toggleBtn.classList.remove('sidebar-inside');
            toggleBtn.innerHTML = '✕';
        }
        
        // Guardar estado en localStorage
        localStorage.setItem('sidebarCollapsed', isCollapsed);
    });
    
    // Cerrar sidebar en dispositivos móviles cuando se hace clic en un enlace
    if (window.innerWidth < 768) {
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (!sidebar.classList.contains('collapsed')) {
                    sidebar.classList.add('collapsed');
                    if (mainContent) mainContent.classList.add('sidebar-collapsed');
                    // Meter botón adentro
                    toggleBtn.classList.add('sidebar-inside');
                    toggleBtn.innerHTML = '☰';
                    localStorage.setItem('sidebarCollapsed', 'true');
                }
            });
        });
    }
});

// Ajustar sidebar en resize
window.addEventListener('resize', () => {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const mainContent = document.querySelector('.main-content-wrapper');
    
    // En dispositivos muy pequeños, colapsar por defecto
    if (window.innerWidth < 480 && !sidebar.classList.contains('collapsed')) {
        sidebar.classList.add('collapsed');
        if (mainContent) mainContent.classList.add('sidebar-collapsed');
        if (toggleBtn) {
            toggleBtn.classList.add('sidebar-inside');
            toggleBtn.innerHTML = '☰';
        }
        localStorage.setItem('sidebarCollapsed', 'true');
    }
});
