import time
import subprocess
import sys

# --- CONFIGURACIÓN ---
# IP MAQUINA IA 
# Si queremos probar localmente contra nosotros mismos, usamos 'localhost'
TARGET_IP = "10.0.6.3" 
COMUNIDAD = "public"
USUARIO_DAVID = "montesponcemontalban"
N_INSTANCIA = 1

def consultar_estado_ia():
    try:
        # Comando snmpwalk para buscar la extensión que definimos como 'estado_ia'
        # nsExtendOutputFull es la rama estándar donde SNMP guarda las salidas de scripts
        comando = [
            "snmpwalk", "-v2c", "-c", COMUNIDAD, "-Oqv", 
            TARGET_IP, "nsExtendOutputFull"
        ]
        
        # Ejecutamos el comando y limpiamos la salida
        resultado = subprocess.check_output(comando, stderr=subprocess.DEVNULL).decode().strip()
        
        # Buscamos nuestra etiqueta específica si hay muchas cosas
        # Buscamos el valor.
        if "1" in resultado.split("\n")[-1]: 
            return "PELIGRO"
        elif "0" in resultado:
            return "SEGURO"
        else:
            return "DESCONOCIDO"

    except subprocess.CalledProcessError:
        return "ERROR_CONEXION"

# --- BUCLE PRINCIPAL ---
print(f"--- INICIANDO MONITORIZACIÓN DE IA EN {TARGET_IP} ---")
print("Esperando datos del Agente SNMP...")

estado_anterior = "INICIO"

while True:
    estado_actual = consultar_estado_ia()
    
    fecha = time.strftime("%H:%M:%S")
    
    if estado_actual != estado_anterior:

        if estado_actual == "PELIGRO":
            # AQUÍ ES DONDE SE DISPARA LA ALERTA 
            print(f"[{fecha}] 🚨 ALERTA CRÍTICA: ¡La IA ha detectado una amenaza! 🚨")
            # --- LANZAR AUTO-ESCALADO REMOTO ---
            print(f"[{fecha}] 🚀 Enviando orden de escalado a la máquina de David ({TARGET_IP})...")
            
            # El comando SSH que se ejecutará en la máquina de IA
            # 1. Entra por SSH
            # 2. Escribe en el log de escalado para dejar constancia
            opciones_ssh = [
                "-o", "StrictHostKeyChecking=no",
                "-o", "ConnectTimeout=5",
                "-i", "/home/ayipeton/.ssh/id_rsa"
            ]
            try: 
                cmd = ["ssh"] + opciones_ssh + ["montesponcemontalban@10.0.6.3", "sudo systemctl stop apache2"]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"[{fecha}] PARADO EL SERVICIO WEB")
            except subprocess.CalledProcessError as e:
                print(f"[{fecha}] ❌  ERROR AL PARAR EL SERVICIO WEB: {e.stderr}")

            try:
                # Ejecutamos el comando y esperamos respuesta
                cmd = ["ssh"] + opciones_ssh + ["montesponcemontalban@10.0.6.3", f"python3 /usr/local/bin/autoscale.py {N_INSTANCIA}"]
                resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
                N_INSTANCIA = N_INSTANCIA + 1
                print(f"[{fecha}] RESPUESTA DE DAVID: {resultado.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"[{fecha}] ❌ ERROR AL ESCALAR: {e.stderr}")

            try:
                cmd = ["ssh"] + opciones_ssh + ["montesponcemontalban@10.0.6.3", "echo 0 | sudo tee /tmp/estado_seguridad.txt > /dev/null"]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[{fecha}] ❌  ERROR AL CAMBIAR EL ESTADO DEL LOG: {e.stderr}")

            try:
                cmd = ["ssh"] + opciones_ssh + ["montesponcemontalban@10.0.6.3", "sudo systemctl start apache2"]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"[{fecha}] REANUDADO EL SERVICIO WEB")
            except subprocess.CalledProcessError as e:
                print(f"[{fecha}] ❌   ERROR AL REANUDAR EL SERVICIO WEB: {e.stderr}")
                
        elif estado_actual == "SEGURO" and estado_anterior == "PELIGRO":
            print(f"[{fecha}] ✅ Sistema Estable.  No hay alertas", end="\r")
        elif estado_actual == "ERROR_CONEXION":
            print(f"[{fecha}] ❌ No se puede conectar con la VM de IA (¿Está encendida?)", end="\r")
    
    # 3. FEEDBACK VISUAL (Para saber que sigue vivo)
    if estado_actual == "SEGURO":
        print(f"[{fecha}] ✅ Sistema Estable...", end="\r")
    elif estado_actual == "PELIGRO":
        print(f"[{fecha}] ⚠️  ATAQUE EN CURSO...", end="\r")

    # 4. ACTUALIZAMOS LA MEMORIA
    estado_anterior = estado_actual
    time.sleep(1) # Preguntar cada 1 segundos
