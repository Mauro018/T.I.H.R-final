document.addEventListener('DOMContentLoaded', () => {
    // Definir los usuarios iniciales con sus correos y estado
    let users = [
        { name: 'Mauro', type: 'comprador', email: 'mauro.compras@gmail.com', status: 'activo' },
        { name: 'Jeison', type: 'comprador', email: 'jeison.cliente@gmail.com', status: 'activo' },
        { name: 'Chifu', type: 'comprador', email: 'chifu.comprador@gmail.com', status: 'activo' },
        { name: 'Juanito', type: 'comprador', email: 'juanito.com@gmail.com', status: 'activo' },
        { name: 'Juan', type: 'comprador', email: 'juan.comprador@gmail.com', status: 'activo' },
        { name: 'Ricardo Pérez', type: 'empresario', company: 'Muebles Finos RP', role: 'Gerente', email: 'ricardo.perez@mueblesfinosrp.com', status: 'activo' },
        { name: 'Ana Mendoza', type: 'empresario', company: 'Taller de Carpintería La Mesa', role: 'Dueña', email: 'ana.mendoza@tallerlamesa.com', status: 'activo' },
        { name: 'Luis García', type: 'empresario', company: 'Madera & Estilo', role: 'Presidente', email: 'l.garcia@maderayestilo.com', status: 'inactivo' },
        { name: 'Sofía Díaz', type: 'comprador', email: 'sofia.d@gmail.com', status: 'activo' },
        { name: 'Carlos López', type: 'empresario', company: 'Artesanos del Pino', role: 'Vicepresidente', email: 'carlos.lopez@artesanosdelpino.com', status: 'activo' },
        { name: 'María Gómez', type: 'comprador', email: 'mariagomez.compradora@gmail.com', status: 'activo' }
    ];

    const empresarioList = document.getElementById('empresarios-list');
    const compradorList = document.getElementById('compradores-list');
    const empresarioTitle = document.getElementById('empresarios-title');
    const compradorTitle = document.getElementById('compradores-title');
    
    // Selects del panel de control
    const disableUserSelect = document.getElementById('disable-user-select');
    const changeUserSelect = document.getElementById('change-user-select');
    const messageUserSelect = document.getElementById('message-user-select');

    // Muestra un mensaje flotante
    const showToast = (message) => {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    };

    // Renderiza las listas de usuarios en la interfaz
    const renderUsers = () => {
        empresarioList.innerHTML = '';
        compradorList.innerHTML = '';
        disableUserSelect.innerHTML = '<option value="">Seleccionar usuario</option>';
        changeUserSelect.innerHTML = '<option value="">Seleccionar usuario</option>';
        messageUserSelect.innerHTML = '<option value="">Seleccionar destinatario</option>';

        users.forEach((user, index) => {
            const li = document.createElement('li');
            li.classList.add('p-2', 'border-b', 'border-gray-200', 'flex', 'justify-between', 'items-center', user.status === 'inactivo' ? 'text-gray-400' : 'text-gray-700');
            
            let userName = user.name;
            if (user.type === 'empresario') {
                userName = `${user.name} - ${user.role} de ${user.company}`;
            }

            li.textContent = userName;
            li.setAttribute('data-index', index);
            
            // Si el usuario está inactivo, agregar un indicador
            if (user.status === 'inactivo') {
                const statusSpan = document.createElement('span');
                statusSpan.textContent = '(Inactivo)';
                statusSpan.classList.add('text-red-500', 'font-semibold', 'ml-2');
                li.appendChild(statusSpan);
            }

            if (user.type === 'empresario') {
                empresarioList.appendChild(li);
            } else {
                compradorList.appendChild(li);
            }

            // Llenar los selects del panel de control
            const option1 = document.createElement('option');
            option1.value = index;
            option1.textContent = userName;
            disableUserSelect.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = index;
            option2.textContent = userName;
            changeUserSelect.appendChild(option2);

            const option3 = document.createElement('option');
            option3.value = index;
            option3.textContent = userName;
            messageUserSelect.appendChild(option3);
        });
    };

    // Alternar visibilidad de las listas
    const toggleList = (list) => {
        if (list.style.display === 'none' || list.style.display === '') {
            list.style.display = 'block';
        } else {
            list.style.display = 'none';
        }
    };

    empresarioTitle.addEventListener('click', () => toggleList(empresarioList));
    compradorTitle.addEventListener('click', () => toggleList(compradorList));

    // Formulario para agregar usuario
    document.getElementById('add-user-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('add-user-name').value;
        const type = document.getElementById('add-user-type').value;
        const company = document.getElementById('add-user-company').value;
        
        let newUser = { name, type, status: 'activo' };

        if (type === 'empresario') {
            const roleOptions = ['Dueño', 'Gerente', 'Presidente', 'Vicepresidente'];
            const randomRole = roleOptions[Math.floor(Math.random() * roleOptions.length)];
            const companySlug = company.toLowerCase().replace(/\s/g, '');
            newUser.company = company;
            newUser.role = randomRole;
            newUser.email = `${name.toLowerCase().split(' ')[0]}.${name.toLowerCase().split(' ')[1]}@${companySlug}.com`;
        } else {
            const nameSlug = name.toLowerCase().replace(/\s/g, '.');
            newUser.email = `${nameSlug}@gmail.com`;
        }
        
        users.push(newUser);
        renderUsers();
        showToast(`Cambios realizados exitosamente, las novedades han sido enviadas al usuario ${newUser.name} a su correo electrónico personal ${newUser.email}`);
        e.target.reset();
    });

    // Formulario para deshabilitar/habilitar usuario
    document.getElementById('disable-user-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const userIndex = document.getElementById('disable-user-select').value;
        if (userIndex !== '') {
            const user = users[userIndex];
            user.status = user.status === 'activo' ? 'inactivo' : 'activo';
            renderUsers();
            showToast(`Cambios realizados exitosamente, las novedades han sido enviadas al usuario ${user.name} a su correo electrónico personal ${user.email}`);
            e.target.reset();
        }
    });

    // Formulario para cambiar tipo de usuario
    document.getElementById('change-type-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const userIndex = document.getElementById('change-user-select').value;
        if (userIndex !== '') {
            const user = users[userIndex];
            user.type = user.type === 'empresario' ? 'comprador' : 'empresario';
            if (user.type === 'comprador') {
                delete user.company;
                delete user.role;
                user.email = `${user.name.toLowerCase().replace(/\s/g, '.')}.comprador@gmail.com`;
            } else {
                // Si se convierte a empresario, se necesita el nombre de la empresa. Para el ejemplo, se puede pedir o asignar una por defecto.
                user.company = 'Nueva Empresa Carpintería';
                user.role = 'Socio';
                user.email = `${user.name.toLowerCase().replace(/\s/g, '')}@nuevaempresa.com`;
            }
            renderUsers();
            showToast(`Cambios realizados exitosamente, las novedades han sido enviadas al usuario ${user.name} a su correo electrónico personal ${user.email}`);
            e.target.reset();
        }
    });

    // Formulario para enviar mensaje por correo
    document.getElementById('send-message-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const userIndex = document.getElementById('message-user-select').value;
        const messageContent = document.getElementById('message-content').value;
        if (userIndex !== '') {
            const user = users[userIndex];
            showToast(`El mensaje se ha enviado al correo electrónico del usuario ${user.name}`);
            e.target.reset();
        }
    });
    
    // Cargar los usuarios al iniciar
    renderUsers();
});