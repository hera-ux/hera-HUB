#!/bin/bash

# Función para verificar si nmap está instalado
check_nmap_installed() {
    if ! command -v nmap &> /dev/null; then
        echo "nmap no esta instalado. Instalando..."
        
        # Detectar la distribución de Linux
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
        fi
        
        # Instalar nmap dependiendo de la distribución
        case "$DISTRO" in
            "arch" | "manjaro" )
                sudo pacman -Syu --noconfirm nmap
                ;;
            "debian" | "ubuntu" | "linuxmint" )
                sudo apt update && sudo apt install -y nmap
                ;;
            "fedora" )
                sudo dnf install -y nmap
                ;;
            "centos" | "rhel" )
                sudo yum install -y nmap
                ;;
            * )
                echo "Distribucion no soportada para instalacion automatica de nmap."
                exit 1
                ;;
        esac
    else
        echo "nmap ya esta instalado."
    fi
}

# Verificar si se ejecuta como root
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        echo "Este script necesita permisos de root para detectar sistemas operativos."
        echo "Ejecuta: sudo $0"
        exit 1
    fi
}

# Llamar a la función para verificar permisos de root
check_root

# Llamar a la función para verificar si nmap está instalado
check_nmap_installed

# Obtener la IP de la puerta de enlace (router)
router_ip=$(ip route | grep default | awk '{print $3}')

# Verifica si se obtuvo la IP correctamente
if [ -z "$router_ip" ]; then
    echo "No se pudo obtener la IP del router."
    exit 1
fi

echo "La IP del router es: $router_ip"

# Extraer la red local (en formato 192.168.1.0/24)
lan_ip=$(echo $router_ip | sed 's/\.[0-9]*$/.0/')

echo "======================================================="
echo "Paso 1: Escaneando hosts activos en la red: $lan_ip/24"
echo "======================================================="

# Realizar un escaneo inicial para encontrar hosts activos
hosts_activos=$(nmap -sn $lan_ip/24 | grep "Nmap scan report for" | awk '{print $5}')

# Contar hosts encontrados
num_hosts=$(echo "$hosts_activos" | wc -l)
echo "Se encontraron $num_hosts hosts activos"
echo ""

echo "======================================================="
echo "Paso 2: Detectando sistema operativo de cada host"
echo "======================================================="
echo ""

# Crear archivo temporal para guardar resultados
resultado_temp="/tmp/nmap_os_scan_$$.txt"
> $resultado_temp

contador=0
# Para cada host activo, realizar detección de OS
for ip in $hosts_activos; do
    contador=$((contador + 1))
    echo "[$contador/$num_hosts] Analizando: $ip"
    
    # Realizar detección de OS con timeout
    os_info=$(timeout 30s nmap -O --osscan-guess $ip 2>/dev/null)
    
    # Extraer información relevante
    mac=$(echo "$os_info" | grep "MAC Address:" | cut -d' ' -f3-)
    os_running=$(echo "$os_info" | grep "Running:" | cut -d':' -f2- | xargs)
    os_details=$(echo "$os_info" | grep "OS details:" | cut -d':' -f2- | xargs)
    device_type=$(echo "$os_info" | grep "Device type:" | cut -d':' -f2- | xargs)
    
    # Guardar en archivo temporal
    echo "-------------------------------------------------------" >> $resultado_temp
    echo "IP: $ip" >> $resultado_temp
    [ ! -z "$mac" ] && echo "MAC: $mac" >> $resultado_temp
    [ ! -z "$device_type" ] && echo "Tipo: $device_type" >> $resultado_temp
    [ ! -z "$os_running" ] && echo "OS: $os_running" >> $resultado_temp
    [ ! -z "$os_details" ] && echo "Detalles: $os_details" >> $resultado_temp
    
    # Si no se detectó nada
    if [ -z "$os_running" ] && [ -z "$os_details" ]; then
        echo "OS: No se pudo detectar (firewall o puertos cerrados)" >> $resultado_temp
    fi
    echo "" >> $resultado_temp
done

echo ""
echo "======================================================="
echo "RESUMEN DE DISPOSITIVOS ENCONTRADOS"
echo "======================================================="
echo ""

# Mostrar resultados
cat $resultado_temp

# Preguntar si guardar resultados
echo "Deseas guardar los resultados en un archivo? (s/n)"
read -r respuesta

if [[ "$respuesta" =~ ^[Ss]$ ]]; then
    archivo_salida="scan_red_$(date +%Y%m%d_%H%M%S).txt"
    cp $resultado_temp "$archivo_salida"
    echo "Resultados guardados en: $archivo_salida"
fi

# Limpiar archivo temporal
rm -f $resultado_temp

echo ""
echo "Presiona Enter para salir..."
read
