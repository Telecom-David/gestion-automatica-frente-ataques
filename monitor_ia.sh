#!/bin/bash
# Este script lee el archivo que genera la IA 
# Ruta acordada 
ARCHIVO="/home/montesponcemontalban/Trabajo-GAR/modulo_ia/estado_seguridad.txt"

if [ -f "$ARCHIVO" ]; then
    cat "$ARCHIVO"
else
    echo "0" # Si no existe, asumimos que todo está bien por seguridad
fi
