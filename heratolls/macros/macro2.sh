#!/bin/bash

echo "Macro iniciada en 3 segundos. Cambia a la ventana donde quieres usar la macro."
echo "Presiona Ctrl+C para detener."
sleep 3

while true; do
    echo "[$(date +%H:%M:%S)] Presionando C..."
    ydotool key 46:1 46:0  # C press
    
    echo "[$(date +%H:%M:%S)] Esperando 10 segundos..."
    sleep 10
    
    echo "[$(date +%H:%M:%S)] Presionando X durante 10 segundos..."
    ydotool key 45:1  # X down
    sleep 10
    ydotool key 45:0  # X up
    
    echo "[$(date +%H:%M:%S)] Esperando 80 segundos antes de repetir..."
    sleep 80
done
