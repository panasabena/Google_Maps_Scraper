#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Sender con MEJOR DELIVERABILITY
- Envía desde Gmail directo (va a Principal, no Promociones)
- Delays entre envíos para parecer natural
- Sin headers de marketing masivo
- Perfecto para B2B outreach
"""

import smtplib
from email.message import EmailMessage
import csv
from io import StringIO
import os
import time
import random

# ==================== CONFIGURACIÓN ====================
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'panasabena@gmail.com'
EMAIL_PASSWORD = 'tvnh yezh ifiy egwt'

# Ruta del archivo CSV con contactos
ARCHIVO_CSV = 'contactos_empresas.csv'  # En la misma carpeta que el script

# Asunto del email (personalizable)
ASUNTO = "Simplifique la gestión de sus clientes"

# ==================== CONFIGURACIÓN DE ENVÍO ====================

# Delay entre emails (segundos)
MIN_DELAY = 30  # Mínimo 30 segundos
MAX_DELAY = 60  # Máximo 60 segundos

# Máximo de emails por hora (para no parecer spam)
MAX_PER_HOUR = 50

# ==================== TEMPLATE HTML ====================

def obtener_template_html(nombre_empresa):
    """
    Template HTML PROFESIONAL Y BONITO
    - Header con gradiente atractivo
    - Diseño limpio y profesional
    - Sin tracking (buena deliverability)
    """
    
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Autogestión para Clientes</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4;">
    
    <!-- Container principal -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                
                <!-- Contenedor del email -->
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 600px;">
                    
                    <!-- Header con color de marca -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 40px; border-radius: 8px 8px 0 0; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">
                                Simplifique la gestión de sus clientes
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Contenido principal -->
                    <tr>
                        <td style="padding: 40px 40px 30px 40px;">
                            
                            <!-- Saludo -->
                            <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #333333;">
                                Hola,
                            </p>
                            
                            <!-- Introducción -->
                            <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #333333;">
                                Vimos que <strong>{nombre_empresa}</strong> ofrece servicios recurrentes a clientes.
                            </p>
                            
                            <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.6; color: #333333;">
                                Muchas empresas como la suya gestionan documentación, consultas y trámites mediante emails, WhatsApp y planillas. <strong>Esto consume tiempo y genera desorden.</strong>
                            </p>
                            
                            <!-- Sección de beneficios con fondo -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 25px;">
                                        <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6; color: #333333;">
                                            Nos especializamos en crear <strong>portales de autogestión para clientes</strong> donde pueden:
                                        </p>
                                        
                                        <!-- Lista de beneficios -->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #667eea; font-size: 18px; margin-right: 8px;">✓</span>
                                                    <span style="font-size: 15px; color: #333333; line-height: 1.6;">Descargar documentos (contratos, certificados, facturas)</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #667eea; font-size: 18px; margin-right: 8px;">✓</span>
                                                    <span style="font-size: 15px; color: #333333; line-height: 1.6;">Realizar trámites online</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #667eea; font-size: 18px; margin-right: 8px;">✓</span>
                                                    <span style="font-size: 15px; color: #333333; line-height: 1.6;">Consultar servicios activos</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #667eea; font-size: 18px; margin-right: 8px;">✓</span>
                                                    <span style="font-size: 15px; color: #333333; line-height: 1.6;">Enviar solicitudes organizadas</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Propuesta de valor -->
                            <p style="margin: 25px 0; font-size: 16px; line-height: 1.6; color: #333333; text-align: center;">
                                <strong style="color: #667eea; font-size: 17px;">Todo en un único lugar profesional con su marca.</strong>
                            </p>
                            
                            <!-- Call to Action -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0 20px 0;">
                                <tr>
                                    <td align="center">
                                        <table cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td align="center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 6px; padding: 14px 40px;">
                                                    <a href="https://calendly.com/alfre-sabena/30min" style="color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 600; display: block;">
                                                        Agendar demo de 5 minutos →
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 25px 0 0 0; font-size: 16px; line-height: 1.6; color: #333333; text-align: center;">
                                ¿Le interesa ver cómo funciona?
                            </p>
                            
                        </td>
                    </tr>
                    
                    <!-- Firma -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px; border-top: 1px solid #e9ecef;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 30px;">
                                <tr>
                                    <td>
                                        <p style="margin: 0 0 5px 0; font-size: 16px; font-weight: 600; color: #333333;">
                                            Saludos,
                                        </p>
                                        <p style="margin: 0 0 3px 0; font-size: 16px; font-weight: 600; color: #667eea;">
                                            Alfredo Sabena
                                        </p>
                                        <p style="margin: 0 0 2px 0; font-size: 14px; color: #666666;">
                                            Co-founder - Data Analytics | Saas Multitenant
                                        </p>
                                        <p style="margin: 0; font-size: 14px; color: #666666;">
                                            📱 3515173052 | 📧 <a href="mailto:panasabena@gmail.com" style="color: #667eea; text-decoration: none;">panasabena@gmail.com</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px 40px; border-radius: 0 0 8px 8px; text-align: center;">
                            <p style="margin: 0; font-size: 12px; color: #999999; line-height: 1.5;">
                                Este correo fue enviado por Portal Autogestión.<br>
                                Si desea dejar de recibir estos correos, responda este email.
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>
"""
    return html

