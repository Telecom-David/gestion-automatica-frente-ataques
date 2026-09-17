import joblib
import numpy as np
import time
import os
import warnings # <--- NUEVO: Necesario para limpiar la consola

# --- SILENCIADOR DE AVISOS ---
# Esto elimina el texto "UserWarning" feo de la consola
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURACIÓN DE CONEXIÓN CON RODRI Y ADRIÁN ---
# [INTEGRACIÓN CON maquina 2]: Cuando M2 termine, se debe de cambiar a "/var/log/apache2/access.log"
ARCHIVO_LOGS = "simulacion_logs.txt" 
# [INTEGRACIÓN CON MAQUINA 3]: 
# Archivo "Buzón" para comunicación asíncrona con el agente SNMP.
# Contenido: "1" (Alerta/Ataque) | "0" (Normal).

ARCHIVO_ALERTA = "/tmp/estado_seguridad.txt" 
# ----------------------------------------------------

print("🔥 SISTEMA DE DEFENSA IA INICIADO 🔥")

# Cargar el modelo pre-entrenado
if not os.path.exists('cerebro_ia.pkl'):
    print("Error: No encuentro el cerebro. Ejecuta primero 'entrenar_modelo.py'")
    exit()

modelo = joblib.load('cerebro_ia.pkl')

print(f"Escribiendo alertas para Adrián en: {ARCHIVO_ALERTA}")
print("   (Pulsa Ctrl+C para detener)")

# Usamos try-except para que al cerrar con Ctrl+C no salga error
try:
    while True:

        # 1. SIMULAMOS LEER UN DATO NUEVO (Esto luego habra que cambiarlo con un patron de logs de la MAQUINA 2)
        # Generamos un dato aleatorio: [Tiempo respuesta, Tamaño paquete]
        
        # --- MEJORA TÉCNICA ---
        # Usamos abs() para evitar tiempos negativos (imposible en física).
        # Usamos desviación 0.1 y 100 para simular una red estable (como en el entrenamiento).
        tiempo_simulado = abs(np.random.normal(0.5, 0.1))
        tamano_simulado = abs(np.random.normal(500, 100))
        
        # TRUCO: Inyectamos un ataque el 10% de las veces para probar que la alerta roja funciona
        if np.random.random() < 0.1:
            tiempo_simulado += 3.0   # Latencia muy alta
            tamano_simulado += 2000  # Paquete muy pesado
        
        dato_real = [[tiempo_simulado, tamano_simulado]]
        
        # 2. PREGUNTAMOS A LA IA
        prediccion = modelo.predict(dato_real)
        # En IsolationForest: -1 es anomalía (ataque), 1 es normal
        es_ataque = True if prediccion[0] == -1 else False
        
        # 3. AVISAMOS A ADRIÁN (Escribimos en el archivo)
        with open(ARCHIVO_ALERTA, "w") as f:
            if es_ataque:
                f.write("1")
            else:
                f.write("0")

        if es_ataque:

            print(f"\033[91m🚨 ¡ATAQUE DETECTADO! Tiempo: {tiempo_simulado:.2f}s | Peso: {tamano_simulado:.0f}B\033[0m")
            # El archivo ya tiene un "1", así que nos quedamos quietos 4s para que M3 lo lea
            time.sleep(3)
        else:

            print(f"\033[92m✅ Tráfico normal.    Tiempo: {tiempo_simulado:.2f}s | Peso: {tamano_simulado:.0f}B\033[0m")
            time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Vigilancia detenida correctamente.")
