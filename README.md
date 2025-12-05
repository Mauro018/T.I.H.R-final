# T.I.H.R - Sistema de Gestión

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Mauro018/T.I.H.R-final.git
cd T.I.H.R-final
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
```

#### Activar entorno virtual:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Ejecutar el servidor
```bash
python manage.py runserver
```

## Actualizar el repositorio

Cuando actualices el repositorio, ejecuta:

```bash
git pull
pip install -r requirements.txt
python manage.py migrate
```

## Dependencias Principales

- Django 5.2.5
- Django REST Framework 3.16.1
- Pillow 11.3.0 (manejo de imágenes)
- PyOTP 2.9.0 (autenticación de dos factores)
- Social Auth (autenticación con redes sociales)
- QRCode 8.2 (generación de códigos QR)

## Estructura del Proyecto

- `core/` - Aplicación principal
- `Empresas/` - Gestión de empresas
- `Productos/` - Gestión de productos
- `uploads/` - Archivos subidos por usuarios

## Configuración

El proyecto está configurado con una base de datos SQLite (`db.sqlite3`) por defecto.
