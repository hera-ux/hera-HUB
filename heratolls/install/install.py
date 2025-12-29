import subprocess
import os

# Listas de aplicaciones
pacman_apps = ["chromium", "pavucontrol", "discord"]
yay_apps = ["spotify", "vscodium", "spotdl"]

# Detectar el usuario real (no root)
usuario_real = os.getenv("SUDO_USER") or os.getenv("USER")

print("¿Tienes yay instalado?")
yay = input("si/no: ").lower()

if yay == "si":
    print("Perfecto, continuando...\n")

elif yay == "no":
    print("Instalando yay...\n")

    # Instalar dependencias necesarias
    subprocess.run(["pacman", "-S", "git", "base-devel", "--needed", "--noconfirm"], check=True)

    # Eliminar carpeta 'yay' si ya existe
    if os.path.exists("yay"):
        print("El directorio 'yay' ya existe, eliminándolo para recompilar...")
        subprocess.run(["rm", "-rf", "yay"])

    # Clonar y preparar yay
    subprocess.run(["git", "clone", "https://aur.archlinux.org/yay.git"], check=True)
    subprocess.run(["chown", "-R", f"{usuario_real}:{usuario_real}", "yay"], check=True)

    os.chdir("yay")

    # Ejecutar makepkg como usuario normal
    subprocess.run(["sudo", "-u", usuario_real, "bash", "-c", "makepkg -si --noconfirm"], check=True)

    os.chdir("..")
    print("✓ yay compilado correctamente\n")

else:
    print("Respuesta no válida. Escribe 'si' o 'no'.")
    exit(1)

# Elección del gestor de paquetes
print("¿Qué gestor de paquetes quieres usar?")
manager = input("pacman/yay: ").lower()
print(f"Has elegido como gestor: {manager}\n")

if manager == "pacman":
    print(f"Este gestor contiene las siguientes apps: {pacman_apps}\n")
elif manager == "yay":
    print(f"Este gestor contiene las siguientes apps: {yay_apps}\n")
else:
    print("Gestor no válido.")
    exit(1)

# Instalación según el gestor
if manager == "pacman":
    print("=== Instalando desde repositorios oficiales ===\n")
    for app in pacman_apps:
        print(f"Instalando {app}...")
        resultado = subprocess.run(["pacman", "-S", app, "--noconfirm"])
        if resultado.returncode == 0:
            print(f"✓ {app} instalado correctamente\n")
        else:
            print(f"✗ Error instalando {app}\n")

elif manager == "yay":
    print("=== Instalando desde AUR ===\n")
    for app in yay_apps:
        print(f"Instalando {app}...")
        resultado = subprocess.run(["sudo", "-u", usuario_real, "yay", "-S", app, "--noconfirm"])
        if resultado.returncode == 0:
            print(f"✓ {app} instalado correctamente\n")
        else:
            print(f"✗ Error instalando {app}\n")
