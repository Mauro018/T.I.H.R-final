"""
Script de Validación - Sistema de Modelos 3D
Verifica que todos los archivos necesarios existan y estén configurados correctamente
"""

import os
import sys

def check_file(path, description):
    """Verifica si un archivo existe"""
    if os.path.exists(path):
        print(f"✅ {description}: OK")
        return True
    else:
        print(f"❌ {description}: NO ENCONTRADO")
        return False

def check_directory(path, description):
    """Verifica si un directorio existe"""
    if os.path.isdir(path):
        print(f"✅ {description}: OK")
        return True
    else:
        print(f"⚠️  {description}: NO EXISTE (se creará automáticamente)")
        return False

def check_content_in_file(path, search_text, description):
    """Verifica si un texto existe en un archivo"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print(f"✅ {description}: OK")
                return True
            else:
                print(f"❌ {description}: NO ENCONTRADO")
                return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("VALIDACIÓN DEL SISTEMA DE MODELOS 3D")
    print("=" * 60)
    print()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    errors = 0

    # 1. Verificar modelos
    print("📋 1. MODELOS")
    print("-" * 60)
    if not check_content_in_file(
        os.path.join(base_dir, 'core', 'models.py'),
        'modelo_3d',
        "Campo modelo_3d en Idea"
    ):
        errors += 1
    print()

    # 2. Verificar formularios
    print("📝 2. FORMULARIOS")
    print("-" * 60)
    if not check_content_in_file(
        os.path.join(base_dir, 'core', 'forms.py'),
        'modelo_3d',
        "Campo modelo_3d en IdeaForm"
    ):
        errors += 1
    print()

    # 3. Verificar vistas
    print("👁️ 3. VISTAS")
    print("-" * 60)
    if not check_content_in_file(
        os.path.join(base_dir, 'Empresas', 'views.py'),
        'ver_imagen_idea',
        "Vista ver_imagen_idea"
    ):
        errors += 1
    if not check_content_in_file(
        os.path.join(base_dir, 'Empresas', 'views.py'),
        'ver_modelo_3d_idea',
        "Vista ver_modelo_3d_idea"
    ):
        errors += 1
    print()

    # 4. Verificar URLs
    print("🔗 4. URLs")
    print("-" * 60)
    if not check_content_in_file(
        os.path.join(base_dir, 'Empresas', 'urls.py'),
        'ver_imagen_idea',
        "URL ver_imagen_idea"
    ):
        errors += 1
    if not check_content_in_file(
        os.path.join(base_dir, 'Empresas', 'urls.py'),
        'ver_modelo_3d_idea',
        "URL ver_modelo_3d_idea"
    ):
        errors += 1
    print()

    # 5. Verificar plantillas
    print("📄 5. PLANTILLAS")
    print("-" * 60)
    if not check_file(
        os.path.join(base_dir, 'Empresas', 'templates', 'Empresas', 'ver_imagen_idea.html'),
        "Plantilla ver_imagen_idea.html"
    ):
        errors += 1
    if not check_file(
        os.path.join(base_dir, 'Empresas', 'templates', 'Empresas', 'ver_modelo_3d_idea.html'),
        "Plantilla ver_modelo_3d_idea.html"
    ):
        errors += 1
    print()

    # 6. Verificar CSS
    print("🎨 6. ARCHIVOS CSS")
    print("-" * 60)
    if not check_file(
        os.path.join(base_dir, 'Empresas', 'static', 'Empresas', 'css', 'ver_media.css'),
        "CSS ver_media.css"
    ):
        errors += 1
    print()

    # 7. Verificar configuración
    print("⚙️ 7. CONFIGURACIÓN")
    print("-" * 60)
    if not check_content_in_file(
        os.path.join(base_dir, 'Gangazos1', 'settings.py'),
        'MEDIA_URL',
        "MEDIA_URL en settings.py"
    ):
        errors += 1
    if not check_content_in_file(
        os.path.join(base_dir, 'Gangazos1', 'settings.py'),
        'MEDIA_ROOT',
        "MEDIA_ROOT en settings.py"
    ):
        errors += 1
    if not check_content_in_file(
        os.path.join(base_dir, 'Gangazos1', 'urls.py'),
        'static(settings.MEDIA_URL',
        "Configuración de media en urls.py"
    ):
        errors += 1
    print()

    # 8. Verificar migraciones
    print("🗃️ 8. MIGRACIONES")
    print("-" * 60)
    if not check_file(
        os.path.join(base_dir, 'core', 'migrations', '0012_idea_modelo_3d.py'),
        "Migración 0012_idea_modelo_3d.py"
    ):
        errors += 1
    print()

    # 9. Verificar directorios
    print("📁 9. DIRECTORIOS")
    print("-" * 60)
    check_directory(
        os.path.join(base_dir, 'uploads'),
        "Directorio uploads/"
    )
    check_directory(
        os.path.join(base_dir, 'uploads', 'ideas'),
        "Directorio uploads/ideas/"
    )
    check_directory(
        os.path.join(base_dir, 'uploads', 'ideas', 'modelos3d'),
        "Directorio uploads/ideas/modelos3d/"
    )
    print()

    # Resumen
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    if errors == 0:
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print()
        print("Siguiente paso:")
        print("  1. Ejecuta: python manage.py migrate")
        print("  2. Ejecuta: python manage.py runserver")
        print("  3. Prueba la funcionalidad")
    else:
        print(f"❌ SE ENCONTRARON {errors} ERRORES")
        print()
        print("Por favor, revisa los archivos marcados con ❌")
        print("Consulta INSTRUCCIONES_MODELO_3D.md para más detalles")
    print("=" * 60)

    return errors == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
