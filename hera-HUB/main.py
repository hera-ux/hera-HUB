import subprocess
import sys
import os
import time
import tty
import termios

def mostrar_menu_principal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    print("\n" + "="*50)
    print("██╗  ██╗███████╗██████╗  █████╗ ")
    print("██║  ██║██╔════╝██╔══██╗██╔══██╗")
    print("███████║█████╗  ██████╔╝███████║")
    print("██╔══██║██╔══╝  ██╔══██╗██╔══██║")
    print("██║  ██║███████╗██║  ██║██║  ██║")
    print("╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝")
    print("\n" + "="*50)
    print("herramientas")
    print("="*50)
    print("1. Generador de Contraseñas")
    print("2. Macros")
    print("3. instalador(solo arch)")
    print("4. sherlock(basico W.I.P)")
    print("0. Salir")
    print("="*50)
    print("i<3L")
    print("="*50)

def mostrar_menu_macros():
    print("\n" + "="*50)
    print("MENÚ DE MACROS")
    print("="*50)
    print("1. gpo dinero")
    print("2. Escanear red")
    print("3. Escanear red + OS (requiere sudo)")
    print("0. Volver al menú principal")
    print("="*50)

def ejecutar_python(ruta):
    """Ejecuta un archivo Python"""
    try:
        subprocess.run([sys.executable, ruta])
    except FileNotFoundError:
        print(f"\n Error: No se encontró el archivo '{ruta}'")
        input("\nPresiona Enter para continuar...")
    except Exception as e:
        print(f"\n Error al ejecutar: {e}")
        input("\nPresiona Enter para continuar...")

def ejecutar_script(ruta, usar_sudo=False):
    """Ejecuta un script bash (.sh) con o sin sudo"""
    try:
        if usar_sudo:
            print("\n[!] Este script requiere permisos de administrador")
            print("Se te pedira tu contrasena de sudo...\n")
            time.sleep(1)
            
            if os.name == 'nt':  # Windows
                print("Error: sudo no está disponible en Windows")
                input("\nPresiona Enter para continuar...")
                return
            else:  # Linux/Mac
                subprocess.run(['sudo', 'bash', ruta])
        else:
            if os.name == 'nt':  # Windows
                subprocess.run(['bash', ruta])
            else:  # Linux/Mac
                subprocess.run(['bash', ruta])
    except FileNotFoundError:
        print(f"\n Error: No se encontró el archivo '{ruta}'")
        input("\nPresiona Enter para continuar...")
    except Exception as e:
        print(f"\nError al ejecutar: {e}")
        input("\nPresiona Enter para continuar...")

def menu_macros():
    while True:
        mostrar_menu_macros()
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            ejecutar_script("macros/macro2.sh")
        elif opcion == "2":
            ejecutar_script("nmap/dispositivos.sh")
        elif opcion == "3":
            # Ejecutar con sudo
            ejecutar_script("nmap/scanOS.sh", usar_sudo=True)
        elif opcion == "0":
            break
        else:
            print("\n Opción no válida")
            input("Presiona Enter para continuar...")

def hera_hub():
    while True:
        mostrar_menu_principal()
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            ejecutar_python("contraseñas/generador.py")
        elif opcion == "2":
            menu_macros()
        elif opcion == "3":
            ejecutar_python("install/install.py")
        elif opcion == "4":
            ejecutar_python("sherlock/sherlock-found.py")
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n Opción no válida")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    hera_hub()
