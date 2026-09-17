import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("Iniciando entrenamiento del modelo de IA...")

# 1. CARGA DE DATOS HISTÓRICOS
# Leemos el dataset generado en la fase anterior.
df = pd.read_csv('datos_entrenamiento.csv')

# Seleccionamos las 'features' (características) que el modelo usará para juzgar.
# La IA aprenderá la correlación entre Tiempo y Tamaño.
datos_aprendizaje = df[['tiempo_respuesta', 'tamano_paquete']]

# 2. CONFIGURACIÓN DEL ALGORITMO (ISOLATION FOREST)
# Este algoritmo es ideal para Ciberseguridad (Detección de Anomalías).
# No busca "patrones de virus conocidos", sino que busca "comportamientos que se desvían de la norma".
# contamination=0.1: Estimamos que aprox el 10% del tráfico podría ser malicioso.
modelo = IsolationForest(contamination=0.1, random_state=42)

# 3. ENTRENAMIENTO (FITTING)
# El modelo analiza la geometría de los datos y traza una frontera entre "Normal" y "Anómalo".
modelo.fit(datos_aprendizaje)

# 4. SERIALIZACIÓN DEL MODELO
# Guardamos el "cerebro" entrenado en un archivo binario (.pkl).
# Esto permite usar la IA en el script de detección sin tener que re-entrenar cada vez.
archivo_modelo = 'cerebro_ia.pkl'
joblib.dump(modelo, archivo_modelo)
print(f"Modelo entrenado y serializado en: {archivo_modelo}")
print("   Listo para ser desplegado en el script de detección en vivo.")
