"""
Script de prueba para verificar la configuración del email
Ejecutar con: python test_email.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gangazos1.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("🔧 Configuración de Email:")
    print(f"   Host: {settings.EMAIL_HOST}")
    print(f"   Puerto: {settings.EMAIL_PORT}")
    print(f"   Usuario: {settings.EMAIL_HOST_USER}")
    print(f"   TLS: {settings.EMAIL_USE_TLS}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print("\n📧 Enviando email de prueba...")
    
    try:
        codigo_prueba = "1234"
        send_mail(
            subject='🔐 Prueba - Código de Verificación TIHR',
            message=f'''
¡Hola Usuario de Prueba!

Este es un correo de prueba del sistema de verificación.

Tu código de verificación de prueba es:

    {codigo_prueba}

Si recibiste este correo, ¡la configuración está funcionando correctamente! ✅

---
Atentamente,
El equipo de TIHR Gangazos
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Enviando al mismo email para prueba
            fail_silently=False,
        )
        print("\n✅ ¡Email enviado correctamente!")
        print(f"   Revisa la bandeja de entrada de: {settings.EMAIL_HOST_USER}")
        
    except Exception as e:
        print(f"\n❌ Error al enviar el email:")
        print(f"   {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que la contraseña de aplicación sea correcta")
        print("   2. Asegúrate de que la verificación en 2 pasos esté activada")
        print("   3. Genera una nueva contraseña de aplicación en:")
        print("      https://myaccount.google.com/apppasswords")

if __name__ == '__main__':
    test_email()
