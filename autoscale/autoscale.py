#!/usr/bin/env python3
import time
import sys
import os
from datetime import datetime

# Archivo donde dejaremos constancia de que hemos actuado
LOG_FILE = "/tmp/historial_escalado.txt"

def log_msg(mensaje):
    """Escribe en pantalla y en el archivo de registro"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto_final = f"[{timestamp}] {mensaje}"
    
    print(texto_final)
    
    # Guardamos en el fichero para tener pruebas forenses
    try:
        with open(LOG_FILE, "a") as f:
            f.write(texto_final + "\n")
    except Exception as e:
        print(f"Error escribiendo log: {e}")

def main():
    N_INSTANCIA = sys.argv[1]
    print("\n" + "!"*50)
    log_msg("RECIBIDA ORDEN DE ESCALADO DE EMERGENCIA")
    print("!"*50 + "\n")

    # 1. Simulación: Provisionar Servidor
    log_msg("Contactando con API del Cloud Provider...")
    time.sleep(1.5) # Simular tiempo de espera de red
    log_msg(f"Desplegando nueva instancia 'web-server-rescue-{N_INSTANCIA}'...")
    time.sleep(2)   # Simular arranque de máquina
    log_msg("Instancia iniciada y operativa.")

    # 2. Simulación: Configurar Red
    log_msg("Actualizando reglas del Balanceador de Carga...")
    time.sleep(1)
    log_msg("Balanceador reconfigurado. Distribuyendo tráfico.")

    # 3. Finalización
    print("\n" + "="*50)
    log_msg("PROTOCOLO DE DEFENSA COMPLETADO CON ÉXITO.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
