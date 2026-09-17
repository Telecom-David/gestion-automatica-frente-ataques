import joblib
import numpy as np
import time
import os
import warnings # Necesario para limpiar la consola

# --- SILENCIADOR DE AVISOS ---
# Esto elimina el texto "UserWarning" de la consola
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURACIÓN DE CONEXIÓN CON Monitorizacion Y Automatizacion ---
# [INTEGRACIÓN CON Automatizacion]: se cambio de prueba local a "/var/log/apache2/access.log"
ARCHIVO_LOGS = "/var/log/apache2/access.log"
# [INTEGRACIÓN CON Monitorizacion]: 
# Archivo "Buzón" para comunicación asíncrona con el agente SNMP.
# Contenido: "1" (Alerta/Ataque) | "0" (Normal).

ARCHIVO_ALERTA = "/tmp/estado_seguridad.txt" 
# ----------------------------------------------------

print(" SISTEMA DE DEFENSA IA INICIADO ")

# Cargar el modelo pre-entrenado
if not os.path.exists('cerebro_ia.pkl'):
    print("Error: No encuentro el cerebro. Ejecuta primero 'entrenar_modelo.py'")
    exit()

modelo = joblib.load('cerebro_ia.pkl')


print(f"Escucando log reales de Rodri en: {ARCHIVO_LOGS}")
print(f"Escribiendo alertas para Adrián en: {ARCHIVO_ALERTA}")
print("   (Pulsa Ctrl+C para detener)")

# COMO EL ARCHIVO CAMBIA CONSTANTEMENTE CON LOS LOGS DEBEMOS DE LEER LINEA A LINEA SEGUN
#ENTREN LOS DATOS

def seguir_log(archivo):
    archivo.seek(0, os.SEEK_END) #vamos al fianl del archivo
    while True:
        linea = archivo.readline()
        if not linea:
            time.sleep(0.1)
            continue
        yield linea 



# Usamos try-except para que al cerrar con Ctrl+C no salga error
try:
    
    while not os.path.exists(ARCHIVO_LOGS):
        print("Esperando trafico del servidor web...")
        time.sleep(2)
    
    with open(ARCHIVO_LOGS, "r") as f:

        log_lines = seguir_log(f)


        for linea in log_lines:

            try:

                #REALIZAMOS LA LINEA DE DATOS
                partes = linea.split('"')

                #Por si hay lineas vacias
                if len(partes) < 3:
                    continue

                # El tamaño siempre es la ultima palabra de la linea de Apache
                datos_servidor = partes[2].split()

                #Si sale un guion el tamaño es 0
                if len(datos_servidor) < 2:
                    continue 

                dato_bytes_texto = datos_servidor[1]

                if dato_bytes_texto == '-':
                    tamano_real = 0.0 # Corregido typo (ñ -> n) para que coincida abajo
                else:
                    tamano_real = float(dato_bytes_texto)

                # 2. GESTIÓN DEL TIEMPO (LATENCIA)
                # Como Apache no nos da el tiempo sin config avanzada,
                # simulamos un tiempo "estable" para que la IA no se confunda.
                # PERO: Usamos el TAMAÑO REAL para detectar el ataque.

                tiempo_simulado = abs(np.random.normal(0.5, 0.1))
        
                dato_para_ai = [[tiempo_simulado, tamano_real]]
        
                # 2. PREGUNTAMOS A LA IA
                prediccion = modelo.predict(dato_para_ai)

                # En IsolationForest: -1 es anomalía (ataque), 1 es normal
                es_ataque = True if prediccion[0] == -1 else False
        
                # 3. AVISAMOS A Monitorizacion (Escribimos en el archivo)
                with open(ARCHIVO_ALERTA, "w") as f:
                    if es_ataque:
                        f.write("1")
                    else:
                        f.write("0")

                if es_ataque:

                    print(f"\033[91m🚨 ¡ATAQUE DETECTADO! Tiempo: {tiempo_simulado:.2f}s | Peso: {tamano_real:.0f}B\033[0m")
                    # El archivo ya tiene un "1", así que nos quedamos quietos 1.5s para que Monitorizacion lo lea
                    time.sleep(2)
                else:

                    print(f"\033[92m✅ Tráfico normal.    Tiempo: {tiempo_simulado:.2f}s | Peso: {tamano_real:.0f}B\033[0m")
                    time.sleep(1)

            except ValueError:

                continue

except KeyboardInterrupt:
    print("\n🛑 Vigilancia detenida correctamente.")
