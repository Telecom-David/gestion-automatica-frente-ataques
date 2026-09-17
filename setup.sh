#!/bin/bash

# --- 1. Actualizar el sistema ---
echo "Actualizando repositorios y sistema..."
sudo apt-get update -y

# --- 2. Instalar Herramientas Básicas ---
echo "Instalando herramientas básicas (Git, Curl, Zip, Python)..."
sudo apt-get install -y git curl wget unzip software-properties-common python3 python3-pip

# --- 3. Instalar Servidor Web (Apache) ---
echo "Instalando Apache Web Server..."
sudo apt-get install -y apache2
sudo systemctl enable apache2
sudo systemctl start apache2

# Crear un index.html de prueba para saber qué máquina es
HOSTNAME=$(hostname)
IP=$(hostname -I)
sudo tee /var/www/html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estado del Servidor</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; }
        h1 { color: #333; }
        p { color: #666; font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>¡Hola! Esta es la máquina: $HOSTNAME</h1>
    <p>La IP de la red interna es: <b>$IP</b></p>
    <hr>
    <p><em>Servidor listo para trabajar.</em></p>
</body>
</html>
EOF

# --- 4. Instalar Base de Datos (MariaDB) ---
echo "Instalando Base de Datos MariaDB..."
sudo apt-get install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb

# --- 5. Instalar Agente SNMP (Para Monitorización) ---
echo "Instalando Agente SNMP..."
sudo apt-get install -y snmp snmpd libsnmp-dev

echo "¡Instalación Completada! Tu entorno base está listo."
echo "   - Web: http://$IP"
echo "   - DB: MariaDB corriendo"
echo "   - Python: $(python3 --version)"