def obtener_texto_plano(nombre_empresa):
    """Versión texto plano (más limpia que HTML)"""
    return f"""
Hola,

Vimos que {nombre_empresa} ofrece servicios recurrentes a clientes.

Muchas empresas como la suya gestionan documentación, consultas y trámites mediante emails, WhatsApp y planillas. Esto consume tiempo y genera desorden.

Nos especializamos en crear portales de autogestión para clientes donde pueden:
• Descargar documentos (contratos, certificados, facturas)
• Realizar trámites online
• Consultar servicios activos
• Enviar solicitudes organizadas

Todo en un único lugar profesional con su marca.

¿Le interesa ver un demo de 5 minutos?
Puede agendar una reunión aquí: https://calendly.com/alfre-sabena/30min

Saludos,
Alfredo Sabena
Co-founder - Data Analytics | Saas Multitenant
📱 3515173052
📧 panasabena@gmail.com
"""

# ==================== FUNCIÓN PRINCIPAL ====================

def enviar_emails(archivo_csv, test_mode=True):
    """Envía emails con delays para mejor deliverability"""
    
    # Leer contactos
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            # Leer todas las líneas y filtrar comentarios ANTES de csv.DictReader
            lines = file.readlines()
            
            # Filtrar líneas que empiezan con # y líneas vacías
            filtered_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    filtered_lines.append(line)
            
            # Detectar delimitador
            if filtered_lines:
                first_data_line = filtered_lines[1] if len(filtered_lines) > 1 else filtered_lines[0]
                delimiter = ';' if ';' in first_data_line and ',' not in first_data_line else ','
            else:
                delimiter = ','
            
            # Crear reader con las líneas filtradas
            from io import StringIO
            csv_string = ''.join(filtered_lines)
            reader = csv.DictReader(StringIO(csv_string), delimiter=delimiter)
            
            # Limpiar espacios y crear lista de contactos
            contactos = []
            for row in reader:
                email = row.get('email', '').strip()
                nombre_empresa = row.get('nombre_empresa', '').strip()
                
                # Agregar solo si tiene email válido
                if email and '@' in email:
                    contactos.append({
                        'email': email,
                        'nombre_empresa': nombre_empresa
                    })
    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_csv}")
        return
    
    if not contactos:
        print("❌ Error: El CSV está vacío")
        return
    
    required_columns = ['email', 'nombre_empresa']
    if not all(col in contactos[0].keys() for col in required_columns):
        print(f"❌ Error: El CSV debe tener: {', '.join(required_columns)}")
        return
    
    # Modo test
    if test_mode:
        contactos = contactos[:2]
        print(f"\n🔸 MODO TEST: Enviando solo a {len(contactos)} contactos")
    else:
        print(f"\n📧 Enviando a {len(contactos)} contactos...")
        print(f"⏱️  Con delays de {MIN_DELAY}-{MAX_DELAY}s entre emails")
        print(f"⏳ Tiempo estimado: {len(contactos) * ((MIN_DELAY + MAX_DELAY) / 2) / 60:.1f} minutos")
    
    enviados = 0
    errores = 0
    start_time = time.time()
    
    for i, contacto in enumerate(contactos, 1):
        email = contacto['email'].strip()
        nombre_empresa = contacto['nombre_empresa'].strip()
        
        try:
            # Template personalizado
            mensaje_html = obtener_template_html(nombre_empresa)
            mensaje_texto = obtener_texto_plano(nombre_empresa)
            
            # Crear mensaje
            msg = EmailMessage()
            msg['Subject'] = ASUNTO
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            
            # IMPORTANTE: Primero texto, luego HTML
            # Esto ayuda a parecer más "personal"
            msg.set_content(mensaje_texto)
            msg.add_alternative(mensaje_html, subtype="html")
            
            # Enviar
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            print(f"✓ [{i}/{len(contactos)}] Enviado a {email} ({nombre_empresa})")
            enviados += 1
            
            # Delay entre envíos (excepto el último)
            if i < len(contactos):
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"   ⏳ Esperando {delay}s antes del siguiente...")
                time.sleep(delay)
            
        except Exception as e:
            print(f"✗ [{i}/{len(contactos)}] Error al enviar a {email}: {e}")
            errores += 1
    
    # Resumen
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print(f"📊 RESUMEN:")
    print(f"   Enviados exitosamente: {enviados}")
    print(f"   Errores: {errores}")
    print(f"   Tiempo total: {elapsed/60:.1f} minutos")
    print(f"   Promedio por email: {elapsed/len(contactos):.1f}s")
    print("="*60)

