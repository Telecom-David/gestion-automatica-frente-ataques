import pandas as pd 
import numpy as np

print("Gerando datos para entrenar al modelo...")

#Preparamos los datos utilizando una distribucion normal porque el trafico
#de una red nunca es constante

# Para asegurar el aprendizaje, le enseñamos las reglas de forma ordenada
np.random.seed(42)

data = {

    #Hacemos el tiempo que tarda en responder (segundos)
    'tiempo_respuesta' : np.random.normal (loc = 0.5, scale = 0.1, size = 1000),

    #Tamaño del paquete de datos (Bytes)
    'tamano_paquete' : np.random.normal(loc = 500, scale = 100, size = 1000),

    #Vamos a distinguir 0 si es trafico normal y 1 si es un ataque 10% ataques
    'es_ataque' : np.random.choice([0, 1], 1000, p = [0.9, 0.1])

}

#Creamos el DataFrame
df = pd.DataFrame(data)

# Para que el algoritmo de Machine Learning detecte los ataques, estos deben
# diferenciarse matemáticamente del tráfico normal, DARLE UNA PSITA CLARA

# 1) Podemos hacer una simulacion de ataques de Denegacion de Servicio que 
# bloqueen el servidor que provoquen una latencia alta

df.loc[df['es_ataque'] == 1, 'tiempo_respuesta'] += 2.0 # consideramos latencia alta 2 seg

# 2) Podemos hacer una simulacion de Payload Malicioso donde el atacante envia scripts
# o conusltas largas dentro del paquete.

df.loc[df['es_ataque'] == 1, 'tamano_paquete'] += 1000


#Guardamos el dataset procesado
archivo_salida = 'datos_entrenamiento.csv'
df.to_csv(archivo_salida, index=False)
print(f" Dataset generado exitosamente: {archivo_salida}")
print("   Nota: Los ataques se han marcado como outliers en tiempo y tamaño.")

