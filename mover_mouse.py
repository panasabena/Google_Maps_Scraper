#!/usr/bin/env python3
"""
Script para mover el mouse periódicamente.
Útil para evitar que la computadora entre en modo de suspensión.
"""

import pyautogui
import time
import sys

# Configuración
INTERVALO = 15  # segundos entre movimientos
DISTANCIA = 50  # píxeles a mover

# Configurar failsafe (mover mouse a esquina superior izquierda detiene el script)
pyautogui.FAILSAFE = True

def mover_mouse():
    """Mueve el mouse en un patrón simple."""
    try:
        # Obtener posición actual
        x_actual, y_actual = pyautogui.position()
        
        # Mover a posición relativa
        pyautogui.moveRel(DISTANCIA, 0, duration=0.5)  # Derecha
        time.sleep(0.5)
        pyautogui.moveRel(-DISTANCIA, 0, duration=0.5)  # Regresa
        
        print(f"Mouse movido a: {pyautogui.position()} | Hora: {time.ctime()}")
        
    except pyautogui.FailSafeException:
        print("Failsafe activado: mouse en esquina. Saliendo...")
        sys.exit(0)

def main():
    print("=" * 50)
    print("Script de movimiento de mouse iniciado")
    print(f"Intervalo: {INTERVALO} segundos")
    print("Presiona Ctrl+C para detener")
    print("Lleva el mouse a la esquina superior izquierda para emergencia")
    print("=" * 50)
    
    contador = 0
    
    try:
        while True:
            mover_mouse()
            contador += 1
            print(f"Ciclo completado: {contador}")
            
            # Esperar hasta el próximo movimiento
            for i in range(INTERVALO):
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n¡Script detenido por el usuario!")
        print(f"Total de ciclos: {contador}")

if __name__ == "__main__":
    main()
