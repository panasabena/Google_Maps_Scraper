#!/usr/bin/env python3
"""
Script para completar datos faltantes (teléfono, web, email)
Hace clic en cada lugar de Google Maps para obtener información detallada
"""
import sys
import pandas as pd
import undetected_chromedriver as uc
from pathlib import Path
import time
import logging
from datetime import datetime

# Importar módulos del scraper
from config import CONFIG, USER_AGENTS
from detail_extractor import DetailExtractor
from utils import setup_logging, delay_aleatorio


def completar_datos_faltantes():
    """
    Completa datos faltantes en el archivo Excel existente
    """
    # Setup logging
    logger = setup_logging('logs')
    
    excel_file = Path('resultados/google_maps_results.xlsx')
    
    if not excel_file.exists():
        print("❌ No se encontró el archivo de resultados")
        print("   Primero ejecuta: python main.py")
        return
    
    # Cargar datos
    print("\n" + "="*60)
    print("📞 COMPLETAR DATOS FALTANTES")
    print("="*60)
    
    df = pd.read_excel(excel_file)
    print(f"\n📊 Lugares cargados: {len(df)}")
    
    # Analizar qué falta (excluir los que ya están marcados como "N/A")
    sin_telefono = df[
        (df['telefono'].isna() | (df['telefono'] == '')) & 
        (df['telefono'] != 'N/A')
    ]
    sin_web = df[
        (df['sitio_web'].isna() | (df['sitio_web'] == '')) & 
        (df['sitio_web'] != 'N/A')
    ]
    
    print(f"📞 Sin teléfono: {len(sin_telefono)} (pendientes de verificar)")
    print(f"🌐 Sin sitio web: {len(sin_web)} (pendientes de verificar)")
    
    # Contar los que ya se verificaron pero no tienen datos
    ya_verificados = len(df[df['telefono'] == 'N/A'])
    if ya_verificados > 0:
        print(f"✓ Ya verificados sin datos: {ya_verificados}")
    
    if len(sin_telefono) == 0 and len(sin_web) == 0:
        print("\n✅ ¡Todos los lugares ya fueron verificados!")
        print("   (Algunos pueden tener 'N/A' si no tenían datos en Google Maps)")
        return
    
    # Preguntar al usuario
    print("\n⚠️  ADVERTENCIA:")
    print(f"   Esto tomará aproximadamente {len(sin_telefono) * 5 / 60:.1f} minutos")
    print(f"   (5-8 segundos por lugar)")
    
    respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
    if respuesta != 's':
        print("❌ Cancelado")
        return
    
    # Inicializar navegador
    print("\n🚀 Inicializando navegador...")
    try:
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={USER_AGENTS[0]}')
        
        driver = uc.Chrome(options=options, use_subprocess=True)
        extractor = DetailExtractor(driver)
        
        print("✅ Navegador inicializado\n")
        
    except Exception as e:
        print(f"❌ Error inicializando navegador: {e}")
        return
    
    # Procesar cada lugar SIN datos
    completados = 0
    telefnos_encontrados = 0
    webs_encontradas = 0
    emails_encontrados = 0
    
    print("="*60)
    print("🔍 EXTRAYENDO DATOS DETALLADOS")
    print("="*60 + "\n")
    
    inicio = datetime.now()
    
    for idx, row in sin_telefono.iterrows():
        try:
            url = row['url_google_maps']
            if not url or pd.isna(url):
                continue
            
            nombre = row['nombre'][:40] if row['nombre'] else 'Sin nombre'
            print(f"[{completados+1}/{len(sin_telefono)}] {nombre}...", end=' ', flush=True)
            
            # Extraer datos detallados
            datos_detallados = extractor.extraer_datos_detallados(url)
            
            # Actualizar DataFrame
            actualizado = False
            
            if datos_detallados.get('telefono'):
                df.at[idx, 'telefono'] = datos_detallados['telefono']
                telefnos_encontrados += 1
                print(f"📞 {datos_detallados['telefono']}", end=' ')
                actualizado = True
            else:
                # Marcar como N/A si no se encontró teléfono
                df.at[idx, 'telefono'] = 'N/A'
            
            if datos_detallados.get('sitio_web'):
                df.at[idx, 'sitio_web'] = datos_detallados['sitio_web']
                webs_encontradas += 1
                if not actualizado:
                    print(f"🌐 Web", end=' ')
                actualizado = True
            else:
                # Marcar como N/A si no se encontró sitio web
                df.at[idx, 'sitio_web'] = 'N/A'
            
            if datos_detallados.get('email'):
                df.at[idx, 'email'] = datos_detallados['email']
                emails_encontrados += 1
                if not actualizado:
                    print(f"📧 Email", end=' ')
                actualizado = True
            else:
                # Marcar como N/A si no se encontró email
                df.at[idx, 'email'] = 'N/A'
            
            if not actualizado:
                print("⚠️  Sin datos (marcado N/A)", end='')
            
            print()  # Nueva línea
            
            completados += 1
            
            # Checkpoint cada 10 lugares
            if completados % 10 == 0:
                df.to_excel(excel_file, index=False)
                csv_file = excel_file.with_suffix('.csv')
                df.to_csv(csv_file, index=False, encoding='utf-8-sig')
                
                tiempo_transcurrido = (datetime.now() - inicio).seconds
                promedio = tiempo_transcurrido / completados if completados > 0 else 0
                restantes = len(sin_telefono) - completados
                tiempo_estimado = (restantes * promedio) / 60
                
                print(f"\n💾 Checkpoint guardado: {completados} procesados")
                print(f"📊 Encontrados: {telefnos_encontrados} teléfonos, {webs_encontradas} webs")
                print(f"⏱️  Tiempo estimado restante: {tiempo_estimado:.1f} minutos\n")
            
            # Delay entre lugares (2-4 segundos)
            delay_aleatorio((2, 4))
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrumpido por usuario")
            print("💾 Guardando progreso...")
            break
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            logging.error(f"Error procesando {nombre}: {str(e)}")
            continue
    
    # Guardar final
    print("\n" + "="*60)
    print("💾 GUARDANDO RESULTADOS FINALES")
    print("="*60 + "\n")
    
    df.to_excel(excel_file, index=False)
    csv_file = excel_file.with_suffix('.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ Excel guardado: {excel_file}")
    print(f"✅ CSV guardado: {csv_file}")
    
    # Cerrar navegador
    driver.quit()
    
    # Estadísticas finales
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS FINALES")
    print("="*60 + "\n")
    
    # Contar excluyendo N/A
    con_telefono = len(df[(df['telefono'].notna()) & (df['telefono'] != 'N/A') & (df['telefono'] != '')])
    con_web = len(df[(df['sitio_web'].notna()) & (df['sitio_web'] != 'N/A') & (df['sitio_web'] != '')])
    con_email = len(df[(df['email'].notna()) & (df['email'] != 'N/A') & (df['email'] != '')])
    
    # Contar N/A (verificados pero sin datos)
    na_telefono = len(df[df['telefono'] == 'N/A'])
    na_web = len(df[df['sitio_web'] == 'N/A'])
    na_email = len(df[df['email'] == 'N/A'])
    
    print(f"Total de lugares: {len(df)}")
    print(f"\nCon datos encontrados:")
    print(f"  📞 Con teléfono: {con_telefono} ({con_telefono/len(df)*100:.1f}%)")
    print(f"  🌐 Con sitio web: {con_web} ({con_web/len(df)*100:.1f}%)")
    print(f"  📧 Con email: {con_email} ({con_email/len(df)*100:.1f}%)")
    
    print(f"\nVerificados sin datos (N/A):")
    print(f"  📞 Sin teléfono: {na_telefono}")
    print(f"  🌐 Sin sitio web: {na_web}")
    print(f"  📧 Sin email: {na_email}")
    
    print(f"\nNuevos datos encontrados en esta ejecución:")
    print(f"  📞 Teléfonos: {telefnos_encontrados}")
    print(f"  🌐 Sitios web: {webs_encontradas}")
    print(f"  📧 Emails: {emails_encontrados}")
    
    tiempo_total = (datetime.now() - inicio).seconds / 60
    print(f"\n⏱️  Tiempo total: {tiempo_total:.1f} minutos")
    print(f"⚡ Promedio: {tiempo_total*60/completados:.1f} segundos por lugar")
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        completar_datos_faltantes()
    except Exception as e:
        logging.error(f"Error fatal: {str(e)}", exc_info=True)
        print(f"\n❌ Error fatal: {str(e)}")
        sys.exit(1)