# ==================== EJECUCIÓN ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📧 EMAIL MARKETING - ALTA DELIVERABILITY")
    print("="*60)
    print("\n💡 Este script:")
    print("   • Envía desde Gmail directo (va a Principal)")
    print("   • Usa delays entre emails (parece natural)")
    print("   • Template limpio sin headers de marketing")
    print("   • Perfecto para B2B outreach")
    
    if not os.path.exists(ARCHIVO_CSV):
        print(f"\n⚠️  No se encontró: {ARCHIVO_CSV}")
        print("\nCrea un CSV con:")
        print("email,nombre_empresa")
        print("contacto@empresa1.com,Empresa 1 SRL")
        exit(1)
    
    print("\n¿Qué deseas hacer?")
    print("1. MODO TEST (primeros 2 contactos)")
    print("2. Enviar a TODOS (con delays)")
    print("3. Salir")
    
    opcion = input("\nOpción (1-3): ").strip()
    
    if opcion == "1":
        confirmacion = input("\n⚠️  ¿Enviar emails de prueba? (si/no): ").strip().lower()
        if confirmacion == "si":
            enviar_emails(ARCHIVO_CSV, test_mode=True)
    
    elif opcion == "2":
        print("\n⚠️  Esto enviará emails a TODOS los contactos")
        print(f"   Con delays de {MIN_DELAY}-{MAX_DELAY}s entre cada uno")
        confirmacion = input("¿CONFIRMAS? Escribe 'ENVIAR': ").strip()
        if confirmacion == "ENVIAR":
            enviar_emails(ARCHIVO_CSV, test_mode=False)
        else:
            print("❌ Cancelado")
    
    elif opcion == "3":
        print("👋 Hasta luego!")
    
    else:
        print("❌ Opción inválida")

print("\n")
