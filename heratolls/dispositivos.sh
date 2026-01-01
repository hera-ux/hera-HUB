#!/bin/bash

# Función para verificar si nmap está instalado
check_nmap_installed() {
    if ! command -v nmap &> /dev/null; then
        echo "nmap no está instalado. Instalando..."
        
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
                echo "Distribución no soportada para instalación automática de nmap."
                exit 1
                ;;
        esac
    else
        echo "nmap ya está instalado."
    fi
}

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

# Realizar un escaneo con nmap en la red local
echo "Escaneando la red local: $lan_ip/24"
nmap -sn $lan_ip/24
c
