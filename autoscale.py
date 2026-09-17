import psutil
import time
import os
import logging

# --- CONFIGURACIÓN ---
UMBRAL_CPU = 50.0  # Umbral bajo (50%) para probar fácil
LOG_FILE = "/var/log/gar_scaling.log"

# Configurar logs
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def simular_arranque_instancia():
    print(" [!] ALERTA: CPU alta. Iniciando escalado...")
    logging.info("ALERTA_ESCALADO: CPU supera umbral. Iniciando nueva instancia...")
    
    time.sleep(2) # Simulación de despliegue
    
    # Simular una nueva IP
    nueva_ip = f"10.0.6.{os.getpid() % 255}"
    mensaje = f"ESCALADO_COMPLETADO: Nueva instancia activa en {nueva_ip}"
    
    print(f" [OK] {mensaje}")
    logging.info(mensaje)

def vigilar():
    print(f"--- Monitor de Escalado Activo (Umbral: {UMBRAL_CPU}%) ---")
    
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            # print(f"CPU: {cpu}%") # Comentado para no llenar el log de systemd

            if cpu > UMBRAL_CPU:
                simular_arranque_instancia()
                time.sleep(10) # Enfriamiento
                
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    vigilar()
